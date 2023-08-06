# coding: utf-8

import pprint
import re

import six





class CreatePtrReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'ptrdname': 'str',
        'description': 'str',
        'ttl': 'int',
        'enterprise_project_id': 'str',
        'tags': 'list[Tag]'
    }

    attribute_map = {
        'ptrdname': 'ptrdname',
        'description': 'description',
        'ttl': 'ttl',
        'enterprise_project_id': 'enterprise_project_id',
        'tags': 'tags'
    }

    def __init__(self, ptrdname=None, description=None, ttl=None, enterprise_project_id=None, tags=None):
        """CreatePtrReq - a model defined in huaweicloud sdk"""
        
        

        self._ptrdname = None
        self._description = None
        self._ttl = None
        self._enterprise_project_id = None
        self._tags = None
        self.discriminator = None

        self.ptrdname = ptrdname
        if description is not None:
            self.description = description
        if ttl is not None:
            self.ttl = ttl
        if enterprise_project_id is not None:
            self.enterprise_project_id = enterprise_project_id
        if tags is not None:
            self.tags = tags

    @property
    def ptrdname(self):
        """Gets the ptrdname of this CreatePtrReq.

        PTR记录对应的域名。

        :return: The ptrdname of this CreatePtrReq.
        :rtype: str
        """
        return self._ptrdname

    @ptrdname.setter
    def ptrdname(self, ptrdname):
        """Sets the ptrdname of this CreatePtrReq.

        PTR记录对应的域名。

        :param ptrdname: The ptrdname of this CreatePtrReq.
        :type: str
        """
        self._ptrdname = ptrdname

    @property
    def description(self):
        """Gets the description of this CreatePtrReq.

        对PTR记录的描述。

        :return: The description of this CreatePtrReq.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreatePtrReq.

        对PTR记录的描述。

        :param description: The description of this CreatePtrReq.
        :type: str
        """
        self._description = description

    @property
    def ttl(self):
        """Gets the ttl of this CreatePtrReq.

        PTR记录在本地DNS服务器的缓存时间，缓存时间越长更新生效越慢，以秒为单位。取值范围：1～2147483647

        :return: The ttl of this CreatePtrReq.
        :rtype: int
        """
        return self._ttl

    @ttl.setter
    def ttl(self, ttl):
        """Sets the ttl of this CreatePtrReq.

        PTR记录在本地DNS服务器的缓存时间，缓存时间越长更新生效越慢，以秒为单位。取值范围：1～2147483647

        :param ttl: The ttl of this CreatePtrReq.
        :type: int
        """
        self._ttl = ttl

    @property
    def enterprise_project_id(self):
        """Gets the enterprise_project_id of this CreatePtrReq.

        反向解析关联的企业项目ID，长度不超过36个字符。

        :return: The enterprise_project_id of this CreatePtrReq.
        :rtype: str
        """
        return self._enterprise_project_id

    @enterprise_project_id.setter
    def enterprise_project_id(self, enterprise_project_id):
        """Sets the enterprise_project_id of this CreatePtrReq.

        反向解析关联的企业项目ID，长度不超过36个字符。

        :param enterprise_project_id: The enterprise_project_id of this CreatePtrReq.
        :type: str
        """
        self._enterprise_project_id = enterprise_project_id

    @property
    def tags(self):
        """Gets the tags of this CreatePtrReq.

        资源标签。

        :return: The tags of this CreatePtrReq.
        :rtype: list[Tag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this CreatePtrReq.

        资源标签。

        :param tags: The tags of this CreatePtrReq.
        :type: list[Tag]
        """
        self._tags = tags

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
        if not isinstance(other, CreatePtrReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
