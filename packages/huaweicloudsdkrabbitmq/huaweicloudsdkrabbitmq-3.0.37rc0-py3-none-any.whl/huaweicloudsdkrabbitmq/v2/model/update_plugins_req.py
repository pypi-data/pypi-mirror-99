# coding: utf-8

import pprint
import re

import six





class UpdatePluginsReq:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'enable': 'bool',
        'plugins': 'str'
    }

    attribute_map = {
        'enable': 'enable',
        'plugins': 'plugins'
    }

    def __init__(self, enable=None, plugins=None):
        """UpdatePluginsReq - a model defined in huaweicloud sdk"""
        
        

        self._enable = None
        self._plugins = None
        self.discriminator = None

        if enable is not None:
            self.enable = enable
        if plugins is not None:
            self.plugins = plugins

    @property
    def enable(self):
        """Gets the enable of this UpdatePluginsReq.

        是否开启改插件。

        :return: The enable of this UpdatePluginsReq.
        :rtype: bool
        """
        return self._enable

    @enable.setter
    def enable(self, enable):
        """Sets the enable of this UpdatePluginsReq.

        是否开启改插件。

        :param enable: The enable of this UpdatePluginsReq.
        :type: bool
        """
        self._enable = enable

    @property
    def plugins(self):
        """Gets the plugins of this UpdatePluginsReq.

        插件列表，多个插件中间用“,”隔开。

        :return: The plugins of this UpdatePluginsReq.
        :rtype: str
        """
        return self._plugins

    @plugins.setter
    def plugins(self, plugins):
        """Sets the plugins of this UpdatePluginsReq.

        插件列表，多个插件中间用“,”隔开。

        :param plugins: The plugins of this UpdatePluginsReq.
        :type: str
        """
        self._plugins = plugins

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
        if not isinstance(other, UpdatePluginsReq):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
