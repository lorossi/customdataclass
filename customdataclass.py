"""This module contains a custom dataclass object.

It does work kinda good.
"""

from __future__ import annotations

import builtins
from typing import Any


class Dataclass:
    """Custom dataclass.

    The real reason is that I didn't really like the way dataclasses work,
    and I wanted to have a better control over the attributes.
    """

    _frozen = False
    _frozen_after_init = True
    _enforce_types = True

    def __init__(self, **kwargs) -> Dataclass:
        """Create a new Dataclass.

        Raises:
            AttributeError: an invalid attribute is passed
            AttributeError: an attribute is missing in kwargs.
            TypeError: a value is not of the correct type.
        """
        if not kwargs:
            return

        self._frozen = False

        for k in kwargs.keys():
            if k not in self.__class_attributes__:
                raise AttributeError(f"{k} is not a valid attribute")

        for k, v in self.__class_attributes__.items():
            if k not in kwargs:
                raise AttributeError(f"Missing {k} in kwargs")

            if self._enforce_types:
                # serialized format don't support tuple and set (they convert \
                # both to list), so we need to convert them back IMPLICITLY
                if self._checkDeserializedIterator(kwargs[k], v):
                    # convert to tuple or set
                    if v == tuple:
                        kwargs[k] = tuple(kwargs[k])
                    elif v == set:
                        kwargs[k] = set(kwargs[k])

                # serialised format don't support classes (they convert them to \
                # dict), so we need to convert them back IMPLICITLY
                if self._checkDeserializedClass(kwargs[k], v):
                    kwargs[k] = v(**kwargs[k])

                # check that the type is correct
                try:
                    valid_type = isinstance(kwargs[k], v)
                except KeyError:
                    valid_type = kwargs[v].__class__.__name__ == v.__name__
                except Exception:
                    valid_type = False

                if not valid_type and not isinstance(kwargs[k], v):
                    raise TypeError(f"{k} should be {v}, not {type(kwargs[k])}")

            setattr(self, k, kwargs[k])

        self._frozen = self._frozen_after_init

    def _checkDeserializedIterator(self, value: list[Any], valid_type: type) -> bool:
        """Check if the value is a valid iterator.

        Args:
            value (list[Any]): value to check
            valid_type (type): type of the value

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        if not isinstance(value, list):
            return False

        return valid_type in (set, tuple)

    def _checkDeserializedClass(self, value: dict, valid_type: type) -> bool:
        """Check if the value is a valid class.

        Args:
            value (dict): value to check
            valid_type (type): type of the value

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        if not isinstance(value, dict):
            return False

        return issubclass(valid_type, Dataclass)

    def __init_subclass__(
        cls,
        enforce_types: bool = True,
        frozen: bool = True,
        allow_list_for_tuple: bool = False,
        **kwargs,
    ) -> None:
        """Initialize the subclass.

        Args:
            enforce_types (bool, optional): If True, the types of the attributes \
                are enforced.
            frozen (bool, optional): If True, attributes cannot be changed after \
                initialization. Defaults to True.
        """
        cls._enforce_types = enforce_types
        cls._frozen_after_init = frozen
        cls._allow_list_for_iters = allow_list_for_tuple
        super().__init_subclass__(**kwargs)

    def __setattr__(self, key: str, value):
        """Set an attribute.

        Args:
            key (str): name of the attribute
            value (any): value of the attribute

        Raises:
            AttributeError: _description_
            AttributeError: _description_
        """
        if self._frozen:
            raise AttributeError(
                f"Can't set {key}. {self.__class__.__name__} is immutable."
            )

        if key not in self.__class_attributes__ and key != "_frozen":
            raise AttributeError(f"Can't set {key}. {key} is not a valid attribute")

        super().__setattr__(key, value)

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Returns:
            str
        """
        parentheses = {
            "tuple": ("(", ")"),
            "list": ("[", "]"),
            "set": ("{", "}"),
            "dict": ("{", "}"),
        }

        s = f"{self.__class__.__name__}("

        for k, v in self.__clean_dict__.items():
            s += f"{k}="
            if isinstance(v, str):
                s += f'"{v}"'
            elif isinstance(v, (list, tuple, set, dict)):
                s += parentheses[v.__class__.__name__][0]
                if isinstance(v, dict):
                    s += ", ".join(f'"{k}": {v}' for k, v in v.items())
                else:
                    s += f"{', '.join(str(i) for i in v)}"

                s += parentheses[v.__class__.__name__][1]
            else:
                s += str(v)

            s += ", "

        s = s[:-2] + ")"
        return s

    def __str__(self) -> str:
        """Return a string representation of the object.

        Returns:
            str
        """
        return self.__repr__()

    def __eq__(self, other) -> bool:
        """Compare two objects.

        Args:
            other (any): object to compare

        Returns:
            bool
        """
        if not isinstance(other, self.__class__):
            return False

        for k in self.__class_attributes__:
            if getattr(self, k) != getattr(other, k):
                return False

        return True

    def __hash__(self) -> int:
        """Return the hash of the object.

        Returns:
            int
        """
        ordered = sorted(self.__clean_dict__.items())
        return hash(tuple(ordered))

    def __contains__(self, item) -> bool:
        """Check if the object contains an item.

        This is used to check if an attribute exists via the \
        built-in `in` operator.

        Args:
            item (any): item to check

        Returns:
            bool
        """
        return item in self.__clean_dict__.keys()

    def __iter__(self):
        """Return an iterator for the object.

        Returns:
            iterator
        """
        return iter(self.__clean_dict__.items())

    @property
    def __class_attributes__(self) -> dict[str, type]:
        """Return all the attributes of the class and their type.

        Returns:
            dict
        """
        # sometimes the types are strings and not class types
        # i don't understand why, I gotta look into it
        return {
            k: v if isinstance(v, type) else getattr(builtins, v)
            for k, v in self.__class__.__annotations__.items()
            if not k.startswith("_")
        }

    @property
    def __clean_dict__(self) -> dict:
        """Return a dictionary with all the attributes of the object, \
            except for the ones starting with an underscore (private).

        Returns:
            dict
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @property
    def to_dict(self) -> dict:
        """Return a dictionary with all the attributes of the object.

        Returns:
            dict
        """

        def iterable_type(var: any) -> type:
            if isinstance(var, (list, tuple, set)):
                return var.__class__

            return None

        d = {}

        for k, v in self.__clean_dict__.items():
            if isinstance(k, Dataclass):
                key = k.to_dict
            else:
                key = k

            if t := iterable_type(v):
                # handle recursive lists
                d[key] = t(i.to_dict if isinstance(i, Dataclass) else i for i in v)
            elif isinstance(v, Dataclass):
                # handle recursive dataclasses
                d[key] = v.to_dict
            else:
                # simple types
                d[key] = v

        return d

    @property
    def to_json(self) -> str:
        """
        Return a json representation of the object. \
        Attributes are recursively converted to json.

        Returns:
            str
        """
        dict_data = self.to_dict

        # all the sets and tuples are converted to lists
        # because json doesn't support them
        for k, v in dict_data.items():
            if isinstance(v, (set, tuple)):
                dict_data[k] = list(v)

        try:
            import ujson
        except ImportError:
            import json as ujson

        return ujson.dumps(dict_data)

    @property
    def to_toml(self) -> str:
        """Return a toml representation of the object.

        Returns:
            str
        """
        try:
            import toml
        except ImportError:
            raise ImportError(
                "toml is not installed. Install it with command pip install toml."
            )
        return toml.dumps(self.to_dict)

    @property
    def to_json_pretty(self) -> str:
        """Return a pretty json representation of the object.

        Returns:
            str
        """
        try:
            import ujson
        except ImportError:
            import json as ujson

        return ujson.dumps(self.to_dict, indent=4, sort_keys=True)

    @property
    def to_yaml(self) -> str:
        """Return a yaml representation of the object.

        Returns:
            str
        """
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "yaml is not installed. Install it with command pip install pyyaml."
            )
        return yaml.dump(self.to_dict)

    @property
    def attributes(self) -> list:
        """Return a list of all the attributes of the class.

        Returns:
            list
        """
        return list(self.__class_attributes__.keys())

    @classmethod
    def from_json(cls, json_string: str):
        """Create an object from a json string.

        Args:
            json_string (str): json string

        Returns:
            object
        """
        try:
            import ujson
        except ImportError:
            import json as ujson

        return cls(**ujson.loads(json_string))

    @classmethod
    def from_toml(cls, toml_string: str):
        """Create an object from a toml string.

        Args:
            toml_string (str): toml string

        Returns:
            object
        """
        try:
            import toml
        except ImportError:
            raise ImportError(
                "toml is not installed. Install it with command pip install toml."
            )
        return cls(**toml.loads(toml_string))

    @classmethod
    def from_yaml(cls, yaml_string: str):
        """Create an object from a yaml string.

        Args:
            yaml_string (str): yaml string

        Returns:
            object
        """
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "yaml is not installed. Install it with command pip install pyyaml."
            )
        return cls(**yaml.load(yaml_string, Loader=yaml.FullLoader))

    @classmethod
    def from_dict(cls, d: dict):
        """Create an object from a dictionary.

        Args:
            d (dict): dictionary

        Returns:
            object
        """
        return cls(**d)
