# -*- coding: utf-8 -*-
"""
validator interface module.
"""

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import CoreObject


class AbstractValidatorBase(CoreObject):
    """
    abstract validator base class.

    all application validators must be subclassed from this.
    """

    @abstractmethod
    def validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        it returns the same or fixed value.

        :param object | list[object] value: value to be validated.

        :keyword bool for_update: specifies that this field is being
                                  validated for update operation.
                                  defaults to False if not provided.

        :keyword bool for_find: specifies that validation is for find operation.
                                defaults to False if not provided.
                                if this validator is for find and `for_find=False`
                                is provided, no validation will be done.

        :raises CoreNotImplementedError: core not implemented error.
        :raises ValidationError: validation error.

        :returns: object | list[object]
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def name(self):
        """
        gets the name of this validator.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def domain(self):
        """
        gets the domain of this validator.

        domain is the type of a BaseEntity subclass that
        this validator validates a value of it.
        if a validator is not specific to an entity, then
        domain could be a unique string name.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type[BaseEntity] | str
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def for_find(self):
        """
        gets a value indicating that this validator should only be used on validation for find.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
