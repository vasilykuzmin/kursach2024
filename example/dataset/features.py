import numpy as np

def CA(x: np.ndarray) -> np.ndarray:
    """Cumulative average."""

    return np.cumsum(x, axis=-1) / np.arange(1, x.shape[-1] + 1)

def CMA(x: np.ndarray, n: int) -> np.ndarray:
    """Cumulative moving average."""

    x_ = x
    x_ = np.cumsum(x_, axis=-1)
    x_[..., n:] -= x_[..., :-n]
    return x_[..., n - 1:] / n

def WA(x: np.ndarray) -> np.ndarray:
    """Linear weighted average."""

    return np.cumsum(x * np.arange(1, x.shape[-1] + 1)) / np.cumsum(np.arange(1, x.shape[-1] + 1))

def WMA(x: np.ndarray, n: int, doublePrecision: bool = True) -> np.ndarray:
    """Linear weighted moving average. Numerical instability."""

    x_ = x
    if doublePrecision:
        x_ = x_.astype(np.float128)
    csum = np.cumsum(x_, axis=-1)
    csum[..., n:] -= csum[..., :-n]
    if doublePrecision:
        x_ = np.cumsum(x_ * np.arange(1, x_.shape[-1] + 1, dtype=np.float64))
    else:
        x_ = np.cumsum(x_ * np.arange(1, x_.shape[-1] + 1))
    x_[..., n:] -= x_[..., :-n]
    return ((x_[..., n-1:] - csum[..., n-1:] * np.arange(0, x_.shape[-1] - n + 1)) / (n * (n + 1) // 2)).astype(np.float64)

def EA(x: np.ndarray, alpha: float) -> np.ndarray:
    """Exponential weighted average."""

    p = x.flatten()
    q = np.ones(x.shape)
    for i in range(0, x.size, x.shape[-1]):
        for j in range(1, x.shape[-1]):
            q[i + j] = q[i + j - 1] * alpha + 1
            p[i + j] += p[i + j - 1] * alpha
    return (p / q).reshape(x.shape)

def EMA(x: np.ndarray, n: int, alpha: float = None, doublePrecision: bool = True) -> np.ndarray:
    """Exponential weighted moving average. Default alpha is (n - 1) / (n + 1). Numerical instability."""

    if alpha is None:
        alpha = (n - 1) / (n + 1)
    xshape = x.shape
    x = x.flatten()
    p = np.asanyarray(x.copy(), dtype=(np.float128 if doublePrecision else np.float64))
    alphan = alpha ** n
    for i in range(0, x.size, xshape[-1]):
        for j in range(1, min(xshape[-1], n)):
            p[i + j] = x[i + j] + p[i + j - 1] * alpha
        for j in range(n, xshape[-1]):
            p[i + j] = x[i + j] + p[i + j - 1] * alpha - x[i + j - n] * alphan
    x = x.reshape(xshape)
    q = (alpha ** np.arange(0, n)).sum()
    return (p / q).reshape(xshape)[..., n-1:].astype(np.float64)

def MACD(x: np.ndarray, 
        nShort: int, nLong: int, nTotal: int, 
        alphaShort: float = None, alphaLong: float = None, alphaTotal: float = None, 
        doublePrecision: bool = True) -> np.ndarray:
    """Moving average convergence/divergence. Default alpha is (n - 1) / (n + 1). Numerical instability."""

    emaShort = EMA(x, nShort, alphaShort, doublePrecision)
    emaLong = EMA(x, nLong, alphaLong, doublePrecision)
    align = min(emaShort.shape[-1], emaLong.shape[-1])
    emaShort = emaShort[..., -align:]
    emaLong = emaLong[..., -align:]
    return EMA(emaShort - emaLong, nTotal, alphaTotal, doublePrecision).astype(np.float64)

def RSI(x: np.ndarray, n: int, alpha: float = None, doublePrecision: bool = True) -> np.ndarray:
    """Relative strength index. Default alpha is (n - 1) / (n + 1). Numerical instability."""

    diffs = x[..., 1:] - x[..., :-1]
    ups   = np.where(diffs > 0 ,  diffs, 0)
    downs = np.where(diffs <= 0, -diffs, 0)
    ups   = EMA(ups  , n, alpha, doublePrecision)
    downs = EMA(downs, n, alpha, doublePrecision)
    return ups / (ups + downs)

def ROC(x : np.ndarray, n : int) -> np.ndarray:
    """Rate of change indicator"""

    return (x[..., n:] - x[..., :-n]) / (x[..., :-n] + 2)

def TSI(x: np.ndarray, n1: int, n2: int, alpha1: float = None, alpha2: float = None, doublePrecision: bool = True) -> np.ndarray:
    """True strength index. Default alphas are (n - 1) / (n + 1). Numerical instability."""

    diffs = x[..., 1:] - x[..., :-1]
    p = EMA(diffs        , n1, alpha1, doublePrecision)
    q = EMA(np.abs(diffs), n1, alpha1, doublePrecision)
    p = EMA(p, n2, alpha2, doublePrecision)
    q = EMA(q, n2, alpha2, doublePrecision)
    q[q == 0] = p[q == 0] = 1
    return p / q
