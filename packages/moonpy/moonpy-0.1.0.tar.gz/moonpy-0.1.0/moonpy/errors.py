from __future__ import unicode_literals


def add_codes(err_cls):
    """Add error codes to string messages via class attribute names."""

    class ErrorsWithCodes(err_cls):
        def __getattribute__(self, code):
            msg = super(ErrorsWithCodes, self).__getattribute__(code)
            if code.startswith("__"):  # python system attributes like __class__
                return msg
            else:
                return "[{code}] {msg}".format(code=code, msg=msg)

    return ErrorsWithCodes()


# fmt: off

@add_codes
class Warnings(object):
    W001 = ()

@add_codes
class Errors(object):
    E001 = ()


@add_codes
class TempErrors(object):
    T001 = ()
