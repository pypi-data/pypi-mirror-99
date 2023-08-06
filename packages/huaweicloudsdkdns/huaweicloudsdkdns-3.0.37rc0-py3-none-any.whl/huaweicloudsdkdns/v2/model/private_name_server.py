# coding: utf-8

import pprint
import re

import six





class PrivateNameServer:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'priority': 'int',
        'address': 'str'
    }

    attribute_map = {
        'priority': 'priority',
        'address': 'address'
    }

    def __init__(self, priority=None, address=None):
        """PrivateNameServer - a model defined in huaweicloud sdk"""
        
        

        self._priority = None
        self._address = None
        self.discriminator = None

        if priority is not None:
            self.priority = priority
        if address is not None:
            self.address = address

    @property
    def priority(self):
        """Gets the priority of this PrivateNameServer.

        优先级。如果priority的值为“1”，表示会第一个采用该域名服务器进行解析。

        :return: The priority of this PrivateNameServer.
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this PrivateNameServer.

        优先级。如果priority的值为“1”，表示会第一个采用该域名服务器进行解析。

        :param priority: The priority of this PrivateNameServer.
        :type: int
        """
        self._priority = priority

    @property
    def address(self):
        """Gets the address of this PrivateNameServer.

        DNS服务器地址。

        :return: The address of this PrivateNameServer.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this PrivateNameServer.

        DNS服务器地址。

        :param address: The address of this PrivateNameServer.
        :type: str
        """
        self._address = address

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
        if not isinstance(other, PrivateNameServer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
