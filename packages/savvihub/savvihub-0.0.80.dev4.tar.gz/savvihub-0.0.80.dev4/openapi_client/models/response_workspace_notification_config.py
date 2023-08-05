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


class ResponseWorkspaceNotificationConfig(object):
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
        'emails': 'list[str]',
        'slack_team_name': 'str'
    }

    attribute_map = {
        'emails': 'emails',
        'slack_team_name': 'slack_team_name'
    }

    def __init__(self, emails=None, slack_team_name=None, local_vars_configuration=None):  # noqa: E501
        """ResponseWorkspaceNotificationConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._emails = None
        self._slack_team_name = None
        self.discriminator = None

        if emails is not None:
            self.emails = emails
        self.slack_team_name = slack_team_name

    @property
    def emails(self):
        """Gets the emails of this ResponseWorkspaceNotificationConfig.  # noqa: E501


        :return: The emails of this ResponseWorkspaceNotificationConfig.  # noqa: E501
        :rtype: list[str]
        """
        return self._emails

    @emails.setter
    def emails(self, emails):
        """Sets the emails of this ResponseWorkspaceNotificationConfig.


        :param emails: The emails of this ResponseWorkspaceNotificationConfig.  # noqa: E501
        :type emails: list[str]
        """

        self._emails = emails

    @property
    def slack_team_name(self):
        """Gets the slack_team_name of this ResponseWorkspaceNotificationConfig.  # noqa: E501


        :return: The slack_team_name of this ResponseWorkspaceNotificationConfig.  # noqa: E501
        :rtype: str
        """
        return self._slack_team_name

    @slack_team_name.setter
    def slack_team_name(self, slack_team_name):
        """Sets the slack_team_name of this ResponseWorkspaceNotificationConfig.


        :param slack_team_name: The slack_team_name of this ResponseWorkspaceNotificationConfig.  # noqa: E501
        :type slack_team_name: str
        """

        self._slack_team_name = slack_team_name

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
        if not isinstance(other, ResponseWorkspaceNotificationConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseWorkspaceNotificationConfig):
            return True

        return self.to_dict() != other.to_dict()
