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


class ProtoVolumeMountRequest(object):
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
        'dataset': 'ProtoVolumeMountRequestSourceDataset',
        'empty_dir': 'object',
        'mount_path': 'str',
        'mount_type': 'str',
        'output': 'object',
        'project': 'ProtoVolumeMountRequestSourceProject',
        'volume': 'ProtoVolumeMountRequestSourceVolume'
    }

    attribute_map = {
        'dataset': 'dataset',
        'empty_dir': 'empty_dir',
        'mount_path': 'mount_path',
        'mount_type': 'mount_type',
        'output': 'output',
        'project': 'project',
        'volume': 'volume'
    }

    def __init__(self, dataset=None, empty_dir=None, mount_path=None, mount_type=None, output=None, project=None, volume=None, local_vars_configuration=None):  # noqa: E501
        """ProtoVolumeMountRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._dataset = None
        self._empty_dir = None
        self._mount_path = None
        self._mount_type = None
        self._output = None
        self._project = None
        self._volume = None
        self.discriminator = None

        if dataset is not None:
            self.dataset = dataset
        if empty_dir is not None:
            self.empty_dir = empty_dir
        self.mount_path = mount_path
        self.mount_type = mount_type
        if output is not None:
            self.output = output
        if project is not None:
            self.project = project
        if volume is not None:
            self.volume = volume

    @property
    def dataset(self):
        """Gets the dataset of this ProtoVolumeMountRequest.  # noqa: E501


        :return: The dataset of this ProtoVolumeMountRequest.  # noqa: E501
        :rtype: ProtoVolumeMountRequestSourceDataset
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this ProtoVolumeMountRequest.


        :param dataset: The dataset of this ProtoVolumeMountRequest.  # noqa: E501
        :type dataset: ProtoVolumeMountRequestSourceDataset
        """

        self._dataset = dataset

    @property
    def empty_dir(self):
        """Gets the empty_dir of this ProtoVolumeMountRequest.  # noqa: E501


        :return: The empty_dir of this ProtoVolumeMountRequest.  # noqa: E501
        :rtype: object
        """
        return self._empty_dir

    @empty_dir.setter
    def empty_dir(self, empty_dir):
        """Sets the empty_dir of this ProtoVolumeMountRequest.


        :param empty_dir: The empty_dir of this ProtoVolumeMountRequest.  # noqa: E501
        :type empty_dir: object
        """

        self._empty_dir = empty_dir

    @property
    def mount_path(self):
        """Gets the mount_path of this ProtoVolumeMountRequest.  # noqa: E501


        :return: The mount_path of this ProtoVolumeMountRequest.  # noqa: E501
        :rtype: str
        """
        return self._mount_path

    @mount_path.setter
    def mount_path(self, mount_path):
        """Sets the mount_path of this ProtoVolumeMountRequest.


        :param mount_path: The mount_path of this ProtoVolumeMountRequest.  # noqa: E501
        :type mount_path: str
        """
        if self.local_vars_configuration.client_side_validation and mount_path is None:  # noqa: E501
            raise ValueError("Invalid value for `mount_path`, must not be `None`")  # noqa: E501

        self._mount_path = mount_path

    @property
    def mount_type(self):
        """Gets the mount_type of this ProtoVolumeMountRequest.  # noqa: E501


        :return: The mount_type of this ProtoVolumeMountRequest.  # noqa: E501
        :rtype: str
        """
        return self._mount_type

    @mount_type.setter
    def mount_type(self, mount_type):
        """Sets the mount_type of this ProtoVolumeMountRequest.


        :param mount_type: The mount_type of this ProtoVolumeMountRequest.  # noqa: E501
        :type mount_type: str
        """
        if self.local_vars_configuration.client_side_validation and mount_type is None:  # noqa: E501
            raise ValueError("Invalid value for `mount_type`, must not be `None`")  # noqa: E501
        allowed_values = ["empty-dir", "project", "dataset", "output", "volume"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and mount_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `mount_type` ({0}), must be one of {1}"  # noqa: E501
                .format(mount_type, allowed_values)
            )

        self._mount_type = mount_type

    @property
    def output(self):
        """Gets the output of this ProtoVolumeMountRequest.  # noqa: E501


        :return: The output of this ProtoVolumeMountRequest.  # noqa: E501
        :rtype: object
        """
        return self._output

    @output.setter
    def output(self, output):
        """Sets the output of this ProtoVolumeMountRequest.


        :param output: The output of this ProtoVolumeMountRequest.  # noqa: E501
        :type output: object
        """

        self._output = output

    @property
    def project(self):
        """Gets the project of this ProtoVolumeMountRequest.  # noqa: E501


        :return: The project of this ProtoVolumeMountRequest.  # noqa: E501
        :rtype: ProtoVolumeMountRequestSourceProject
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ProtoVolumeMountRequest.


        :param project: The project of this ProtoVolumeMountRequest.  # noqa: E501
        :type project: ProtoVolumeMountRequestSourceProject
        """

        self._project = project

    @property
    def volume(self):
        """Gets the volume of this ProtoVolumeMountRequest.  # noqa: E501


        :return: The volume of this ProtoVolumeMountRequest.  # noqa: E501
        :rtype: ProtoVolumeMountRequestSourceVolume
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this ProtoVolumeMountRequest.


        :param volume: The volume of this ProtoVolumeMountRequest.  # noqa: E501
        :type volume: ProtoVolumeMountRequestSourceVolume
        """

        self._volume = volume

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
        if not isinstance(other, ProtoVolumeMountRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ProtoVolumeMountRequest):
            return True

        return self.to_dict() != other.to_dict()
