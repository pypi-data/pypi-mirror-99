#!/usr/bin/env python3
# coding: utf-8
# Copyright (c) Modos Team, 2020

import re
from typing import Dict, Any, Optional, Tuple, List, Union, Callable

import pymongo
from dateparser import parse


class MongoDBQueriesManagerBaseError(Exception):
    """ Base MongoDBQueriesManager errors. """


class SkipError(MongoDBQueriesManagerBaseError):
    """ Raised when skip is negative / bad value."""


class LimitError(MongoDBQueriesManagerBaseError):
    """ Raised when limit is negative / bad value. """


class ListOperatorError(MongoDBQueriesManagerBaseError):
    """ Raised list operator was not possible. """


class FilterError(MongoDBQueriesManagerBaseError):
    """ Raised when parse filter method fail to find a valid match. """


class TextOperatorError(MongoDBQueriesManagerBaseError):
    """ Raised when parse text operator contain an empty string. """


class CustomCasterFail(MongoDBQueriesManagerBaseError):
    """ Raised when a custom cast fail. """


class MongoDBQueriesManager:
    """ MongoDBQueriesManager class.

    This class contain all method to convert string query to MongoDB query

    Attributes:
        mongodb_operator (Dict[str, str]): MongoDB operator, used to convert query operators into MongoDB operators.
        regex_dict (Dict[Union[str, re.Pattern], Any]): Contain all typing for cast into right format.
    """

    mongodb_operator: Dict[str, str] = {
        '=': '$eq',
        '!=': '$ne',
        '>': '$gt',
        '>=': '$gte',
        '<': '$lt',
        '<=': '$lte',
        '!': '$exists',
        '': '$exists'
    }

    regex_dict: Dict[Union[str, re.Pattern], Any] = {
        re.compile(r"^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$"): float,
        re.compile(r"^[-+]?\d+$"): int,
        re.compile(r"^[12]\d{3}(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)(T|"
                   r" )?(([01][0-9]|2[0-3]):[0-5]\d(:[0-5]\d(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?)?$"):
            lambda date: parse(date, languages=['fr', 'en']),
        re.compile(r"^\w+(?=(,?,))(?:\1\w+)+$"): lambda list_value: list_value.split(','),
        re.compile(r"\/((?![*+?])(?:[^\r\n\[/\\]|\\.|\[(?:[^\r\n\]\\]|\\.)*\])+)"
                   r"\/((?:g(?:im?|mi?)?|i(?:gm?|mg?)?|m(?:gi?|ig?)?)?)"): re.compile,
        "true": lambda boolean: True,
        "false": lambda boolean: False,
        "null": lambda null: None,
        "none": lambda none: None,
    }

    custom_cast_dict: Optional[Dict[str, Callable]]

    def __init__(self, casters: Optional[Dict[str, Callable]] = None) -> None:
        self.custom_cast_dict = casters

    def filter_logic(self, filter_params: str) -> Dict[str, Any]:
        """ Build filter

        Args:
            filter_params (str): Filter params from url query (ie, 'name=John')

        Returns:
            Dict[str, Any]: Dictionary with MongoDB filter
        """
        operator = self.find_operator(filter_params=filter_params)

        if operator != '':
            try:
                key, value = filter_params.split(operator)
            except ValueError as err:
                raise FilterError(f'Fail to split filter {filter_params} with operator {operator}') from err
        else:
            key, value = '', filter_params

        value = self.cast_value_logic(value)

        # $eq logic
        if not isinstance(value, list) and operator == '=':
            return {key: value}

        # $in, $nin, $exists logic
        if isinstance(value, list):
            # Cast list items
            casted_list_item = list()
            for item in value:
                casted_list_item.append(self.cast_value_logic(item))

            if operator == '=':
                return {key: {"$in": casted_list_item}}
            if operator == '!=':
                return {key: {"$nin": casted_list_item}}
            raise ListOperatorError('List operator not found')

        # $exists logic
        if operator in ['', '!']:
            return {value: {self.mongodb_operator[operator]: bool(operator == '')}}

        # $gt, $gte, $lt, $lte, $ne, logic
        return {key: {self.mongodb_operator[operator]: value}}

    def cast_value_logic(self, value: str) -> Any:
        """ Cast value into right type

        Args:
            value (str): Value to cast

        Returns:
            Any: Casted value
        """
        if self.custom_cast_dict is not None:
            for rule, func in self.custom_cast_dict.items():
                if value.startswith(f'{rule}(') and value.endswith(')'):
                    try:
                        casted_value = func(value.replace(f'{rule}(', '')[:-1])
                    except Exception as err:
                        raise CustomCasterFail(f'Fail to cast {value} with caster {rule}') from err

                    return casted_value

        for regex, cast in self.regex_dict.items():
            if isinstance(regex, re.Pattern):
                if regex.match(value):
                    return cast(value)
            else:
                if regex == value.lower():
                    return cast(value)
        return value

    @staticmethod
    def find_operator(filter_params: str) -> str:
        """Return the right operator

        Args:
            filter_params (str): Filter params (ie, 'name=John'):

        Returns:
            str: Return operator
        """
        for operator in ['<=', '>=', '!=', '=', '>', '<', '!']:
            if filter_params.find(operator) > -1:
                return operator
        return ''

    @staticmethod
    def sort_logic(sort_params: str) -> Optional[List[Tuple]]:
        """ Convert query sort value into MongoDB format

        Notes:
            Work if `sort=` into url query

        Args:
            sort_params (str): Sort param from url query (ie, 'sort=-created_at')

        Returns:
            Optional[List[Tuple]]: Tuple with MongoDB sort info
        """
        sort_params_final: List[Tuple] = list()
        value = sort_params.split('=')[1]

        if value:
            for param in value.split(','):
                if param.startswith('+'):
                    sort_params_final.append((param[1:], pymongo.ASCENDING))
                elif param.startswith('-'):
                    sort_params_final.append((param[1:], pymongo.DESCENDING))
                else:
                    sort_params_final.append((param, pymongo.ASCENDING))
            return sort_params_final
        return None

    def text_operator_logic(self, text_param: str) -> str:
        """ Convert text query value into MongoDB format

        Args:
            text_param (str): Text param from url query (ie, '$text=java shop -coffee')

        Returns:
            int: Limit integer value
        """
        if text_param == "$text=":
            raise TextOperatorError('Bad $text value')

        return self.cast_value_logic(text_param.split('=')[1])

    @staticmethod
    def limit_logic(limit_param: str) -> int:
        """ Convert query limit value into MongoDB format

        Args:
            limit_param (str): Limit param from url query (ie, 'limit=5')

        Returns:
            int: Limit integer value
        """
        if limit_param == 'limit=':
            return 0

        try:
            limit_value = int(limit_param.split('=')[1])
        except ValueError as err:
            raise LimitError('Bad limit value') from err

        if limit_value < 0:
            raise LimitError('Negative limit value')

        return limit_value

    @staticmethod
    def skip_logic(skip_param: str) -> int:
        """ Convert query skip value into MongoDB format

        Args:
            skip_param (str): Skip param from url query (ie, 'limit=5')

        Returns:
            int: Skip integer value
        """

        if skip_param == 'skip=':
            return 0

        try:
            skip_value = int(skip_param.split('=')[1])
        except ValueError as err:
            raise SkipError('Bad skip value') from err

        if skip_value < 0:
            raise SkipError('Negative skip value')

        return skip_value
