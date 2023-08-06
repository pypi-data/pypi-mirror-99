# coding: utf-8

import pprint
import re

import six





class NameServersResp:


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
        'region': 'str',
        'ns_records': 'list[NsRecords]'
    }

    attribute_map = {
        'type': 'type',
        'region': 'region',
        'ns_records': 'ns_records'
    }

    def __init__(self, type=None, region=None, ns_records=None):
        """NameServersResp - a model defined in huaweicloud sdk"""
        
        

        self._type = None
        self._region = None
        self._ns_records = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if region is not None:
            self.region = region
        if ns_records is not None:
            self.ns_records = ns_records

    @property
    def type(self):
        """Gets the type of this NameServersResp.

        待查询名称服务器的类型。  取值范围: public, private。  如果为空，表示查询所有类型的名称服务器。 如果为public，表示查询公网的名称服务器。  如果为private，表示查询内网的名称服务器。

        :return: The type of this NameServersResp.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this NameServersResp.

        待查询名称服务器的类型。  取值范围: public, private。  如果为空，表示查询所有类型的名称服务器。 如果为public，表示查询公网的名称服务器。  如果为private，表示查询内网的名称服务器。

        :param type: The type of this NameServersResp.
        :type: str
        """
        self._type = type

    @property
    def region(self):
        """Gets the region of this NameServersResp.

        待查询的region ID。  当查询公网的名称服务器时，此处不填。

        :return: The region of this NameServersResp.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this NameServersResp.

        待查询的region ID。  当查询公网的名称服务器时，此处不填。

        :param region: The region of this NameServersResp.
        :type: str
        """
        self._region = region

    @property
    def ns_records(self):
        """Gets the ns_records of this NameServersResp.


        :return: The ns_records of this NameServersResp.
        :rtype: list[NsRecords]
        """
        return self._ns_records

    @ns_records.setter
    def ns_records(self, ns_records):
        """Sets the ns_records of this NameServersResp.


        :param ns_records: The ns_records of this NameServersResp.
        :type: list[NsRecords]
        """
        self._ns_records = ns_records

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
        if not isinstance(other, NameServersResp):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
