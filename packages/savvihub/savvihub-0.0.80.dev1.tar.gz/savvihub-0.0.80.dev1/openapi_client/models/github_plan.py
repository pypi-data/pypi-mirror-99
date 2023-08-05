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


class GithubPlan(object):
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
        'collaborators': 'int',
        'filled_seats': 'int',
        'name': 'str',
        'private_repos': 'int',
        'seats': 'int',
        'space': 'int'
    }

    attribute_map = {
        'collaborators': 'collaborators',
        'filled_seats': 'filled_seats',
        'name': 'name',
        'private_repos': 'private_repos',
        'seats': 'seats',
        'space': 'space'
    }

    def __init__(self, collaborators=None, filled_seats=None, name=None, private_repos=None, seats=None, space=None, local_vars_configuration=None):  # noqa: E501
        """GithubPlan - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._collaborators = None
        self._filled_seats = None
        self._name = None
        self._private_repos = None
        self._seats = None
        self._space = None
        self.discriminator = None

        self.collaborators = collaborators
        self.filled_seats = filled_seats
        self.name = name
        self.private_repos = private_repos
        self.seats = seats
        self.space = space

    @property
    def collaborators(self):
        """Gets the collaborators of this GithubPlan.  # noqa: E501


        :return: The collaborators of this GithubPlan.  # noqa: E501
        :rtype: int
        """
        return self._collaborators

    @collaborators.setter
    def collaborators(self, collaborators):
        """Sets the collaborators of this GithubPlan.


        :param collaborators: The collaborators of this GithubPlan.  # noqa: E501
        :type collaborators: int
        """

        self._collaborators = collaborators

    @property
    def filled_seats(self):
        """Gets the filled_seats of this GithubPlan.  # noqa: E501


        :return: The filled_seats of this GithubPlan.  # noqa: E501
        :rtype: int
        """
        return self._filled_seats

    @filled_seats.setter
    def filled_seats(self, filled_seats):
        """Sets the filled_seats of this GithubPlan.


        :param filled_seats: The filled_seats of this GithubPlan.  # noqa: E501
        :type filled_seats: int
        """

        self._filled_seats = filled_seats

    @property
    def name(self):
        """Gets the name of this GithubPlan.  # noqa: E501


        :return: The name of this GithubPlan.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GithubPlan.


        :param name: The name of this GithubPlan.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def private_repos(self):
        """Gets the private_repos of this GithubPlan.  # noqa: E501


        :return: The private_repos of this GithubPlan.  # noqa: E501
        :rtype: int
        """
        return self._private_repos

    @private_repos.setter
    def private_repos(self, private_repos):
        """Sets the private_repos of this GithubPlan.


        :param private_repos: The private_repos of this GithubPlan.  # noqa: E501
        :type private_repos: int
        """

        self._private_repos = private_repos

    @property
    def seats(self):
        """Gets the seats of this GithubPlan.  # noqa: E501


        :return: The seats of this GithubPlan.  # noqa: E501
        :rtype: int
        """
        return self._seats

    @seats.setter
    def seats(self, seats):
        """Sets the seats of this GithubPlan.


        :param seats: The seats of this GithubPlan.  # noqa: E501
        :type seats: int
        """

        self._seats = seats

    @property
    def space(self):
        """Gets the space of this GithubPlan.  # noqa: E501


        :return: The space of this GithubPlan.  # noqa: E501
        :rtype: int
        """
        return self._space

    @space.setter
    def space(self, space):
        """Sets the space of this GithubPlan.


        :param space: The space of this GithubPlan.  # noqa: E501
        :type space: int
        """

        self._space = space

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
        if not isinstance(other, GithubPlan):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GithubPlan):
            return True

        return self.to_dict() != other.to_dict()
