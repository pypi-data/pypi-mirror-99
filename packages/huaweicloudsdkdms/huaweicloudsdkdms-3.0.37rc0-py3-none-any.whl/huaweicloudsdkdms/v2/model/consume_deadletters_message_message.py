# coding: utf-8

import pprint
import re

import six





class ConsumeDeadlettersMessageMessage:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'body': 'object',
        'attributes': 'object'
    }

    attribute_map = {
        'body': 'body',
        'attributes': 'attributes'
    }

    def __init__(self, body=None, attributes=None):
        """ConsumeDeadlettersMessageMessage - a model defined in huaweicloud sdk"""
        
        

        self._body = None
        self._attributes = None
        self.discriminator = None

        if body is not None:
            self.body = body
        if attributes is not None:
            self.attributes = attributes

    @property
    def body(self):
        """Gets the body of this ConsumeDeadlettersMessageMessage.

        消息体的内容。

        :return: The body of this ConsumeDeadlettersMessageMessage.
        :rtype: object
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this ConsumeDeadlettersMessageMessage.

        消息体的内容。

        :param body: The body of this ConsumeDeadlettersMessageMessage.
        :type: object
        """
        self._body = body

    @property
    def attributes(self):
        """Gets the attributes of this ConsumeDeadlettersMessageMessage.

        属性的列表。

        :return: The attributes of this ConsumeDeadlettersMessageMessage.
        :rtype: object
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """Sets the attributes of this ConsumeDeadlettersMessageMessage.

        属性的列表。

        :param attributes: The attributes of this ConsumeDeadlettersMessageMessage.
        :type: object
        """
        self._attributes = attributes

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
        if not isinstance(other, ConsumeDeadlettersMessageMessage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
