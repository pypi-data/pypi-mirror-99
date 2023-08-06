# coding: utf-8

import pprint
import re

import six





class MetricRequestV2DividendCustomFields:


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
        'options': 'str'
    }

    attribute_map = {
        'name': 'name',
        'options': 'options'
    }

    def __init__(self, name=None, options=None):
        """MetricRequestV2DividendCustomFields - a model defined in huaweicloud sdk"""
        
        

        self._name = None
        self._options = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if options is not None:
            self.options = options

    @property
    def name(self):
        """Gets the name of this MetricRequestV2DividendCustomFields.

        自定义字段名称

        :return: The name of this MetricRequestV2DividendCustomFields.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MetricRequestV2DividendCustomFields.

        自定义字段名称

        :param name: The name of this MetricRequestV2DividendCustomFields.
        :type: str
        """
        self._name = name

    @property
    def options(self):
        """Gets the options of this MetricRequestV2DividendCustomFields.

        自定义字段取值，逗号分隔

        :return: The options of this MetricRequestV2DividendCustomFields.
        :rtype: str
        """
        return self._options

    @options.setter
    def options(self, options):
        """Sets the options of this MetricRequestV2DividendCustomFields.

        自定义字段取值，逗号分隔

        :param options: The options of this MetricRequestV2DividendCustomFields.
        :type: str
        """
        self._options = options

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
        if not isinstance(other, MetricRequestV2DividendCustomFields):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
