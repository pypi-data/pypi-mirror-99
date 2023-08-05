import copy
import csv
import inspect
import tempfile
from collections import OrderedDict
from functools import partial, wraps
from types import GeneratorType


def immutable(func):
    """
    Decorator for wrapper "builder" functions.  These are functions on the Query class or other classes used for
    building queries which mutate the query and return self.  To make the build functions immutable, this decorator is
    used which will deepcopy the current instance.  This decorator will return the return value of the inner function
    or the new copy of the instance.  The inner function does not need to return self.
    """

    def _copy(self, *args, mutate=False, **kwargs):
        """
        :param mutate:
            When True, overrides the immutable behavior of this decorator.
        """
        self_copy = self if mutate else copy.deepcopy(self)
        result = func(self_copy, *args, **kwargs)

        # Return self if the inner function returns None.  This way the inner function can return something
        # different (for example when creating joins, a different builder is returned).
        if result is None:
            return self_copy

        return result

    return _copy


def deepcopy(value, memodict):
    cls = value.__class__
    result = cls.__new__(cls)

    memodict[id(value)] = result

    for k, v in value.__dict__.items():
        result.__dict__[k] = copy.deepcopy(v, memodict)

    return result


def wrap_list(value, wrapper=list):
    return value if isinstance(value, (tuple, list)) else wrapper([value])


def setdeepattr(d, keys, value):
    """
    Similar to the built-in `setattr`, this function accepts a list/tuple of keys to set a value deep in a `dict`

    Given the following dict structure

    .. code-block:: python

        d = {
          'A': {
            '0': {
              'a': 1,
              'b': 2,
            }
          },
        }

    Calling `setdeepattr` with a key path to a value deep in the structure will set that value. If the value or any
    of the objects in the key path do not exist, then a dict will be created.

    .. code-block:: python

        # Overwrites the value in `d` at A.0.a, which was 1, to 3
        setdeepattr(d, ('A', '0', 'a'), 3)

        # Adds an entry in `d` to A.0 with the key 'c' and the value 3
        setdeepattr(d, ('A', '0', 'c'), 3)

        # Adds an entry in `d` with the key 'X' and the value a new dict
        # Adds an entry in `d` to `X` with the key '0' and the value a new dict
        # Adds an entry in `d` to `X.0` with the key 'a' and the value 0
        setdeepattr(d, ('X', '0', 'a'), 0)

    :param d:
        A dict value with nested dict attributes.
    :param keys:
        A list/tuple path of keys in `d` to the desired value
    :param value:
        The value to set at the given path `keys`.
    """
    if not isinstance(keys, (list, tuple)):
        keys = (keys,)

    top, *rest = keys

    if rest:
        if top not in d:
            d[top] = {}

        setdeepattr(d[top], rest, value)

    else:
        d[top] = value


def getdeepattr(d, keys, default_value=None):
    """
    Similar to the built-in `getattr`, this function accepts a list/tuple of keys to get a value deep in a `dict`

    Given the following dict structure

    .. code-block:: python

        d = {
          'A': {
            '0': {
              'a': 1,
              'b': 2,
            }
          },
        }

    Calling `getdeepattr` with a key path to a value deep in the structure will return that value. If the value or any
    of the objects in the key path do not exist, then the default value is returned.

    .. code-block:: python

        assert 1 == getdeepattr(d, ('A', '0', 'a'))
        assert 2 == getdeepattr(d, ('A', '0', 'b'))
        assert 0 == getdeepattr(d, ('A', '0', 'c'), default_value=0)
        assert 0 == getdeepattr(d, ('X', '0', 'a'), default_value=0)

    :param d:
        A dict value with nested dict attributes.
    :param keys:
        A list/tuple path of keys in `d` to the desired value
    :param default_value:
        A default value that will be returned if the path `keys` does not yield a value.
    :return:
        The value following the path `keys` or `default_value`
    """
    d_level = d

    for key in keys:
        if key not in d_level:
            return default_value

        d_level = d_level[key]

    return d_level


def apply_kwargs(f, *args, **kwargs):
    argspec = inspect.getfullargspec(f)
    allowed = set(argspec.args[-len(argspec.defaults or ()) :])
    return f(*args, **{key: kwarg for key, kwarg in kwargs.items() if argspec.varkw or key in allowed})


def filter_kwargs(f):
    """
    Removes any kwargs from function call that are not accepted by the called function.

    :param f:
    :return:
    """
    return partial(apply_kwargs, f)


def flatten(items):
    return [item for level in items for item in wrap_list(level)]


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    return [l[i : i + n] for i in range(0, len(l), n)]


def ordered_distinct_list(l):
    seen = set()
    return [x for x in l if not x in seen and not seen.add(x)]


def ordered_distinct_list_by_attr(l, attr="alias", keep_last=False):
    mapping = {}  # will contain mapping from attr_value to item
    for item in l:
        attr_value = getattr(item, attr)
        if not keep_last and attr_value in mapping:
            # only keep the first occurrence in the result so skip the item if the attribute value is already present
            continue

        mapping[attr_value] = item

    return list(mapping.values())


def groupby(items, by):
    """
    Group items using a function to derive a key.

    :param items:
        The items to group

    :param by:
        A lambda function to create a key based on the item

    :return:
        an Ordered dict
    """
    result = OrderedDict()
    for item in items:
        key = by(item)

        if key in result:
            result[key].append(item)
        else:
            result[key] = [item]

    return result


def alias_selector(alias):
    if alias is None or alias.startswith("$"):
        return alias
    return "${}".format(alias)


def alias_for_alias_selector(f_alias):
    if f_alias and f_alias[0] == "$":
        return f_alias[1:]
    return f_alias


def reduce_data_frame_levels(data_frame, level):
    reduced = data_frame.reset_index(level=level, drop=True)
    if reduced.size == 1 and reduced.index.names == [None]:
        return reduced.iloc[0]
    return reduced


def read_csv(fp):
    """
    Read a csv file and return its content.

    :param fp: Path of the file.
    :return: List of rows.
    """
    rows = []
    with open(fp, "r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            rows.append(row)

    return rows


def write_named_temp_csv(rows):
    """
    Write the provided rows to a named temporary file.

    :param rows: List of lists to be written.
    :return: A named temporary file containing the rows.
    """
    ntf = tempfile.NamedTemporaryFile(suffix=".csv")
    with open(ntf.name, "w") as f:
        ntf_writer = csv.writer(f, delimiter=",")
        ntf_writer.writerows(rows)

    return ntf


def listify(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        retval = func(*args, **kwargs)
        if isinstance(retval, GeneratorType):
            return list(retval)
        return retval

    return new_func


def filter_nones(iterable):
    return filter(None.__ne__, iterable)
