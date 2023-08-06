"""
Module provides access to entity types that can be parsed to obtain numeric values.

Import classes:
    - NumericalEntity
"""

from typing import Any, Callable, Dict, List

import attr

from dialogy import constants
from dialogy.types.entity import BaseEntity


@attr.s
class NumericalEntity(BaseEntity):
    """
    Numerical Entity Type

    Use this type for handling all entities that can be parsed to obtain:
    - numbers
    - date
    - time
    - datetime

    Attributes:
        - `dim` dimension of the entity from duckling parser
        - `type` is the type of the entity which can have values in ["value", "interval"]
    """

    origin = attr.ib(
        type=str, default="value", validator=attr.validators.instance_of(str)
    )
    __properties_map = constants.BASE_ENTITY_PROPS
