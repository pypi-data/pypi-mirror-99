import sys
import functools
import collections
import time
from distutils.version import LooseVersion

import matplotlib
import PIL.Image
import numpy as np
from io import BytesIO as StringIO

from glue import __version__ as glue_version
from glue.core import Data

GLUE_LT_016 = LooseVersion(glue_version) < LooseVersion('0.16')

if sys.version_info[:2] < (3, 7):
    from contextlib import contextmanager  # noqa

    @contextmanager
    def nullcontext():
        yield None

else:
    from contextlib import nullcontext  # noqa


def float_or_none(x):
    return float(x) if x is not None else None


def rgba_to_png_data(rgba):
    width, height = rgba.shape[1], rgba.shape[0]
    f = StringIO()
    img = PIL.Image.frombuffer("RGBA", (width, height), rgba, 'raw', 'RGBA', 0, 0)
    img.save(f, "png")
    return f.getvalue()


def scalar_to_png_data(data, colormap='viridis'):
    mask = ~np.isfinite(data)
    intensity = np.ma.masked_array(data, mask)
    colormap = matplotlib.cm.get_cmap(colormap)
    colormap.set_bad(alpha=0)
    data = colormap(intensity, bytes=True)
    return rgba_to_png_data(data)


def reduce_size(data, max_size):
    for axis in range(3):
        shape = data.shape
        while shape[axis] > max_size:
            slices1 = [slice(None, None, None)] * 3
            slices1[axis] = slice(0, -1, 2)
            slices2 = [slice(None, None, None)] * 3
            slices2[axis] = slice(1, None, 2)
            data = data[slices1]
            shape = data.shape
    return data


def _update_not_none(d, **kwargs):
    for key, value in kwargs.items():
        if value is not None:
            d[key] = value


def grid_slice(xmin, xmax, shape, ymin, ymax):
    '''Given a grid with shape, and begin and end coordinates xmin, xmax, what slice
    do we need to take such that it minimally covers ymin, ymax.
    xmin, xmax = 0, 1; shape = 4
    0  0.25  0.5  0.75  1
    |    |    |    |    |
    ymin, ymax = 0.5, 1.0 should give 2,4, 0.5, 1.0
    ymin, ymax = 0.4, 1.0 should give 1,4, 0.25, 1.0

    ymin, ymax = -1, 1.0 should give 0,4, 0, 1.0

    what about negative ymin and ymax ?
    It will just flip ymin and ymax
    ymin, ymax = 1.0, 0.5 should give 2,4, 0.5, 1.5

    xmin, xmax = 1, 0; shape = 4
    1  0.75  0.5  0.25  0
    |    |    |    |    |
    ymin, ymax = 0.5, 1.0 should give 0,2, 1.0, 0.5
    ymin, ymax = 0.4, 1.0 should give 0,3, 1.0, 0.25

    '''
    width = (xmax - xmin)
    ymin, ymax = min(ymin, ymax), max(ymin, ymax)
    # normalize the coordinates
    nmin = (ymin - xmin) / width
    nmax = (ymax - xmin) / width
    # grid indices
    if width < 0:
        imin = max(0, int(np.floor(nmax * shape)))
        imax = min(shape, int(np.ceil(nmin * shape)))
    else:
        imin = max(0, int(np.floor(nmin * shape)))
        imax = min(shape, int(np.ceil(nmax * shape)))
    # transform back to the coordinate system of x
    nmin = imin / shape
    nmax = imax / shape
#     if width < 0:
#         return imin, imax, xmin + nmax * width, xmin + nmin * width
#     else:
    return (imin, imax), (xmin + nmin * width, xmin + nmax * width)


def get_ioloop():
    import IPython
    import zmq
    ipython = IPython.get_ipython()
    if ipython and hasattr(ipython, 'kernel'):
        return zmq.eventloop.ioloop.IOLoop.instance()


def debounced(delay_seconds=0.5, method=False):
    def wrapped(f):
        counters = collections.defaultdict(int)

        @functools.wraps(f)
        def execute(*args, **kwargs):
            if method:  # if it is a method, we want to have a counter per instance
                key = args[0]
            else:
                key = None
            counters[key] += 1

            def debounced_execute(counter=counters[key]):
                # only execute if the counter wasn't changed in the meantime
                if counter == counters[key]:
                    f(*args, **kwargs)
            ioloop = get_ioloop()

            def thread_safe():
                ioloop.add_timeout(time.time() + delay_seconds, debounced_execute)
            if ioloop is None:  # not IPython, maybe unittest
                debounced_execute()
            else:
                ioloop.add_callback(thread_safe)
        return execute
    return wrapped


def colormap_to_hexlist(cmap, N=256):
    x = np.linspace(0, 1, N)
    colors = ["#%02x%02x%02x" % tuple([int(k * 255) for k in color]) for color in cmap(x)[:, :3]]
    return colors


def validate_data_argument(data_collection, data):
    """
    Validate the data argument passed to the viewer functions and return
    a glue data object.
    """

    if data is None:
        if len(data_collection) == 0:
            raise ValueError('No dataset is present in the data collection, '
                             'load or add a dataset before creating a data viewer')
        elif len(data_collection) > 1:
            raise ValueError('There is more than one dataset in the data '
                             'collection, please pass a data argument')
        else:
            return data_collection[0]
    elif isinstance(data, str):
        if GLUE_LT_016 and data in [d.label for d in data_collection]:
            for d in data_collection:
                if d.label == data:
                    return d
        elif not GLUE_LT_016 and data in data_collection:
            return data_collection[data]
        else:
            raise ValueError(f"'{data}' is not a valid dataset name. The "
                             f"following datasets are available:\n\n" +
                             "\n".join([f"  * '{d.label}'" for d in data_collection]))
    elif not isinstance(data, Data):
        raise TypeError('The data argument should either be a glue data '
                        'object or the name of a dataset.\nThe following '
                        'datasets are available:\n\n' +
                        '\n'.join([f"  * '{d.label}'" for d in data_collection]))
    else:
        return data
