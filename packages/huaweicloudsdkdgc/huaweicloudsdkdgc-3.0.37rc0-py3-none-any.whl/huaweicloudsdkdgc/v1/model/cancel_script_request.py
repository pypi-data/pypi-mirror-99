# coding: utf-8

import pprint
import re

import six





class CancelScriptRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'script_name': 'str',
        'instance_id': 'str'
    }

    attribute_map = {
        'script_name': 'script_name',
        'instance_id': 'instance_id'
    }

    def __init__(self, script_name=None, instance_id=None):
        """CancelScriptRequest - a model defined in huaweicloud sdk"""
        
        

        self._script_name = None
        self._instance_id = None
        self.discriminator = None

        self.script_name = script_name
        self.instance_id = instance_id

    @property
    def script_name(self):
        """Gets the script_name of this CancelScriptRequest.


        :return: The script_name of this CancelScriptRequest.
        :rtype: str
        """
        return self._script_name

    @script_name.setter
    def script_name(self, script_name):
        """Sets the script_name of this CancelScriptRequest.


        :param script_name: The script_name of this CancelScriptRequest.
        :type: str
        """
        self._script_name = script_name

    @property
    def instance_id(self):
        """Gets the instance_id of this CancelScriptRequest.


        :return: The instance_id of this CancelScriptRequest.
        :rtype: str
        """
        return self._instance_id

    @instance_id.setter
    def instance_id(self, instance_id):
        """Sets the instance_id of this CancelScriptRequest.


        :param instance_id: The instance_id of this CancelScriptRequest.
        :type: str
        """
        self._instance_id = instance_id

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
        if not isinstance(other, CancelScriptRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
