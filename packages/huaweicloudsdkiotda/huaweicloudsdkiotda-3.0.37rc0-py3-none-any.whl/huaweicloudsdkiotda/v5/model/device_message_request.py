# coding: utf-8

import pprint
import re

import six





class DeviceMessageRequest:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'message_id': 'str',
        'name': 'str',
        'message': 'object',
        'encoding': 'str',
        'payload_format': 'str',
        'topic': 'str',
        'topic_full_name': 'str'
    }

    attribute_map = {
        'message_id': 'message_id',
        'name': 'name',
        'message': 'message',
        'encoding': 'encoding',
        'payload_format': 'payload_format',
        'topic': 'topic',
        'topic_full_name': 'topic_full_name'
    }

    def __init__(self, message_id=None, name=None, message=None, encoding=None, payload_format=None, topic=None, topic_full_name=None):
        """DeviceMessageRequest - a model defined in huaweicloud sdk"""
        
        

        self._message_id = None
        self._name = None
        self._message = None
        self._encoding = None
        self._payload_format = None
        self._topic = None
        self._topic_full_name = None
        self.discriminator = None

        if message_id is not None:
            self.message_id = message_id
        if name is not None:
            self.name = name
        self.message = message
        if encoding is not None:
            self.encoding = encoding
        if payload_format is not None:
            self.payload_format = payload_format
        if topic is not None:
            self.topic = topic
        if topic_full_name is not None:
            self.topic_full_name = topic_full_name

    @property
    def message_id(self):
        """Gets the message_id of this DeviceMessageRequest.

        消息id，由用户生成（推荐使用UUID），同一个设备下唯一， 如果用户填写的id在设备下不唯一， 则接口返回错误。

        :return: The message_id of this DeviceMessageRequest.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """Sets the message_id of this DeviceMessageRequest.

        消息id，由用户生成（推荐使用UUID），同一个设备下唯一， 如果用户填写的id在设备下不唯一， 则接口返回错误。

        :param message_id: The message_id of this DeviceMessageRequest.
        :type: str
        """
        self._message_id = message_id

    @property
    def name(self):
        """Gets the name of this DeviceMessageRequest.

        消息名称

        :return: The name of this DeviceMessageRequest.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DeviceMessageRequest.

        消息名称

        :param name: The name of this DeviceMessageRequest.
        :type: str
        """
        self._name = name

    @property
    def message(self):
        """Gets the message of this DeviceMessageRequest.

        消息内容，支持string和json格式。 

        :return: The message of this DeviceMessageRequest.
        :rtype: object
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this DeviceMessageRequest.

        消息内容，支持string和json格式。 

        :param message: The message of this DeviceMessageRequest.
        :type: object
        """
        self._message = message

    @property
    def encoding(self):
        """Gets the encoding of this DeviceMessageRequest.

        消息内容编码格式，取值范围none|base64,默认值none。 

        :return: The encoding of this DeviceMessageRequest.
        :rtype: str
        """
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        """Sets the encoding of this DeviceMessageRequest.

        消息内容编码格式，取值范围none|base64,默认值none。 

        :param encoding: The encoding of this DeviceMessageRequest.
        :type: str
        """
        self._encoding = encoding

    @property
    def payload_format(self):
        """Gets the payload_format of this DeviceMessageRequest.

        有效负载格式，在消息内容编码格式为none时有效，取值范围standard|raw，默认值standard（平台封装的标准格式），取值为raw时直接将消息内容作为有效负载下发。 

        :return: The payload_format of this DeviceMessageRequest.
        :rtype: str
        """
        return self._payload_format

    @payload_format.setter
    def payload_format(self, payload_format):
        """Sets the payload_format of this DeviceMessageRequest.

        有效负载格式，在消息内容编码格式为none时有效，取值范围standard|raw，默认值standard（平台封装的标准格式），取值为raw时直接将消息内容作为有效负载下发。 

        :param payload_format: The payload_format of this DeviceMessageRequest.
        :type: str
        """
        self._payload_format = payload_format

    @property
    def topic(self):
        """Gets the topic of this DeviceMessageRequest.

        消息下行到设备的topic, 可选， 仅适用于MQTT协议接入的设备。 用户只能填写在租户产品界面配置的topic, 否则会校验不通过。 平台给消息topic添加的前缀为$oc/devices/{device_id}/user/， 用户可以在前缀的基础上增加自定义部分， 如增加messageDown，则平台拼接前缀后完整的topic为 $oc/devices/{device_id}/user/messageDown，其中device_id以实际设备的网关id替代。 如果用户指定该topic，消息会通过该topic下行到设备，如果用户不指定， 则消息通过系统默认的topic下行到设备,系统默认的topic格式为： $oc/devices/{device_id}/sys/messages/down。此字段与topic_full_name字段只可填写一个。 

        :return: The topic of this DeviceMessageRequest.
        :rtype: str
        """
        return self._topic

    @topic.setter
    def topic(self, topic):
        """Sets the topic of this DeviceMessageRequest.

        消息下行到设备的topic, 可选， 仅适用于MQTT协议接入的设备。 用户只能填写在租户产品界面配置的topic, 否则会校验不通过。 平台给消息topic添加的前缀为$oc/devices/{device_id}/user/， 用户可以在前缀的基础上增加自定义部分， 如增加messageDown，则平台拼接前缀后完整的topic为 $oc/devices/{device_id}/user/messageDown，其中device_id以实际设备的网关id替代。 如果用户指定该topic，消息会通过该topic下行到设备，如果用户不指定， 则消息通过系统默认的topic下行到设备,系统默认的topic格式为： $oc/devices/{device_id}/sys/messages/down。此字段与topic_full_name字段只可填写一个。 

        :param topic: The topic of this DeviceMessageRequest.
        :type: str
        """
        self._topic = topic

    @property
    def topic_full_name(self):
        """Gets the topic_full_name of this DeviceMessageRequest.

        消息下行到设备的完整topic名称, 可选。用户需要下发用户自定义的topic给设备时，可以使用该参数指定完整的topic名称，物联网平台不校验该topic是否在平台定义，直接透传给设备。设备需要提前订阅该topic。此字段与topic字段只可填写一个。 

        :return: The topic_full_name of this DeviceMessageRequest.
        :rtype: str
        """
        return self._topic_full_name

    @topic_full_name.setter
    def topic_full_name(self, topic_full_name):
        """Sets the topic_full_name of this DeviceMessageRequest.

        消息下行到设备的完整topic名称, 可选。用户需要下发用户自定义的topic给设备时，可以使用该参数指定完整的topic名称，物联网平台不校验该topic是否在平台定义，直接透传给设备。设备需要提前订阅该topic。此字段与topic字段只可填写一个。 

        :param topic_full_name: The topic_full_name of this DeviceMessageRequest.
        :type: str
        """
        self._topic_full_name = topic_full_name

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
        if not isinstance(other, DeviceMessageRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
