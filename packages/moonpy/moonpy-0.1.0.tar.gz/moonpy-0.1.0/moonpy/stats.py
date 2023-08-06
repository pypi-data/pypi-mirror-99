import numpy as np
from scipy.stats.mstats import mquantiles


def quantile(ary, q, axis=None, limit=None):
    """Use same quantile function as R (Type 7)."""
    assert isinstance(ary, np.ndarray)
    if limit is None:
        limit = tuple()
    return mquantiles(ary, q, alphap=1, betap=1, axis=axis, limit=limit)
