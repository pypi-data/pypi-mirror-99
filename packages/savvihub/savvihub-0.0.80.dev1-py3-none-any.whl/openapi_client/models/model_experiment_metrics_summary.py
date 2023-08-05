# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import inspect
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class ModelExperimentMetricsSummary(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'latest': 'dict(str, ProtoExperimentMetric)'
    }

    attribute_map = {
        'latest': 'latest'
    }

    def __init__(self, latest=None, local_vars_configuration=None):  # noqa: E501
        """ModelExperimentMetricsSummary - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._latest = None
        self.discriminator = None

        if latest is not None:
            self.latest = latest

    @property
    def latest(self):
        """Gets the latest of this ModelExperimentMetricsSummary.  # noqa: E501


        :return: The latest of this ModelExperimentMetricsSummary.  # noqa: E501
        :rtype: dict(str, ProtoExperimentMetric)
        """
        return self._latest

    @latest.setter
    def latest(self, latest):
        """Sets the latest of this ModelExperimentMetricsSummary.


        :param latest: The latest of this ModelExperimentMetricsSummary.  # noqa: E501
        :type latest: dict(str, ProtoExperimentMetric)
        """

        self._latest = latest

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = inspect.getargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ModelExperimentMetricsSummary):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelExperimentMetricsSummary):
            return True

        return self.to_dict() != other.to_dict()
