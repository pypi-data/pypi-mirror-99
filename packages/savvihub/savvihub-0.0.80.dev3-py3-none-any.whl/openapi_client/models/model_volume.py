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


class ModelVolume(object):
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
        'base_path': 'str',
        'bucket_name': 'str',
        'created_dt': 'datetime',
        'deleted_dt': 'datetime',
        'edges': 'ModelVolumeEdges',
        'file_count': 'int',
        'id': 'int',
        'immutable_slug': 'str',
        'is_read_only': 'bool',
        'last_sync_time': 'datetime',
        'role_owner_ref': 'int',
        'role_type': 'str',
        'size': 'int',
        'status': 'str',
        'updated_dt': 'datetime'
    }

    attribute_map = {
        'base_path': 'base_path',
        'bucket_name': 'bucket_name',
        'created_dt': 'created_dt',
        'deleted_dt': 'deleted_dt',
        'edges': 'edges',
        'file_count': 'file_count',
        'id': 'id',
        'immutable_slug': 'immutable_slug',
        'is_read_only': 'is_read_only',
        'last_sync_time': 'last_sync_time',
        'role_owner_ref': 'role_owner_ref',
        'role_type': 'role_type',
        'size': 'size',
        'status': 'status',
        'updated_dt': 'updated_dt'
    }

    def __init__(self, base_path=None, bucket_name=None, created_dt=None, deleted_dt=None, edges=None, file_count=None, id=None, immutable_slug=None, is_read_only=None, last_sync_time=None, role_owner_ref=None, role_type=None, size=None, status=None, updated_dt=None, local_vars_configuration=None):  # noqa: E501
        """ModelVolume - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._base_path = None
        self._bucket_name = None
        self._created_dt = None
        self._deleted_dt = None
        self._edges = None
        self._file_count = None
        self._id = None
        self._immutable_slug = None
        self._is_read_only = None
        self._last_sync_time = None
        self._role_owner_ref = None
        self._role_type = None
        self._size = None
        self._status = None
        self._updated_dt = None
        self.discriminator = None

        if base_path is not None:
            self.base_path = base_path
        if bucket_name is not None:
            self.bucket_name = bucket_name
        self.created_dt = created_dt
        self.deleted_dt = deleted_dt
        if edges is not None:
            self.edges = edges
        if file_count is not None:
            self.file_count = file_count
        if id is not None:
            self.id = id
        if immutable_slug is not None:
            self.immutable_slug = immutable_slug
        if is_read_only is not None:
            self.is_read_only = is_read_only
        self.last_sync_time = last_sync_time
        if role_owner_ref is not None:
            self.role_owner_ref = role_owner_ref
        if role_type is not None:
            self.role_type = role_type
        if size is not None:
            self.size = size
        if status is not None:
            self.status = status
        self.updated_dt = updated_dt

    @property
    def base_path(self):
        """Gets the base_path of this ModelVolume.  # noqa: E501


        :return: The base_path of this ModelVolume.  # noqa: E501
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path):
        """Sets the base_path of this ModelVolume.


        :param base_path: The base_path of this ModelVolume.  # noqa: E501
        :type base_path: str
        """

        self._base_path = base_path

    @property
    def bucket_name(self):
        """Gets the bucket_name of this ModelVolume.  # noqa: E501


        :return: The bucket_name of this ModelVolume.  # noqa: E501
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this ModelVolume.


        :param bucket_name: The bucket_name of this ModelVolume.  # noqa: E501
        :type bucket_name: str
        """

        self._bucket_name = bucket_name

    @property
    def created_dt(self):
        """Gets the created_dt of this ModelVolume.  # noqa: E501


        :return: The created_dt of this ModelVolume.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this ModelVolume.


        :param created_dt: The created_dt of this ModelVolume.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def deleted_dt(self):
        """Gets the deleted_dt of this ModelVolume.  # noqa: E501


        :return: The deleted_dt of this ModelVolume.  # noqa: E501
        :rtype: datetime
        """
        return self._deleted_dt

    @deleted_dt.setter
    def deleted_dt(self, deleted_dt):
        """Sets the deleted_dt of this ModelVolume.


        :param deleted_dt: The deleted_dt of this ModelVolume.  # noqa: E501
        :type deleted_dt: datetime
        """

        self._deleted_dt = deleted_dt

    @property
    def edges(self):
        """Gets the edges of this ModelVolume.  # noqa: E501


        :return: The edges of this ModelVolume.  # noqa: E501
        :rtype: ModelVolumeEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this ModelVolume.


        :param edges: The edges of this ModelVolume.  # noqa: E501
        :type edges: ModelVolumeEdges
        """

        self._edges = edges

    @property
    def file_count(self):
        """Gets the file_count of this ModelVolume.  # noqa: E501


        :return: The file_count of this ModelVolume.  # noqa: E501
        :rtype: int
        """
        return self._file_count

    @file_count.setter
    def file_count(self, file_count):
        """Sets the file_count of this ModelVolume.


        :param file_count: The file_count of this ModelVolume.  # noqa: E501
        :type file_count: int
        """

        self._file_count = file_count

    @property
    def id(self):
        """Gets the id of this ModelVolume.  # noqa: E501


        :return: The id of this ModelVolume.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelVolume.


        :param id: The id of this ModelVolume.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def immutable_slug(self):
        """Gets the immutable_slug of this ModelVolume.  # noqa: E501


        :return: The immutable_slug of this ModelVolume.  # noqa: E501
        :rtype: str
        """
        return self._immutable_slug

    @immutable_slug.setter
    def immutable_slug(self, immutable_slug):
        """Sets the immutable_slug of this ModelVolume.


        :param immutable_slug: The immutable_slug of this ModelVolume.  # noqa: E501
        :type immutable_slug: str
        """

        self._immutable_slug = immutable_slug

    @property
    def is_read_only(self):
        """Gets the is_read_only of this ModelVolume.  # noqa: E501


        :return: The is_read_only of this ModelVolume.  # noqa: E501
        :rtype: bool
        """
        return self._is_read_only

    @is_read_only.setter
    def is_read_only(self, is_read_only):
        """Sets the is_read_only of this ModelVolume.


        :param is_read_only: The is_read_only of this ModelVolume.  # noqa: E501
        :type is_read_only: bool
        """

        self._is_read_only = is_read_only

    @property
    def last_sync_time(self):
        """Gets the last_sync_time of this ModelVolume.  # noqa: E501


        :return: The last_sync_time of this ModelVolume.  # noqa: E501
        :rtype: datetime
        """
        return self._last_sync_time

    @last_sync_time.setter
    def last_sync_time(self, last_sync_time):
        """Sets the last_sync_time of this ModelVolume.


        :param last_sync_time: The last_sync_time of this ModelVolume.  # noqa: E501
        :type last_sync_time: datetime
        """

        self._last_sync_time = last_sync_time

    @property
    def role_owner_ref(self):
        """Gets the role_owner_ref of this ModelVolume.  # noqa: E501


        :return: The role_owner_ref of this ModelVolume.  # noqa: E501
        :rtype: int
        """
        return self._role_owner_ref

    @role_owner_ref.setter
    def role_owner_ref(self, role_owner_ref):
        """Sets the role_owner_ref of this ModelVolume.


        :param role_owner_ref: The role_owner_ref of this ModelVolume.  # noqa: E501
        :type role_owner_ref: int
        """

        self._role_owner_ref = role_owner_ref

    @property
    def role_type(self):
        """Gets the role_type of this ModelVolume.  # noqa: E501


        :return: The role_type of this ModelVolume.  # noqa: E501
        :rtype: str
        """
        return self._role_type

    @role_type.setter
    def role_type(self, role_type):
        """Sets the role_type of this ModelVolume.


        :param role_type: The role_type of this ModelVolume.  # noqa: E501
        :type role_type: str
        """

        self._role_type = role_type

    @property
    def size(self):
        """Gets the size of this ModelVolume.  # noqa: E501


        :return: The size of this ModelVolume.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this ModelVolume.


        :param size: The size of this ModelVolume.  # noqa: E501
        :type size: int
        """

        self._size = size

    @property
    def status(self):
        """Gets the status of this ModelVolume.  # noqa: E501


        :return: The status of this ModelVolume.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ModelVolume.


        :param status: The status of this ModelVolume.  # noqa: E501
        :type status: str
        """

        self._status = status

    @property
    def updated_dt(self):
        """Gets the updated_dt of this ModelVolume.  # noqa: E501


        :return: The updated_dt of this ModelVolume.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this ModelVolume.


        :param updated_dt: The updated_dt of this ModelVolume.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

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
        if not isinstance(other, ModelVolume):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelVolume):
            return True

        return self.to_dict() != other.to_dict()
