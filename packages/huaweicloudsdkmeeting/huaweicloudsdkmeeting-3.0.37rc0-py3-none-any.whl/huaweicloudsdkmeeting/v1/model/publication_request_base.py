# coding: utf-8

import pprint
import re

import six





class PublicationRequestBase:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'publish_name': 'str',
        'start_time': 'int',
        'end_time': 'int',
        'dept_list': 'list[str]',
        'device_list': 'list[str]'
    }

    attribute_map = {
        'publish_name': 'publishName',
        'start_time': 'startTime',
        'end_time': 'endTime',
        'dept_list': 'deptList',
        'device_list': 'deviceList'
    }

    def __init__(self, publish_name=None, start_time=None, end_time=None, dept_list=None, device_list=None):
        """PublicationRequestBase - a model defined in huaweicloud sdk"""
        
        

        self._publish_name = None
        self._start_time = None
        self._end_time = None
        self._dept_list = None
        self._device_list = None
        self.discriminator = None

        self.publish_name = publish_name
        self.start_time = start_time
        self.end_time = end_time
        self.dept_list = dept_list
        self.device_list = device_list

    @property
    def publish_name(self):
        """Gets the publish_name of this PublicationRequestBase.

        发布名称

        :return: The publish_name of this PublicationRequestBase.
        :rtype: str
        """
        return self._publish_name

    @publish_name.setter
    def publish_name(self, publish_name):
        """Sets the publish_name of this PublicationRequestBase.

        发布名称

        :param publish_name: The publish_name of this PublicationRequestBase.
        :type: str
        """
        self._publish_name = publish_name

    @property
    def start_time(self):
        """Gets the start_time of this PublicationRequestBase.

        开始时间

        :return: The start_time of this PublicationRequestBase.
        :rtype: int
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this PublicationRequestBase.

        开始时间

        :param start_time: The start_time of this PublicationRequestBase.
        :type: int
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this PublicationRequestBase.

        结束时间

        :return: The end_time of this PublicationRequestBase.
        :rtype: int
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this PublicationRequestBase.

        结束时间

        :param end_time: The end_time of this PublicationRequestBase.
        :type: int
        """
        self._end_time = end_time

    @property
    def dept_list(self):
        """Gets the dept_list of this PublicationRequestBase.

        发布到部门编码列表

        :return: The dept_list of this PublicationRequestBase.
        :rtype: list[str]
        """
        return self._dept_list

    @dept_list.setter
    def dept_list(self, dept_list):
        """Sets the dept_list of this PublicationRequestBase.

        发布到部门编码列表

        :param dept_list: The dept_list of this PublicationRequestBase.
        :type: list[str]
        """
        self._dept_list = dept_list

    @property
    def device_list(self):
        """Gets the device_list of this PublicationRequestBase.

        发布到设备用户ID列表

        :return: The device_list of this PublicationRequestBase.
        :rtype: list[str]
        """
        return self._device_list

    @device_list.setter
    def device_list(self, device_list):
        """Sets the device_list of this PublicationRequestBase.

        发布到设备用户ID列表

        :param device_list: The device_list of this PublicationRequestBase.
        :type: list[str]
        """
        self._device_list = device_list

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
        if not isinstance(other, PublicationRequestBase):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
