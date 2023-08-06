import datetime
import json
import logging
import multiprocessing
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

if not os.getenv("CLOUD_PROVIDER") or os.getenv("CLOUD_PROVIDER") == "gcp":
    import google.auth
    import google.auth.transport
    import google.auth.transport.requests
    from google.cloud import storage  # pylint: disable=no-name-in-module
    from googleapiclient import errors

# fmt: off
FilePath = Union[str, Path]
# Superficial JSON input/output types
# https://github.com/python/typing/issues/182#issuecomment-186684288
JSONOutput = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JSONOutputBin = Union[bytes, str, int, float, bool, None, Dict[str, Any], List[Any]]
# For input, we also accept tuples, ordered dicts etc.
JSONInput = Union[str, int, float, bool, None, Dict[str, Any], List[Any], Tuple[Any], OrderedDict]
JSONInputBin = Union[bytes, str, int, float, bool, None, Dict[str, Any], List[Any], Tuple[Any], OrderedDict]
YAMLInput = JSONInput
YAMLOutput = JSONOutput
# fmt: on

######################
#  operating system  #
######################
is_windows = sys.platform.startswith("win")
is_linux = sys.platform.startswith("linux")
is_osx = sys.platform == "darwin"


#################
#  file system  #
#################


def path2str(path):
    return str(path)


def b_to_str(b_str):
    return str(b_str, encoding="utf-8")


def ensure_path(path):
    if isinstance(path, str):
        return Path(path)
    else:
        return path


#########
# symlink
#########
def symlink(orig, dest):
    """Create a symlink.

    :orig (unicode / Path): Origin path
    :dest (unicode / Path): Destination path of the symlink.
    """
    if is_windows:
        import subprocess

        subprocess.check_call(
            ["mklink", "/d", path2str(orig), path2str(dest)], shell=True
        )
    else:
        orig.symlink_to(dest)


def symlink_remove(link):
    """Remove a symlnk.

    :link (unicode / Path): The path to the symlink.
    """
    os.unlink(path2str(link))


######
# json
######
def force_path(location, require_exists=True):
    if not isinstance(location, Path):
        location = Path(location)
    if require_exists and not location.exists():
        raise ValueError(f"Can't read file: {location}")
    return location


def force_string(location):
    if isinstance(location, str):
        return location
    return str(location)


def json_dumps(
    data: JSONInput, indent: Optional[int] = 0, sort_keys: bool = False
) -> str:
    if sort_keys:
        indent = None if indent == 0 else indent
        result = json.dumps(
            data, indent=indent, separators=(",", ":"), sort_keys=sort_keys
        )
    else:
        result = json.dumps(data, indent=indent, escape_forward_slashes=False)
    return result


def read_json(location: FilePath) -> JSONOutput:
    if location == "-":
        data = sys.stdin.read()
        return json.loads(data)
    file_path = force_path(location)
    with file_path.open("r", encoding="utf8") as f:
        return json.load(f)


def write_json(location: FilePath, data: JSONInput, indent: int = 2) -> None:
    json_data = json_dumps(data, indent=indent)
    if location == "-":
        print(json_data)
    else:
        file_path = force_path(location, require_exists=False)
        with file_path.open("w", encoding="utf8") as f:
            f.write(json_data)


#########
#  run  #
#########
def run(command, cwd=None, env=None, polling_interval=datetime.timedelta(seconds=1)):
    """Run a subprocess.

    Any subprocess output is emitted through the logging modules.

    Returns:
      output: A string containing the output.
    """
    logging.info("Running: %s \ncwd=%s", " ".join(command), cwd)

    if not env:
        env = os.environ
    else:
        keys = sorted(env.keys())

        lines = []
        for k in keys:
            lines.append("{}={}".format(k, env[k]))

    process = subprocess.Popen(
        command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    logging.info("Subprocess output:\n")
    output = []
    while process.poll() is None:
        process.stdout.flush()
        for line in iter(process.stdout.readline, b""):
            line = line.decode().strip()
            output.append(line)
            logging.info(line)

        time.sleep(polling_interval.total_seconds())

    process.stdout.flush()
    for line in iter(process.stdout.readline, b""):
        line = line.decode().strip()
        output.append(line)
        logging.info(line)

    if process.returncode != 0:
        raise subprocess.CalledProcessError(
            process.returncode,
            "cmd: {} exited with code {}".format(" ".join(command), process.returncode),
            "\n".join(output),
        )

    return "\n".join(output)


def run_and_output(*args, **argv):
    return run(*args, **argv)


###############
#  git clone  #
###############
def clone_repo(dest, repo_owner, repo_name, sha=None, branches=None):
    """Clone the repo,

    Args:
      dest: This is the root path for the training code.
      repo_owner: The owner for github organization.
      repo_name: The repo name.
      sha: The sha number of the repo.
      branches: (Optional): One or more branches to fetch. Each branch be specified
        as "remote:local". If no sha is provided
        we will checkout the last branch provided. If a sha is provided we
        checkout the provided sha.

    Returns:
      dest: Directory where it was checked out
      sha: The sha of the code.
    """
    repo = f"https://github.com/{repo_owner}/{repo_name}.git"
    logging.info(f"repo {repo}")

    run(["git", "clone", repo, dest])

    if branches:
        for b in branches:
            run(
                [
                    "git",
                    "fetch",
                    "origin",
                    b,
                ],
                cwd=dest,
            )

        if not sha:
            b = branches[-1].split(":", 1)[-1]
            run(
                [
                    "git",
                    "checkout",
                    b,
                ],
                cwd=dest,
            )

    if sha:
        run(["git", "checkout", sha], cwd=dest)

    # Get the actual git hash.
    # This ensures even for periodic jobs which don't set the sha we know
    # the version of the code tested.
    sha = run_and_output(["git", "rev-parse", "HEAD"], cwd=dest)

    return dest, sha


#########
#  gcs  #
#########
def to_gcs_uri(bucket, path):
    """Convert bucket and path to a GCS URI."""
    return f"gs://{os.path.join(bucket, path)}"


GCS_REGEX = re.compile("gs://([^/]*)(/.*)?")


def split_gcs_uri(gcs_uri):
    """Split a GCS URI into bucket and path."""
    m = GCS_REGEX.match(gcs_uri)
    bucket = m.group(1)
    path = ""
    if m.group(2):
        path = m.group(2).lstrip("/")
    return bucket, path


def upload_to_gcs(contents, target):
    gcs_client = storage.Client()

    bucket_name, path = split_gcs_uri(target)

    bucket = gcs_client.get_bucket(bucket_name)
    logging.info(f"Writing {target}")
    blob = bucket.blob(path)
    blob.upload_from_string(contents)


def upload_file_to_gcs(source, target):
    gcs_client = storage.Client()
    bucket_name, path = split_gcs_uri(target)

    bucket = gcs_client.get_bucket(bucket_name)

    logging.info(f"Uploading file {source} to {target}.")
    blob = bucket.blob(path)
    blob.upload_from_filename(source)


def read_file(path):
    """Read a file.

    Args:
      path: A local or GCS path.

    Returns:
      contents: Contents of the file
    """

    if not path.lower().startswith("gs://"):
        with open(path) as hf:
            hf.read()

    bucket_name, path = split_gcs_uri(path)

    gcs_client = storage.Client()

    bucket = gcs_client.get_bucket(bucket_name)

    blob = bucket.blob(path)
    return blob.download_as_string()


#####################
#  service account  #
#####################
def maybe_activate_service_account():
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        logging.info(
            "GOOGLE_APPLICATION_CREDENTIALS is set; configuring gcloud "
            "to use service account."
        )
        run(
            [
                "gcloud",
                "auth",
                "activate-service-account",
                "--key-file=" + os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
            ]
        )

    else:
        logging.info("GOOGLE_APPLICATION_CREDENTIALS is not set.")
