"""Queenbee utility functions."""
import hashlib
import json
from typing import List, Dict

import yaml
from pydantic import BaseModel as PydanticBaseModel
from pydantic import validator, Field, constr

from .parser import parse_file
from .variable import get_ref_variable


# set up yaml.dump to keep the order of the input dictionary
# from https://stackoverflow.com/a/31609484/4394669
def _keep_name_order_in_yaml():
    represent_dict_order = \
        lambda self, data:  self.represent_mapping(
            'tag:yaml.org,2002:map', data.items())
    yaml.add_representer(dict, represent_dict_order)


_keep_name_order_in_yaml()


class BaseModelNoType(PydanticBaseModel):
    """BaseModel with functionality to return the object as a yaml string.

    This BaseModel does not enforce adding a type. This is useful for subclasses in
    extensions.
    """

    def yaml(self, exclude_unset=False, **kwargs):
        """Get a YAML string from the model

        Keyword Arguments:
            exclude_unset {bool} -- Boolean toggle to add or remove any unset/None values
            (default: {False})

        Returns:
            str -- A yaml string representing the model
        """
        return yaml.dump(
            json.loads(self.json(by_alias=True,
                                 exclude_unset=exclude_unset, **kwargs)),
            default_flow_style=False
        )

    def to_dict(self, exclude_unset=False, by_alias=True, **kwargs):
        """Get a dictionary from the model

        Keyword Arguments:
            exclude_unset {bool} -- Boolean toggle to add or remove any unset/None values
                (default: {False})
            by_alias {bool} -- Boolean toggle to use attribute alias or attribute names
                as key (default: {True})

        Returns:
            dict -- A python dictionary representing the model
        """
        return json.loads(self.json(by_alias=by_alias, exclude_unset=exclude_unset, **kwargs))

    def to_json(self, filepath, indent=None, **kwargs):
        """Write a JSON file of the model

        Arguments:
            filepath {str} -- Path to the file to be written

        Keyword Arguments:
            indent {int} -- indent amount (default: {None})
        """
        with open(filepath, 'w') as file:
            file.write(self.json(by_alias=True, exclude_unset=False,
                                 indent=indent, **kwargs))

    def to_yaml(self, filepath, exclude_unset=False, **kwargs):
        """Write a YAML file of the model

        Arguments:
            filepath {str} -- Path to the file to be written

        Keyword Arguments:
            exclude_unset {bool} -- Boolean toggle to add or remove any unset/None values
            (default: {False})
        """
        content = self.yaml(exclude_unset=exclude_unset, **kwargs)

        with open(filepath, 'w') as out_file:
            out_file.write(content)

    @classmethod
    def from_file(cls, filepath):
        """Create a model from a file

        Arguments:
            filepath {str} -- Path to the file to read (can be JSON or YAML)

        Returns:
            cls -- An instance of the pydantic class
        """
        data = parse_file(filepath)
        return cls.parse_obj(data)

    def __repr__(self):
        return self.yaml()

    @property
    def __hash__(self):
        """Return a model hash

        Returns:
            str -- A hash/digest of the model
        """
        return hashlib.sha256(
            self.json(by_alias=True, exclude_unset=False).encode('utf-8')
        ).hexdigest()

    def _referenced_values(self, var_names: List[str]) -> Dict[str, List[str]]:
        """Get all referenced values specified by var name

        Arguments:
            var_names {List[str]} -- List of class attribute names to check for
                referenced values

        Returns:
            Dict[str, List[str]] -- A dictionary where each key corresponds to a class
                attribute indexing a list of referenced values
        """
        ref_values = {}

        for name in var_names:
            value = getattr(self, name, None)

            if isinstance(value, str):
                ref_var = get_ref_variable(value)

                if ref_var != []:
                    ref_values[name] = ref_var

        return ref_values


class BaseModel(BaseModelNoType):
    """BaseModel with functionality to return the object as a yaml string."""

    type: constr(regex='^BaseModel$') = 'BaseModel'

    annotations: Dict[str, str] = Field(
        None,
        description='An optional dictionary to add annotations to inputs. These '
        'annotations will be used by the client side libraries.'
    )

    @validator('type')
    def ensure_type_match(cls, v):
        name = cls.__name__
        if name != v:
            raise ValueError(
                f'The value for "type" ({v}) must be the same as class name ({name}). '
                'In most cases, this is the result of not adding the type field to the '
                f'Pydantic object. In this case: {name}'
            )
        return v

    @validator('annotations', always=True)
    def replace_none_value(cls, v):
        return {} if not v else v
