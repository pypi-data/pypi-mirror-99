# coding: utf-8

import pprint
import re

import six





class Constraint:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'type': 'str',
        'value': 'str',
        'errormsg': 'str'
    }

    attribute_map = {
        'type': 'type',
        'value': 'value',
        'errormsg': 'errormsg'
    }

    def __init__(self, type=None, value=None, errormsg=None):
        """Constraint - a model defined in huaweicloud sdk"""
        
        

        self._type = None
        self._value = None
        self._errormsg = None
        self.discriminator = None

        self.type = type
        self.value = value
        self.errormsg = errormsg

    @property
    def type(self):
        """Gets the type of this Constraint.

        校验规则类型

        :return: The type of this Constraint.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Constraint.

        校验规则类型

        :param type: The type of this Constraint.
        :type: str
        """
        self._type = type

    @property
    def value(self):
        """Gets the value of this Constraint.

        校验规则

        :return: The value of this Constraint.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Constraint.

        校验规则

        :param value: The value of this Constraint.
        :type: str
        """
        self._value = value

    @property
    def errormsg(self):
        """Gets the errormsg of this Constraint.

        校验失败描述

        :return: The errormsg of this Constraint.
        :rtype: str
        """
        return self._errormsg

    @errormsg.setter
    def errormsg(self, errormsg):
        """Sets the errormsg of this Constraint.

        校验失败描述

        :param errormsg: The errormsg of this Constraint.
        :type: str
        """
        self._errormsg = errormsg

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Constraint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
