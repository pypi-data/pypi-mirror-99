# coding: utf-8

import pprint
import re

import six





class TrackerObsInfo:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'bucket_name': 'str',
        'file_prefix_name': 'str',
        'is_obs_created': 'bool',
        'bucket_lifecycle': 'int'
    }

    attribute_map = {
        'bucket_name': 'bucket_name',
        'file_prefix_name': 'file_prefix_name',
        'is_obs_created': 'is_obs_created',
        'bucket_lifecycle': 'bucket_lifecycle'
    }

    def __init__(self, bucket_name=None, file_prefix_name=None, is_obs_created=None, bucket_lifecycle=None):
        """TrackerObsInfo - a model defined in huaweicloud sdk"""
        
        

        self._bucket_name = None
        self._file_prefix_name = None
        self._is_obs_created = None
        self._bucket_lifecycle = None
        self.discriminator = None

        if bucket_name is not None:
            self.bucket_name = bucket_name
        if file_prefix_name is not None:
            self.file_prefix_name = file_prefix_name
        if is_obs_created is not None:
            self.is_obs_created = is_obs_created
        if bucket_lifecycle is not None:
            self.bucket_lifecycle = bucket_lifecycle

    @property
    def bucket_name(self):
        """Gets the bucket_name of this TrackerObsInfo.

        标识OBS桶名称。由数字或字母开头，支持小写字母、数字、“-”、“.”，长度为3～63个字符。

        :return: The bucket_name of this TrackerObsInfo.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """Sets the bucket_name of this TrackerObsInfo.

        标识OBS桶名称。由数字或字母开头，支持小写字母、数字、“-”、“.”，长度为3～63个字符。

        :param bucket_name: The bucket_name of this TrackerObsInfo.
        :type: str
        """
        self._bucket_name = bucket_name

    @property
    def file_prefix_name(self):
        """Gets the file_prefix_name of this TrackerObsInfo.

        标识需要存储于OBS的日志文件前缀，0-9，a-z，A-Z，'-'，'.'，'_'长度为0～64字符。

        :return: The file_prefix_name of this TrackerObsInfo.
        :rtype: str
        """
        return self._file_prefix_name

    @file_prefix_name.setter
    def file_prefix_name(self, file_prefix_name):
        """Sets the file_prefix_name of this TrackerObsInfo.

        标识需要存储于OBS的日志文件前缀，0-9，a-z，A-Z，'-'，'.'，'_'长度为0～64字符。

        :param file_prefix_name: The file_prefix_name of this TrackerObsInfo.
        :type: str
        """
        self._file_prefix_name = file_prefix_name

    @property
    def is_obs_created(self):
        """Gets the is_obs_created of this TrackerObsInfo.

        是否支持新建OBS桶。   值为“true”时，表示新创建OBS桶存储事件文件；   值为“false”时，选择已存在的OBS桶存储事件文件。

        :return: The is_obs_created of this TrackerObsInfo.
        :rtype: bool
        """
        return self._is_obs_created

    @is_obs_created.setter
    def is_obs_created(self, is_obs_created):
        """Sets the is_obs_created of this TrackerObsInfo.

        是否支持新建OBS桶。   值为“true”时，表示新创建OBS桶存储事件文件；   值为“false”时，选择已存在的OBS桶存储事件文件。

        :param is_obs_created: The is_obs_created of this TrackerObsInfo.
        :type: bool
        """
        self._is_obs_created = is_obs_created

    @property
    def bucket_lifecycle(self):
        """Gets the bucket_lifecycle of this TrackerObsInfo.

        标识配置桶内对象存储周期。 当\"tracker_type\"参数值为\"data\"时该参数值有效。

        :return: The bucket_lifecycle of this TrackerObsInfo.
        :rtype: int
        """
        return self._bucket_lifecycle

    @bucket_lifecycle.setter
    def bucket_lifecycle(self, bucket_lifecycle):
        """Sets the bucket_lifecycle of this TrackerObsInfo.

        标识配置桶内对象存储周期。 当\"tracker_type\"参数值为\"data\"时该参数值有效。

        :param bucket_lifecycle: The bucket_lifecycle of this TrackerObsInfo.
        :type: int
        """
        self._bucket_lifecycle = bucket_lifecycle

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
        if not isinstance(other, TrackerObsInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
