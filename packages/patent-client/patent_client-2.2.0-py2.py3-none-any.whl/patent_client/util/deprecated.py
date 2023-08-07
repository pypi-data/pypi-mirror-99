import importlib
import json
from collections import OrderedDict
from copy import deepcopy
from hashlib import md5
import warnings
import itertools

import inflection
from dateutil.parser import parse as parse_dt


def hash_dict(dictionary):
    return md5(json.dumps(dictionary, sort_keys=True).encode("utf-8")).hexdigest()


FILTERS = {
    #'exact',
    #'iexact',
    #'contains',
    #'icontains',
    "in": lambda x, y: x in y,
    "eq": lambda x, y: x == y,
    #'gt',
    #'gte',
    #'lt',
    #'lte',
    #'startswith',
    #'istartswith',
    #'endswith',
    #'iendswith',
    #'range',
    #'date',
    #'year','
    #'month',
    #'day',
    #'week',
    #'week_day',
    #'quarter','
    #'time',
    #'hour','
    #'minute',
    #'second',
    #'isnull',
    #'regex',
    #'iregex',
}


def one_to_one(class_name, **mapping):
    module_name, class_name = class_name.rsplit(".", 1)

    @property
    def get(self):
        try:
            klass = getattr(importlib.import_module(module_name), class_name)
        except AttributeError:
            return None
        filter_obj = {k: getattr(self, v) for (k, v) in mapping.items()}
        return klass.objects.get(**filter_obj)

    return get


def one_to_many(class_name, **mapping):
    module_name, class_name = class_name.rsplit(".", 1)

    @property
    def get(self):
        klass = getattr(importlib.import_module(module_name), class_name)
        filter_obj = {k: getattr(self, v) for (k, v) in mapping.items()}
        return klass.objects.filter(**filter_obj)

    return get


def values_iterator(iterator, *keys, tuples=False):
    for v in iterator:
        if tuples:
            yield tuple(recur_accessor(v, k) for k in keys)
        else:
            yield {k: recur_accessor(v, k) for k in keys}


def recur_accessor(obj, accessor):
    if "__" not in accessor:
        a = accessor
        rest = None
    else:
        a, rest = accessor.split("__", 1)

    if hasattr(obj, a):
        new_obj = getattr(obj, a)
        if callable(new_obj):
            new_obj = new_obj()
    else:
        try:
            a = int(a)
        except ValueError:
            pass
        try:
            new_obj = obj[a]
        except (KeyError, TypeError, IndexError):
            new_obj = None
    if not rest:
        return new_obj
    else:
        return recur_accessor(new_obj, rest)


class Model(object):
    """
    Model Base Class

    Takes in a dictionary of data and :
    1. Automatically inflects all keys to underscore_case
    2. Converts any value that has "date" or "datetime" into the appropriate type
    3. Appends all keys in the dictionary as attributes on the object
    4. Attaches the original inflected data dictionary as Model.data
    """

    def __init__(self, data, backref=None, **kwargs):
        try:
            self.data = self._convert_data(data)

            for k, v in self.data.items():
                setattr(self, k, self.data[k])
        except Exception as e:
            self.error = e
        self.backref = backref

    def _convert_data(self, data):
        if isinstance(data, list):
            return [self._convert_data(a) for a in data]
        elif isinstance(data, dict):
            dictionary = {
                inflection.underscore(k): self._convert_data(v)
                for (k, v) in data.items()
            }
            for k, v in dictionary.items():
                try:
                    if "datetime" in k and type(v) == str:
                        dictionary[k] = parse_dt(v)
                    elif "date" in k and type(v) == str:
                        dictionary[k] = parse_dt(v).date()
                except ValueError:  # Malformed datetimes:
                    dictionary[k] = None
            return dictionary
        else:
            return data

    def as_dict(self):
        """Convert object to dictionary, recursively converting any objects to dictionaries themselves"""
        output = {key: getattr(self, key) for key in self.attrs if hasattr(self, key)}
        for k, v in output.items():
            if isinstance(v, list):
                output[k] = [i.asdict() if hasattr(i, "asdict") else i for i in v]
            if hasattr(v, "asdict"):
                output[k] = v.asdict()
        return output

    def __repr__(self):
        """Default representation"""
        primary_key = getattr(self, "primary_key", self.attrs[0])
        repr_string = (
            f"<{self.__class__.__name__} {primary_key}={getattr(self, primary_key)}"
        )
        if hasattr(self, "error"):
            repr_string += f" error={self.error}"
        return repr_string + ">"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return (self.__class__ == other.__class__) and (hash(self) == hash(other))

    def __ne__(self, other):
        return not self.__eq__(other)


class BaseManager:
    """
    Manager Base Class

    This class is essentially a configurable generator. It is intended to be initialized 
    as an empty object at Model.objects. Users can then modify the manager by calling either:
        
        Manager.filter -> adds filter criteria
        Manager.sort -> adds sorting criteria
        Manager.options -> adds key:value options

    All methods should return a brand-new manager with the appropriate parameters re-set. The 
    Manager also has a special method to fetch a single matching object:

        Manager.get -> adds filter critera, and returns the first object if only one object is found, else raises an Exception

    The manager's attributes are stored in a dictionary at Manager.config. Config has the following structure:

        {
            'filter': {
                key: value,
                key: value,
            },
            'order_by': [value, value, value],
            'values': [value, value, value]
            'options': {
                key: value
            }
        }
        
    """

    def __init__(
        self, config=dict(filter=dict(), order_by=list(), options=dict()), values=list()
    ):
        self.config = config

    def __add__(self, other):
        return QuerySet(itertools.chain(self, other))

    def filter(self, *args, **kwargs):
        if args:
            kwargs[self.primary_key] = args
        for k, v in kwargs.items():
            if not isinstance(v, str):
                try:
                    kwargs[k] = list(str(i) for i in v)
                except TypeError:
                    kwargs[k] = str(v)

        new_config = deepcopy(self.config)
        new_config["filter"] = {**new_config["filter"], **kwargs}
        return self.__class__(new_config)

    def order_by(self, *args):
        """Take arguments, and store in a special keyword argument called 'sort' """
        new_config = deepcopy(self.config)
        new_config["order_by"] = list(new_config["order_by"]) + list(args)
        return self.__class__(new_config)

    def set_options(self, **kwargs):
        new_config = deepcopy(self.config)
        new_config["options"] = {**new_config["options"], **kwargs}
        return self.__class__(new_config)

    def get(self, *args, **kwargs):
        """Implement a new manager with the requested keywords, and if the length is 1,
        return that record, else raise an exception"""
        manager = self.filter(*args, **kwargs)
        if len(manager) > 1:
            doc_nos = "\n".join([str(r) for r in manager])
            raise ValueError("More than one document found!\n" + doc_nos)
        return manager.first()

    def values(self, *fields):
        """Return new manager with special keywords 'values__fields' and 'values__list'"""
        new_config = deepcopy(self.config)
        new_config["values"] = fields
        new_config["options"]["values_iterator"] = True
        new_config["options"]["values_list"] = False
        return self.__class__(new_config)

    def values_list(self, *fields, flat=False):
        """Same as values, but adds an additional parameter for "flat" lists """
        new_config = deepcopy(self.config)
        new_config["values"] = fields
        new_config["options"]["values_iterator"] = True
        new_config["options"]["values_list"] = True
        new_config["options"]["values_list_flat"] = flat
        return self.__class__(new_config)

    def to_pandas(self, limit=50):
        import pandas as pd

        objects = list(self)
        return pd.DataFrame.from_records(
            {k: getattr(r, k, None) for k in objects[0].attrs} for r in objects
        )

    def explode(self, attribute):
        from itertools import chain

        return QuerySet(chain.from_iterable(getattr(r, attribute, None) for r in self))


class QuerySet(BaseManager):
    """
    Utility class that extends the Manager helper function to 
    any collection of Patent Client objects
    """

    def __init__(self, iterable):
        self.iterable = iterable

    def __getitem__(self, key):
        return self.iterable[key]

    def __iter__(self):
        return iter(self.iterable)

    def __repr__(self):
        return f"<QuerySet({repr(self.iterable)})>"


class IterableManager(BaseManager):
    """
    Iterable Manager Base Class

    This class extends BaseManager for iterable managers. This requires that the extending manager
    implement __iter__. 

    This is used for all managers that are not container-like - i.e. does not provide a definite length

    """

    def first(self):
        return next(iter(self))


class Manager(BaseManager):
    """
    Standard Manager Base Class

    This class extends BaseManager by adding support for the __getitem__ method for iteration
    This is used for all managers that behave like containers, rather than pure iterators

    """

    def count(self):
        return len(self)

    def first(self):
        try:
            return self[0]
        except StopIteration:
            raise ValueError("No matching records found!")

    def all(self):
        return iter(self)

    def get_item(self, key):
        raise NotImplementedError(f"{self.__class__} has no get_item method")

    def __getitem__(self, key):
        """resolves slices and keys into Model objects. Relies on .get_item(key) to obtain
        the record itself"""
        if type(key) == slice:
            indices = list(range(len(self)))[key.start : key.stop : key.step]
            return [self.__getitem__(index) for index in indices]
        else:
            if key >= len(self):
                raise StopIteration
            obj = self.get_item(key)
            options = self.config["options"]

            if options.get("values_iterator") == True:
                data = obj.data
                fdata = OrderedDict()
                for k in self.config["values"]:
                    value = recur_accessor(obj, k)
                    fdata[k] = value
                data = fdata
                if options.get("values_list", False):
                    data = tuple(data[k] for k, v in data.items())
                    if len(self.config["values"]) == 1 and options.get(
                        "values_list_flat", False
                    ):
                        data = data[0]
                return data
            else:
                return obj
