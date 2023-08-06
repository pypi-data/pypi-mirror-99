# coding: utf-8

import pprint
import re

import six





class ActionDisForwarding:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'region_name': 'str',
        'project_id': 'str',
        'stream_name': 'str',
        'stream_id': 'str'
    }

    attribute_map = {
        'region_name': 'region_name',
        'project_id': 'project_id',
        'stream_name': 'stream_name',
        'stream_id': 'stream_id'
    }

    def __init__(self, region_name=None, project_id=None, stream_name=None, stream_id=None):
        """ActionDisForwarding - a model defined in huaweicloud sdk"""
        
        

        self._region_name = None
        self._project_id = None
        self._stream_name = None
        self._stream_id = None
        self.discriminator = None

        self.region_name = region_name
        self.project_id = project_id
        if stream_name is not None:
            self.stream_name = stream_name
        if stream_id is not None:
            self.stream_id = stream_id

    @property
    def region_name(self):
        """Gets the region_name of this ActionDisForwarding.

        DIS服务对应的region区域

        :return: The region_name of this ActionDisForwarding.
        :rtype: str
        """
        return self._region_name

    @region_name.setter
    def region_name(self, region_name):
        """Sets the region_name of this ActionDisForwarding.

        DIS服务对应的region区域

        :param region_name: The region_name of this ActionDisForwarding.
        :type: str
        """
        self._region_name = region_name

    @property
    def project_id(self):
        """Gets the project_id of this ActionDisForwarding.

        DIS服务对应的projectId信息

        :return: The project_id of this ActionDisForwarding.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ActionDisForwarding.

        DIS服务对应的projectId信息

        :param project_id: The project_id of this ActionDisForwarding.
        :type: str
        """
        self._project_id = project_id

    @property
    def stream_name(self):
        """Gets the stream_name of this ActionDisForwarding.

        DIS服务对应的通道名称，和通道ID参数中至少一个不为空，和通道ID参数都存在时，以通道ID参数值为准。通过调用DIS服务 [查询通道列表](https://support.huaweicloud.com/api-dis/dis_02_0024.html)接口获取。

        :return: The stream_name of this ActionDisForwarding.
        :rtype: str
        """
        return self._stream_name

    @stream_name.setter
    def stream_name(self, stream_name):
        """Sets the stream_name of this ActionDisForwarding.

        DIS服务对应的通道名称，和通道ID参数中至少一个不为空，和通道ID参数都存在时，以通道ID参数值为准。通过调用DIS服务 [查询通道列表](https://support.huaweicloud.com/api-dis/dis_02_0024.html)接口获取。

        :param stream_name: The stream_name of this ActionDisForwarding.
        :type: str
        """
        self._stream_name = stream_name

    @property
    def stream_id(self):
        """Gets the stream_id of this ActionDisForwarding.

        DIS服务对应的通道ID，和通道名称参数中至少一个不为空，和通道名称参数都存在时，以本参数值为准。通过调用DIS服务 [查询通道详情](https://support.huaweicloud.com/api-dis/dis_02_0025.html)接口获取。

        :return: The stream_id of this ActionDisForwarding.
        :rtype: str
        """
        return self._stream_id

    @stream_id.setter
    def stream_id(self, stream_id):
        """Sets the stream_id of this ActionDisForwarding.

        DIS服务对应的通道ID，和通道名称参数中至少一个不为空，和通道名称参数都存在时，以本参数值为准。通过调用DIS服务 [查询通道详情](https://support.huaweicloud.com/api-dis/dis_02_0025.html)接口获取。

        :param stream_id: The stream_id of this ActionDisForwarding.
        :type: str
        """
        self._stream_id = stream_id

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
        if not isinstance(other, ActionDisForwarding):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
