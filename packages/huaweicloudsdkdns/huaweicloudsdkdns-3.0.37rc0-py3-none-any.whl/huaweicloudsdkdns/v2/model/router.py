# coding: utf-8

import pprint
import re

import six





class Router:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'router_id': 'str',
        'router_region': 'str'
    }

    attribute_map = {
        'router_id': 'router_id',
        'router_region': 'router_region'
    }

    def __init__(self, router_id=None, router_region=None):
        """Router - a model defined in huaweicloud sdk"""
        
        

        self._router_id = None
        self._router_region = None
        self.discriminator = None

        self.router_id = router_id
        if router_region is not None:
            self.router_region = router_region

    @property
    def router_id(self):
        """Gets the router_id of this Router.

        Router(VPC)所属VPC的ID。

        :return: The router_id of this Router.
        :rtype: str
        """
        return self._router_id

    @router_id.setter
    def router_id(self, router_id):
        """Sets the router_id of this Router.

        Router(VPC)所属VPC的ID。

        :param router_id: The router_id of this Router.
        :type: str
        """
        self._router_id = router_id

    @property
    def router_region(self):
        """Gets the router_region of this Router.

        Router(VPC)所在的region。

        :return: The router_region of this Router.
        :rtype: str
        """
        return self._router_region

    @router_region.setter
    def router_region(self, router_region):
        """Sets the router_region of this Router.

        Router(VPC)所在的region。

        :param router_region: The router_region of this Router.
        :type: str
        """
        self._router_region = router_region

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
        if not isinstance(other, Router):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
