# coding: utf-8

import pprint
import re

import six





class CreateRecordSetWithLineRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'zone_id': 'str',
        'body': 'CreateRecordSetWithLineReq'
    }

    attribute_map = {
        'zone_id': 'zone_id',
        'body': 'body'
    }

    def __init__(self, zone_id=None, body=None):
        """CreateRecordSetWithLineRequest - a model defined in huaweicloud sdk"""
        
        

        self._zone_id = None
        self._body = None
        self.discriminator = None

        self.zone_id = zone_id
        if body is not None:
            self.body = body

    @property
    def zone_id(self):
        """Gets the zone_id of this CreateRecordSetWithLineRequest.


        :return: The zone_id of this CreateRecordSetWithLineRequest.
        :rtype: str
        """
        return self._zone_id

    @zone_id.setter
    def zone_id(self, zone_id):
        """Sets the zone_id of this CreateRecordSetWithLineRequest.


        :param zone_id: The zone_id of this CreateRecordSetWithLineRequest.
        :type: str
        """
        self._zone_id = zone_id

    @property
    def body(self):
        """Gets the body of this CreateRecordSetWithLineRequest.


        :return: The body of this CreateRecordSetWithLineRequest.
        :rtype: CreateRecordSetWithLineReq
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this CreateRecordSetWithLineRequest.


        :param body: The body of this CreateRecordSetWithLineRequest.
        :type: CreateRecordSetWithLineReq
        """
        self._body = body

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
        if not isinstance(other, CreateRecordSetWithLineRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
