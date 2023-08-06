# coding: utf-8

import pprint
import re

import six





class RestoreInstanceFromCollectionRequestBodyCollections:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'old_name': 'str',
        'new_name': 'str',
        'restore_collection_time': 'str'
    }

    attribute_map = {
        'old_name': 'old_name',
        'new_name': 'new_name',
        'restore_collection_time': 'restore_collection_time'
    }

    def __init__(self, old_name=None, new_name=None, restore_collection_time=None):
        """RestoreInstanceFromCollectionRequestBodyCollections - a model defined in huaweicloud sdk"""
        
        

        self._old_name = None
        self._new_name = None
        self._restore_collection_time = None
        self.discriminator = None

        self.old_name = old_name
        if new_name is not None:
            self.new_name = new_name
        self.restore_collection_time = restore_collection_time

    @property
    def old_name(self):
        """Gets the old_name of this RestoreInstanceFromCollectionRequestBodyCollections.

        恢复前表名。

        :return: The old_name of this RestoreInstanceFromCollectionRequestBodyCollections.
        :rtype: str
        """
        return self._old_name

    @old_name.setter
    def old_name(self, old_name):
        """Sets the old_name of this RestoreInstanceFromCollectionRequestBodyCollections.

        恢复前表名。

        :param old_name: The old_name of this RestoreInstanceFromCollectionRequestBodyCollections.
        :type: str
        """
        self._old_name = old_name

    @property
    def new_name(self):
        """Gets the new_name of this RestoreInstanceFromCollectionRequestBodyCollections.

        恢复后表名。

        :return: The new_name of this RestoreInstanceFromCollectionRequestBodyCollections.
        :rtype: str
        """
        return self._new_name

    @new_name.setter
    def new_name(self, new_name):
        """Sets the new_name of this RestoreInstanceFromCollectionRequestBodyCollections.

        恢复后表名。

        :param new_name: The new_name of this RestoreInstanceFromCollectionRequestBodyCollections.
        :type: str
        """
        self._new_name = new_name

    @property
    def restore_collection_time(self):
        """Gets the restore_collection_time of this RestoreInstanceFromCollectionRequestBodyCollections.

        数据库集合恢复时间点。UNIX时间戳格式，单位是毫秒，时区是UTC。

        :return: The restore_collection_time of this RestoreInstanceFromCollectionRequestBodyCollections.
        :rtype: str
        """
        return self._restore_collection_time

    @restore_collection_time.setter
    def restore_collection_time(self, restore_collection_time):
        """Sets the restore_collection_time of this RestoreInstanceFromCollectionRequestBodyCollections.

        数据库集合恢复时间点。UNIX时间戳格式，单位是毫秒，时区是UTC。

        :param restore_collection_time: The restore_collection_time of this RestoreInstanceFromCollectionRequestBodyCollections.
        :type: str
        """
        self._restore_collection_time = restore_collection_time

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
        if not isinstance(other, RestoreInstanceFromCollectionRequestBodyCollections):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
