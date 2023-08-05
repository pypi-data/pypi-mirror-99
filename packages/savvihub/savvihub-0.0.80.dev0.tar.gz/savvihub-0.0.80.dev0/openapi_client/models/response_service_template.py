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


class ResponseServiceTemplate(object):
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
        'created_by_id': 'int',
        'created_dt': 'datetime',
        'description': 'str',
        'env_vars': 'ModelEnvVars',
        'id': 'int',
        'image_execute_type': 'str',
        'immutable_slug': 'str',
        'is_public': 'bool',
        'is_savvihub_managed': 'bool',
        'kernel_image_id': 'int',
        'kernel_resource_spec_id': 'int',
        'name': 'str',
        'ports': 'ModelServicePorts',
        'service_config': 'ModelServiceConfig',
        'service_type': 'str',
        'start_command': 'str',
        'updated_dt': 'datetime',
        'workspace_id': 'int'
    }

    attribute_map = {
        'created_by_id': 'created_by_id',
        'created_dt': 'created_dt',
        'description': 'description',
        'env_vars': 'env_vars',
        'id': 'id',
        'image_execute_type': 'image_execute_type',
        'immutable_slug': 'immutable_slug',
        'is_public': 'is_public',
        'is_savvihub_managed': 'is_savvihub_managed',
        'kernel_image_id': 'kernel_image_id',
        'kernel_resource_spec_id': 'kernel_resource_spec_id',
        'name': 'name',
        'ports': 'ports',
        'service_config': 'service_config',
        'service_type': 'service_type',
        'start_command': 'start_command',
        'updated_dt': 'updated_dt',
        'workspace_id': 'workspace_id'
    }

    def __init__(self, created_by_id=None, created_dt=None, description=None, env_vars=None, id=None, image_execute_type=None, immutable_slug=None, is_public=None, is_savvihub_managed=None, kernel_image_id=None, kernel_resource_spec_id=None, name=None, ports=None, service_config=None, service_type=None, start_command=None, updated_dt=None, workspace_id=None, local_vars_configuration=None):  # noqa: E501
        """ResponseServiceTemplate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._created_by_id = None
        self._created_dt = None
        self._description = None
        self._env_vars = None
        self._id = None
        self._image_execute_type = None
        self._immutable_slug = None
        self._is_public = None
        self._is_savvihub_managed = None
        self._kernel_image_id = None
        self._kernel_resource_spec_id = None
        self._name = None
        self._ports = None
        self._service_config = None
        self._service_type = None
        self._start_command = None
        self._updated_dt = None
        self._workspace_id = None
        self.discriminator = None

        self.created_by_id = created_by_id
        self.created_dt = created_dt
        self.description = description
        if env_vars is not None:
            self.env_vars = env_vars
        self.id = id
        self.image_execute_type = image_execute_type
        self.immutable_slug = immutable_slug
        self.is_public = is_public
        self.is_savvihub_managed = is_savvihub_managed
        self.kernel_image_id = kernel_image_id
        self.kernel_resource_spec_id = kernel_resource_spec_id
        self.name = name
        if ports is not None:
            self.ports = ports
        if service_config is not None:
            self.service_config = service_config
        self.service_type = service_type
        self.start_command = start_command
        self.updated_dt = updated_dt
        self.workspace_id = workspace_id

    @property
    def created_by_id(self):
        """Gets the created_by_id of this ResponseServiceTemplate.  # noqa: E501


        :return: The created_by_id of this ResponseServiceTemplate.  # noqa: E501
        :rtype: int
        """
        return self._created_by_id

    @created_by_id.setter
    def created_by_id(self, created_by_id):
        """Sets the created_by_id of this ResponseServiceTemplate.


        :param created_by_id: The created_by_id of this ResponseServiceTemplate.  # noqa: E501
        :type created_by_id: int
        """
        if self.local_vars_configuration.client_side_validation and created_by_id is None:  # noqa: E501
            raise ValueError("Invalid value for `created_by_id`, must not be `None`")  # noqa: E501

        self._created_by_id = created_by_id

    @property
    def created_dt(self):
        """Gets the created_dt of this ResponseServiceTemplate.  # noqa: E501


        :return: The created_dt of this ResponseServiceTemplate.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ResponseServiceTemplate.


        :param created_dt: The created_dt of this ResponseServiceTemplate.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def description(self):
        """Gets the description of this ResponseServiceTemplate.  # noqa: E501


        :return: The description of this ResponseServiceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ResponseServiceTemplate.


        :param description: The description of this ResponseServiceTemplate.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def env_vars(self):
        """Gets the env_vars of this ResponseServiceTemplate.  # noqa: E501


        :return: The env_vars of this ResponseServiceTemplate.  # noqa: E501
        :rtype: ModelEnvVars
        """
        return self._env_vars

    @env_vars.setter
    def env_vars(self, env_vars):
        """Sets the env_vars of this ResponseServiceTemplate.


        :param env_vars: The env_vars of this ResponseServiceTemplate.  # noqa: E501
        :type env_vars: ModelEnvVars
        """

        self._env_vars = env_vars

    @property
    def id(self):
        """Gets the id of this ResponseServiceTemplate.  # noqa: E501


        :return: The id of this ResponseServiceTemplate.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseServiceTemplate.


        :param id: The id of this ResponseServiceTemplate.  # noqa: E501
        :type id: int
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def image_execute_type(self):
        """Gets the image_execute_type of this ResponseServiceTemplate.  # noqa: E501


        :return: The image_execute_type of this ResponseServiceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._image_execute_type

    @image_execute_type.setter
    def image_execute_type(self, image_execute_type):
        """Sets the image_execute_type of this ResponseServiceTemplate.


        :param image_execute_type: The image_execute_type of this ResponseServiceTemplate.  # noqa: E501
        :type image_execute_type: str
        """

        self._image_execute_type = image_execute_type

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ResponseServiceTemplate.  # noqa: E501


        :return: The immutable_slug of this ResponseServiceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ResponseServiceTemplate.


        :param immutable_slug: The immutable_slug of this ResponseServiceTemplate.  # noqa: E501
        :type immutable_slug: str
        """
        if self.local_vars_configuration.client_side_validation and immutable_slug is None:  # noqa: E501
            raise ValueError("Invalid value for `immutable_slug`, must not be `None`")  # noqa: E501

        self._immutable_slug = immutable_slug

    @property
    def is_public(self):
        """Gets the is_public of this ResponseServiceTemplate.  # noqa: E501


        :return: The is_public of this ResponseServiceTemplate.  # noqa: E501
        :rtype: bool
        """
        return self._is_public

    @is_public.setter
    def is_public(self, is_public):
        """Sets the is_public of this ResponseServiceTemplate.


        :param is_public: The is_public of this ResponseServiceTemplate.  # noqa: E501
        :type is_public: bool
        """
        if self.local_vars_configuration.client_side_validation and is_public is None:  # noqa: E501
            raise ValueError("Invalid value for `is_public`, must not be `None`")  # noqa: E501

        self._is_public = is_public

    @property
    def is_savvihub_managed(self):
        """Gets the is_savvihub_managed of this ResponseServiceTemplate.  # noqa: E501


        :return: The is_savvihub_managed of this ResponseServiceTemplate.  # noqa: E501
        :rtype: bool
        """
        return self._is_savvihub_managed

    @is_savvihub_managed.setter
    def is_savvihub_managed(self, is_savvihub_managed):
        """Sets the is_savvihub_managed of this ResponseServiceTemplate.


        :param is_savvihub_managed: The is_savvihub_managed of this ResponseServiceTemplate.  # noqa: E501
        :type is_savvihub_managed: bool
        """
        if self.local_vars_configuration.client_side_validation and is_savvihub_managed is None:  # noqa: E501
            raise ValueError("Invalid value for `is_savvihub_managed`, must not be `None`")  # noqa: E501

        self._is_savvihub_managed = is_savvihub_managed

    @property
    def kernel_image_id(self):
        """Gets the kernel_image_id of this ResponseServiceTemplate.  # noqa: E501


        :return: The kernel_image_id of this ResponseServiceTemplate.  # noqa: E501
        :rtype: int
        """
        return self._kernel_image_id

    @kernel_image_id.setter
    def kernel_image_id(self, kernel_image_id):
        """Sets the kernel_image_id of this ResponseServiceTemplate.


        :param kernel_image_id: The kernel_image_id of this ResponseServiceTemplate.  # noqa: E501
        :type kernel_image_id: int
        """

        self._kernel_image_id = kernel_image_id

    @property
    def kernel_resource_spec_id(self):
        """Gets the kernel_resource_spec_id of this ResponseServiceTemplate.  # noqa: E501


        :return: The kernel_resource_spec_id of this ResponseServiceTemplate.  # noqa: E501
        :rtype: int
        """
        return self._kernel_resource_spec_id

    @kernel_resource_spec_id.setter
    def kernel_resource_spec_id(self, kernel_resource_spec_id):
        """Sets the kernel_resource_spec_id of this ResponseServiceTemplate.


        :param kernel_resource_spec_id: The kernel_resource_spec_id of this ResponseServiceTemplate.  # noqa: E501
        :type kernel_resource_spec_id: int
        """

        self._kernel_resource_spec_id = kernel_resource_spec_id

    @property
    def name(self):
        """Gets the name of this ResponseServiceTemplate.  # noqa: E501


        :return: The name of this ResponseServiceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseServiceTemplate.


        :param name: The name of this ResponseServiceTemplate.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def ports(self):
        """Gets the ports of this ResponseServiceTemplate.  # noqa: E501


        :return: The ports of this ResponseServiceTemplate.  # noqa: E501
        :rtype: ModelServicePorts
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this ResponseServiceTemplate.


        :param ports: The ports of this ResponseServiceTemplate.  # noqa: E501
        :type ports: ModelServicePorts
        """

        self._ports = ports

    @property
    def service_config(self):
        """Gets the service_config of this ResponseServiceTemplate.  # noqa: E501


        :return: The service_config of this ResponseServiceTemplate.  # noqa: E501
        :rtype: ModelServiceConfig
        """
        return self._service_config

    @service_config.setter
    def service_config(self, service_config):
        """Sets the service_config of this ResponseServiceTemplate.


        :param service_config: The service_config of this ResponseServiceTemplate.  # noqa: E501
        :type service_config: ModelServiceConfig
        """

        self._service_config = service_config

    @property
    def service_type(self):
        """Gets the service_type of this ResponseServiceTemplate.  # noqa: E501


        :return: The service_type of this ResponseServiceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._service_type

    @service_type.setter
    def service_type(self, service_type):
        """Sets the service_type of this ResponseServiceTemplate.


        :param service_type: The service_type of this ResponseServiceTemplate.  # noqa: E501
        :type service_type: str
        """
        if self.local_vars_configuration.client_side_validation and service_type is None:  # noqa: E501
            raise ValueError("Invalid value for `service_type`, must not be `None`")  # noqa: E501

        self._service_type = service_type

    @property
    def start_command(self):
        """Gets the start_command of this ResponseServiceTemplate.  # noqa: E501


        :return: The start_command of this ResponseServiceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._start_command

    @start_command.setter
    def start_command(self, start_command):
        """Sets the start_command of this ResponseServiceTemplate.


        :param start_command: The start_command of this ResponseServiceTemplate.  # noqa: E501
        :type start_command: str
        """

        self._start_command = start_command

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ResponseServiceTemplate.  # noqa: E501


        :return: The updated_dt of this ResponseServiceTemplate.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ResponseServiceTemplate.


        :param updated_dt: The updated_dt of this ResponseServiceTemplate.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def workspace_id(self):
        """Gets the workspace_id of this ResponseServiceTemplate.  # noqa: E501


        :return: The workspace_id of this ResponseServiceTemplate.  # noqa: E501
        :rtype: int
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this ResponseServiceTemplate.


        :param workspace_id: The workspace_id of this ResponseServiceTemplate.  # noqa: E501
        :type workspace_id: int
        """
        if self.local_vars_configuration.client_side_validation and workspace_id is None:  # noqa: E501
            raise ValueError("Invalid value for `workspace_id`, must not be `None`")  # noqa: E501

        self._workspace_id = workspace_id

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
        if not isinstance(other, ResponseServiceTemplate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseServiceTemplate):
            return True

        return self.to_dict() != other.to_dict()
