# coding: utf-8

import pprint
import re

import six





class Tag:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'key': 'str',
        'value': 'str'
    }

    attribute_map = {
        'key': 'key',
        'value': 'value'
    }

    def __init__(self, key=None, value=None):
        """Tag - a model defined in huaweicloud sdk"""
        
        

        self._key = None
        self._value = None
        self.discriminator = None

        self.key = key
        if value is not None:
            self.value = value

    @property
    def key(self):
        """Gets the key of this Tag.

        键。最大长度36个unicode字符。 key不能为空。不能包含“=”,“*”,“<”,“>”,“\\”,“,”,“|”,“/”，且首尾字符不能为空格。

        :return: The key of this Tag.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Tag.

        键。最大长度36个unicode字符。 key不能为空。不能包含“=”,“*”,“<”,“>”,“\\”,“,”,“|”,“/”，且首尾字符不能为空格。

        :param key: The key of this Tag.
        :type: str
        """
        self._key = key

    @property
    def value(self):
        """Gets the value of this Tag.

        值。每个值最大长度43个unicode字符，可以为空字符串。 不能包含“=”,“*”,“<”,“>”,“\\”,“,”,“|”,“/”，且首尾字符不能为空格。

        :return: The value of this Tag.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Tag.

        值。每个值最大长度43个unicode字符，可以为空字符串。 不能包含“=”,“*”,“<”,“>”,“\\”,“,”,“|”,“/”，且首尾字符不能为空格。

        :param value: The value of this Tag.
        :type: str
        """
        self._value = value

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
        if not isinstance(other, Tag):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
