# coding: utf-8

import pprint
import re

import six





class UpdateRecordSetReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'name': 'str',
        'description': 'str',
        'type': 'str',
        'ttl': 'int',
        'records': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'type': 'type',
        'ttl': 'ttl',
        'records': 'records'
    }

    def __init__(self, name=None, description=None, type=None, ttl=None, records=None):
        """UpdateRecordSetReq - a model defined in huaweicloud sdk"""
        
        

        self._name = None
        self._description = None
        self._type = None
        self._ttl = None
        self._records = None
        self.discriminator = None

        self.name = name
        if description is not None:
            self.description = description
        self.type = type
        if ttl is not None:
            self.ttl = ttl
        if records is not None:
            self.records = records

    @property
    def name(self):
        """Gets the name of this UpdateRecordSetReq.

        域名，后缀需以zone name结束且为FQDN（即以“.”号结束的完整主机名）。

        :return: The name of this UpdateRecordSetReq.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateRecordSetReq.

        域名，后缀需以zone name结束且为FQDN（即以“.”号结束的完整主机名）。

        :param name: The name of this UpdateRecordSetReq.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """Gets the description of this UpdateRecordSetReq.

        可选配置，对域名的描述。

        :return: The description of this UpdateRecordSetReq.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateRecordSetReq.

        可选配置，对域名的描述。

        :param description: The description of this UpdateRecordSetReq.
        :type: str
        """
        self._description = description

    @property
    def type(self):
        """Gets the type of this UpdateRecordSetReq.

        Record Set的类型。

        :return: The type of this UpdateRecordSetReq.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UpdateRecordSetReq.

        Record Set的类型。

        :param type: The type of this UpdateRecordSetReq.
        :type: str
        """
        self._type = type

    @property
    def ttl(self):
        """Gets the ttl of this UpdateRecordSetReq.

        解析记录在本地DNS服务器的缓存时间，缓存时间越长更新生效越慢，以秒为单位。

        :return: The ttl of this UpdateRecordSetReq.
        :rtype: int
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this UpdateRecordSetReq.

        解析记录在本地DNS服务器的缓存时间，缓存时间越长更新生效越慢，以秒为单位。

        :param ttl: The ttl of this UpdateRecordSetReq.
        :type: int
        """
        self._ttl = ttl

    @property
    def records(self):
        """Gets the records of this UpdateRecordSetReq.

        解析记录的值。不同类型解析记录对应的值的规则不同。

        :return: The records of this UpdateRecordSetReq.
        :rtype: list[str]
        """
        return self._records

    @records.setter
    def records(self, records):
        """Sets the records of this UpdateRecordSetReq.

        解析记录的值。不同类型解析记录对应的值的规则不同。

        :param records: The records of this UpdateRecordSetReq.
        :type: list[str]
        """
        self._records = records

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
        if not isinstance(other, UpdateRecordSetReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
