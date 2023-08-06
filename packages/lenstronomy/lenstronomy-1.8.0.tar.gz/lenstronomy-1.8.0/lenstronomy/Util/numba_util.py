import lenstronomy
import os
import yaml
import numpy as np

"""
From pyautolens:
Depending on if we're using a super computer, we want two different numba decorators:
If on laptop:
@numba.jit(nopython=True, cache=True, parallel=False)
If on super computer:
@numba.jit(nopython=True, cache=False, parallel=True)
"""

# in case the xdg library is installed, the import statement with pyxdg can raise an error
# to avoid it, we draw back to the ~/.config directory in case this import fails.
# TODO come up with more permanent solution of path to configuration directory
try:
    from xdg.BaseDirectory import xdg_config_home
except ImportError:
    xdg_config_home = '~/.config'

user_config_file = os.path.join(xdg_config_home, "lenstronomy", "config.yaml")

module_path = os.path.dirname(lenstronomy.__file__)
default_config_file = os.path.join(module_path, 'Conf', 'conf_default.yaml')

if os.path.exists(user_config_file ):
    conf_file = user_config_file
else:
    conf_file = default_config_file

with open(conf_file) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    conf = yaml.load(file, Loader=yaml.FullLoader)
    numba_conf = conf['numba']
    nopython = numba_conf['nopython']
    cache = numba_conf['cache']
    parallel = numba_conf['parallel']
    numba_enabled = numba_conf['enable']
    fastmath = numba_conf['fastmath']
    error_model = numba_conf['error_model']

if numba_enabled:
    try:
        import numba
    except ImportError:
        numba_enabled = False

__all__ = ['jit', 'generated_jit']


def jit(nopython=nopython, cache=cache, parallel=parallel, fastmath=fastmath, error_model=error_model):
    if numba_enabled:
        def wrapper(func):
            return numba.jit(func, nopython=nopython, cache=cache, parallel=parallel, fastmath=fastmath, error_model=error_model)
    else:
        def wrapper(func):
            return func
    return wrapper

def generated_jit(nopython=nopython, cache=cache, parallel=parallel, fastmath=fastmath, error_model=error_model):
    """ Wrapper around numba.generated_jit. Allows you to redirect a function to another based on its type - see the Numba docs for more info"""
    if numba_enabled:
        def wrapper(func):
            return numba.generated_jit(func, nopython=nopython, cache=cache, parallel=parallel, fastmath=fastmath, error_model=error_model)
    else:
        def wrapper(func):
            return func

    return wrapper


@generated_jit()
def nan_to_num(x, posinf=1e10, neginf=-1e10, nan=0.):
    """
    Implements a Numba equivalent to np.nan_to_num (with copy=False!) array or scalar in Numba.
    Behaviour is the same as np.nan_to_num with copy=False, although it only supports 1-dimensional arrays and scalar inputs.
    """
    # The generated_jit part is necessary because of the need to support both arrays and scalars for all input functions.
    if (isinstance(x, numba.types.Array) or isinstance(x, np.ndarray)) and x.ndim > 0:
        return nan_to_num_arr if numba_enabled else nan_to_num_arr(x, posinf, neginf, nan)
    else:
        return nan_to_num_single if numba_enabled else nan_to_num_single(x, posinf, neginf, nan)


@jit()
def nan_to_num_arr(x, posinf=1e10, neginf=-1e10, nan=0.):
    """Part of the Numba implementation of np.nan_to_num - see nan_to_num"""
    for i in range(len(x)):
        if np.isnan(x[i]):
            x[i] = nan
        if np.isinf(x[i]):
            if x[i] > 0:
                x[i]=posinf
            else:
                x[i]=neginf
    return x


@jit()
def nan_to_num_single(x, posinf=1e10, neginf=-1e10, nan=0.):
    """Part of the Numba implementation of np.nan_to_num - see nan_to_num"""
    if np.isnan(x):
        return nan
    elif np.isinf(x):
        if x > 0:
            return posinf
        else:
            return neginf
    else:
        return x
