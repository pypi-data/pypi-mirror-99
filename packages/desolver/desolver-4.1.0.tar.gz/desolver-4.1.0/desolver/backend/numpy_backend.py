from .common import *

import numpy
import scipy
import scipy.special

# Datatypes
bool = numpy.bool
float16 = numpy.float16
float32 = numpy.float32
float64 = numpy.float64
uint8 = numpy.uint8
int16 = numpy.int16
int32 = numpy.int32
int64 = numpy.int64

float_fmts.update({
    'float16': float16,
    'float32': float32,
    'float64': float64
})


def asarray(x):
    return array(x)


def to_float(x):
    return numpy.asanyarray(x).astype(float64)


def to_type(x, dtype):
    return numpy.asanyarray(x).astype(dtype)


# Convenience Decorators
def type_reg(f):
    def _wrapped(*args, **kwargs):
        kwargs.setdefault("dtype", float_fmts[float_fmt()])
        return f(*args, **kwargs)

    _wrapped.original_function = f
    return _wrapped


# Fundamental Mathematical Operators
neg = numpy.negative
pow = numpy.power
abs = numpy.abs
sqrt = numpy.sqrt

exp = numpy.exp
expm1 = numpy.expm1
log = numpy.log
log10 = numpy.log10
log1p = numpy.log1p
log2 = numpy.log2

add = numpy.add
sub = numpy.subtract
div = numpy.divide
mul = numpy.multiply

reciprocal = numpy.reciprocal
remainder = numpy.remainder

ceil = numpy.ceil
floor = numpy.floor
round = numpy.round
fmod = numpy.fmod

clip = numpy.clip
sign = numpy.sign
trunc = numpy.trunc

# Trigonometric Functions
cos = numpy.cos
sin = numpy.sin
tan = numpy.tan

cosh = numpy.cosh
sinh = numpy.sinh
tanh = numpy.tanh

acos = numpy.arccos
asin = numpy.arcsin
atan = numpy.arctan
atan2 = numpy.arctan2

# Other Functions
digamma = scipy.special.digamma
erf = scipy.special.erf
erfc = scipy.special.erfc
erfinv = scipy.special.erfinv
sigmoid = scipy.special.expit


def softplus(x, out=None):
    return log(1 + exp(x), out=out)


# Additional Definitions
def rsqrt(x, out=None):
    return pow(x, -0.5, out=out)


def square(x, out=None):
    return pow(x, 2, out=out)


def addcdiv(x, y1=None, y2=None, value=1, out=None):
    if y1 is None or y2 is None:
        raise ValueError("y1 and y2 must both be specified")
    if out is None:
        out = value * div(y1, y2)
        out = x + out
    else:
        div(y1, y2, out=out)
        mul(value, out, out=out)
        add(x, out, out=out)
    return out


def addcmul(x, y1=None, y2=None, value=1, out=None):
    if y1 is None or y2 is None:
        raise ValueError("y1 and y2 must both be specified")
    if out is None:
        out = value * mul(y1, y2)
        out = x + out
    else:
        mul(y1, y2, out=out)
        mul(value, out, out=out)
        add(x, out, out=out)
    return out


def frac(x, out=None):
    if out is None:
        return x - floor(x)
    floor(x, out=out)
    sub(x, out, out=out)
    return out


def lerp(start, end, weight, out=None):
    if out is None:
        return start + weight * (end - start)
    sub(end, start, out=out)
    mul(weight, out, out=out)
    add(start, out, out=out)
    return out


def mvlgamma(x, p):
    return scipy.special.multigammaln(x, d=p)


# Common Array Operations
einsum = numpy.einsum
concatenate = numpy.concatenate
append = numpy.append
stack = numpy.stack
ravel = numpy.ravel
flatten = numpy.ravel
arange = type_reg(numpy.arange)
logspace = type_reg(numpy.logspace)
linspace = type_reg(numpy.linspace)
eye = type_reg(numpy.eye)

# Reduction Ops
argmax = numpy.argmax
argmin = numpy.argmin
cumprod = numpy.cumprod
cumsum = numpy.cumsum
logsumexp = scipy.special.logsumexp
mean = numpy.mean
median = numpy.median
prod = numpy.prod
std = numpy.std
var = numpy.var
sum = numpy.sum
norm = numpy.linalg.norm


def dist(x, y, ord=2):
    if asarray(x).dtype == float16 or asarray(y).dtype == float16:
        return numpy.linalg.norm(asarray(x).astype(float64) - asarray(y).astype(float64), ord=ord).astype(float16)
    else:
        return numpy.linalg.norm(x - y, ord=ord)


# Comparison Ops
allclose = numpy.allclose
argsort = numpy.argsort

eq = numpy.equal
ne = numpy.not_equal
ge = numpy.greater_equal
gt = numpy.greater
le = numpy.less_equal
lt = numpy.less


def equal(*args, **kwargs):
    return numpy.all(eq(*args, **kwargs))


isfinite = numpy.isfinite
isinf = numpy.isinf
isnan = numpy.isnan
max = numpy.max
min = numpy.min
any = numpy.any
all = numpy.all

array = type_reg(numpy.array)
zeros = type_reg(numpy.zeros)
ones  = type_reg(numpy.ones)
empty = type_reg(numpy.empty)
full = type_reg(numpy.full)
zeros_like = type_reg(numpy.zeros_like)
ones_like = type_reg(numpy.ones_like)
empty_like = type_reg(numpy.empty_like)
full_like = type_reg(numpy.full_like)


def to_numpy(x):
    return numpy.asarray(x)


def as_bool_array(x):
    return numpy.asarray(x).astype(bool)


def copy(x):
    return numpy.copy(x)


def reshape(x, new_dims):
    return numpy.reshape(asarray(x), new_dims)


def shape(x):
    return numpy.shape(x)


def logical_not(x, out=None, where=True):
    return numpy.logical_not(x, out=out, where=where)


def logical_or(a, b, out=None, where=True):
    return numpy.logical_or(a, b, out=out, where=where)


def logical_and(a, b, out=None, where=True):
    return numpy.logical_and(a, b, out=out, where=where)


def logical_xor(a, b, out=None, where=True):
    return numpy.logical_xor(a, b, out=out, where=where)

nonzero = numpy.nonzero
argsort = numpy.argsort

def solve_linear_system(A,b,overwrite_a=True,overwrite_b=True,check_finite=False):
    return scipy.linalg.solve(A,b,overwrite_a=overwrite_a,overwrite_b=overwrite_b,check_finite=check_finite)

matrix_inv = numpy.linalg.inv
