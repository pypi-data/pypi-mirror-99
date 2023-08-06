# coding: utf-8

import pprint
import re

import six





class ConsumeMessage:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'message': 'ConsumeMessageMessage',
        'handler': 'str'
    }

    attribute_map = {
        'message': 'message',
        'handler': 'handler'
    }

    def __init__(self, message=None, handler=None):
        """ConsumeMessage - a model defined in huaweicloud sdk"""
        
        

        self._message = None
        self._handler = None
        self.discriminator = None

        if message is not None:
            self.message = message
        if handler is not None:
            self.handler = handler

    @property
    def message(self):
        """Gets the message of this ConsumeMessage.


        :return: The message of this ConsumeMessage.
        :rtype: ConsumeMessageMessage
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ConsumeMessage.


        :param message: The message of this ConsumeMessage.
        :type: ConsumeMessageMessage
        """
        self._message = message

    @property
    def handler(self):
        """Gets the handler of this ConsumeMessage.

        消息handler。

        :return: The handler of this ConsumeMessage.
        :rtype: str
        """
        return self._handler

    @handler.setter
    def handler(self, handler):
        """Sets the handler of this ConsumeMessage.

        消息handler。

        :param handler: The handler of this ConsumeMessage.
        :type: str
        """
        self._handler = handler

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
        if not isinstance(other, ConsumeMessage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
