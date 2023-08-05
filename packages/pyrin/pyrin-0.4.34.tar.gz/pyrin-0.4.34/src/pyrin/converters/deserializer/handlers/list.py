# -*- coding: utf-8 -*-
"""
deserializer handlers list module.
"""

import re

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import DeserializerBase, \
    StringPatternDeserializerBase


@deserializer()
class ListDeserializer(DeserializerBase):
    """
    list deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of ListDeserializer.

        :keyword bool internal: specifies that this deserializer is internal.
                                internal deserializers will not be used for
                                deserializing client inputs.
                                defaults to False if not provided.
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes every possible value available in input list.

        gets a new deserialized list, leaving the input unchanged.

        :param list value: value that should be deserialized.

        :rtype: list
        """

        result = []
        for item in value:
            result.append(deserializer_services.deserialize(item, **options))

        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this deserializer.

        which could deserialize values from this type.

        :rtype: type[list]
        """

        return list


@deserializer()
class StringListDeserializer(StringPatternDeserializerBase):
    """
    string list deserializer class.

    note that this deserializer could only handle lists with single depth.
    meaning that nested lists are not supported. and also nested tuples or
    dictionaries or sets or any other collections are not supported and
    stops deserialization.
    for example: [1, (2, 4), [5, 4]] will not be deserialized.
    """

    # default min for this deserializer is 2 because
    # it should at least has [ and ] at both ends.
    DEFAULT_MIN = 2

    # matches a list inside string, all of these values will be matched.
    # example: [], [1], [1,], [1,2], [1,2,]
    # it won't accept nested collections, all of these values won't match.
    # example: [()], [1, {2: 4}, [2,3]]
    LIST_REGEX = re.compile(r'^\[\]$|^\[[^\(\){}\[\]]+(,[^\(\){}\[\]]+)*\]$')

    def __init__(self, **options):
        """
        creates an instance of StringListDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  patterns and their min and
                                                                  max length for list
                                                                  deserialization.

        :note accepted_formats: list[tuple[Pattern format, int min_length, int max_length]]

        :keyword bool internal: specifies that this deserializer is internal.
                                internal deserializers will not be used for
                                deserializing client inputs.
                                defaults to False if not provided.
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.

        :param str value: value to be deserialized.

        :keyword Pattern matching_pattern: the pattern that has matched the value.

        :rtype: list
        """

        # removing the first '[' and last ']' from value.
        value = value[1:-1]
        items = value.split(',')
        temp_list = []
        for item in items:
            if len(item.strip()) > 0:
                temp_list.append(item.strip())

        return deserializer_services.deserialize(temp_list, **options)

    @property
    def default_formats(self):
        """
        gets default accepted patterns that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.LIST_REGEX, self.UNDEF_LENGTH, self.UNDEF_LENGTH)]
