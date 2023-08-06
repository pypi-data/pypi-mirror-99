import collections
import inspect
import re
from collections import defaultdict
from copy import copy
from inspect import signature
from itertools import product

from six import string_types


def isiter(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def class_name(obj):
    class_name = str(type(obj))
    class_name = re.search(".*'(.+?)'.*", class_name).group(1)
    return class_name


def _can_iterate(obj):
    is_string = isinstance(obj, string_types)
    is_iterable = isinstance(obj, collections.Iterable)

    return is_iterable and not is_string


def is_column_vector(x):
    return len(x.shape) == 2 and x.shape[1] == 1


def is_row_vector(x):
    return len(x.shape) == 1


def _group_by(data, criteria):
    """
        Group objects in data using a function or a key
    """
    if isinstance(criteria, str):
        criteria_str = criteria

        def criteria(x):
            return x[criteria_str]

    res = defaultdict(list)
    for element in data:
        key = criteria(element)
        res[key].append(element)
    return res


def _get_params_value(params):
    """
        Given an iterator (k1, k2), returns a function that when called
        with an object obj returns a tuple of the form:
        ((k1, obj.parameters[k1]), (k2, obj.parameters[k2]))
    """
    # sort params for consistency
    ord_params = sorted(params)

    def fn(obj):
        l = []
        for p in ord_params:
            try:
                l.append((p, obj.parameters[p]))
            except:
                raise ValueError('{} is not a valid parameter'.format(p))
        return tuple(l)

    return fn


def _sorted_map_iter(d):
    ord_keys = sorted(d.keys())
    for k in ord_keys:
        yield (k, d[k])


def _product(k, v):
    """
        Perform the product between two objects
        even if they don't support iteration
    """
    if not _can_iterate(k):
        k = [k]
    if not _can_iterate(v):
        v = [v]
    return list(product(k, v))


def _mapping_to_tuple_pairs(d):
    """
        Convert a mapping object (such as a dictionary) to tuple pairs,
        using its keys and values to generate the pairs and then generating
        all possible combinations between those
        e.g. {1: (1,2,3)} -> (((1, 1),), ((1, 2),), ((1, 3),))
    """
    # order the keys, this will prevent different implementations of Python,
    # return different results from the same dictionary since the order of
    # iteration depends on it
    t = []
    ord_keys = sorted(d.keys())
    for k in ord_keys:
        t.append(_product(k, d[k]))
    return tuple(product(*t))


def _flatten_list(l):
    return [item for sublist in l for item in sublist]


# http://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    import matplotlib.colors as colors
    import numpy as np
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def default_heatmap():
    import matplotlib.pyplot as plt
    return truncate_colormap(plt.cm.OrRd, 0.1, 0.7)


def map_parameters_in_fn_call(args, kwargs, func):
    """
    Based on function signature, parse args to to convert them to key-value
    pairs and merge them with kwargs
    Any parameter found in args that does not match the function signature
    is still passed.
    Missing parameters are filled with their default values
    """
    # Get missing parameters in kwargs to look for them in args
    args_spec = inspect.getargspec(func).args
    params_all = set(args_spec)
    params_missing = params_all - set(kwargs.keys())

    if 'self' in args_spec:
        offset = 1
    else:
        offset = 0

    # Get indexes for those args
    idxs = [args_spec.index(name) for name in params_missing]

    # Parse args
    args_parsed = dict()

    for idx in idxs:
        key = args_spec[idx]

        try:
            value = args[idx - offset]
        except IndexError:
            pass
        else:
            args_parsed[key] = value

    parsed = copy(kwargs)
    parsed.update(args_parsed)

    # fill default values
    default = {k: v.default for k, v
               in signature(func).parameters.items()
               if v.default != inspect._empty}

    to_add = set(default.keys()) - set(parsed.keys())

    default_to_add = {k: v for k, v in default.items() if k in to_add}
    parsed.update(default_to_add)

    return parsed
