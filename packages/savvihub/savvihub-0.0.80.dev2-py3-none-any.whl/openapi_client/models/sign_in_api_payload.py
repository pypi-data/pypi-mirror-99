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


class SignInAPIPayload(object):
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
        'email_or_username': 'str',
        'password': 'str'
    }

    attribute_map = {
        'email_or_username': 'email_or_username',
        'password': 'password'
    }

    def __init__(self, email_or_username=None, password=None, local_vars_configuration=None):  # noqa: E501
        """SignInAPIPayload - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._email_or_username = None
        self._password = None
        self.discriminator = None

        self.email_or_username = email_or_username
        self.password = password

    @property
    def email_or_username(self):
        """Gets the email_or_username of this SignInAPIPayload.  # noqa: E501


        :return: The email_or_username of this SignInAPIPayload.  # noqa: E501
        :rtype: str
        """
        return self._email_or_username

    @email_or_username.setter
    def email_or_username(self, email_or_username):
        """Sets the email_or_username of this SignInAPIPayload.


        :param email_or_username: The email_or_username of this SignInAPIPayload.  # noqa: E501
        :type email_or_username: str
        """
        if self.local_vars_configuration.client_side_validation and email_or_username is None:  # noqa: E501
            raise ValueError("Invalid value for `email_or_username`, must not be `None`")  # noqa: E501

        self._email_or_username = email_or_username

    @property
    def password(self):
        """Gets the password of this SignInAPIPayload.  # noqa: E501


        :return: The password of this SignInAPIPayload.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this SignInAPIPayload.


        :param password: The password of this SignInAPIPayload.  # noqa: E501
        :type password: str
        """
        if self.local_vars_configuration.client_side_validation and password is None:  # noqa: E501
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501

        self._password = password

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
        if not isinstance(other, SignInAPIPayload):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SignInAPIPayload):
            return True

        return self.to_dict() != other.to_dict()
