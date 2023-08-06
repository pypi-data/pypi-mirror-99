# coding: utf-8

import pprint
import re

import six





class HttpForwarding:


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'url': 'str',
        'cert_id': 'str',
        'cn_name': 'str',
        'sni_enable': 'bool'
    }

    attribute_map = {
        'url': 'url',
        'cert_id': 'cert_id',
        'cn_name': 'cn_name',
        'sni_enable': 'sni_enable'
    }

    def __init__(self, url=None, cert_id=None, cn_name=None, sni_enable=None):
        """HttpForwarding - a model defined in huaweicloud sdk"""
        
        

        self._url = None
        self._cert_id = None
        self._cn_name = None
        self._sni_enable = None
        self.discriminator = None

        self.url = url
        if cert_id is not None:
            self.cert_id = cert_id
        if cn_name is not None:
            self.cn_name = cn_name
        if sni_enable is not None:
            self.sni_enable = sni_enable

    @property
    def url(self):
        """Gets the url of this HttpForwarding.

        用于接收满足规则条件数据的http服务器地址。

        :return: The url of this HttpForwarding.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this HttpForwarding.

        用于接收满足规则条件数据的http服务器地址。

        :param url: The url of this HttpForwarding.
        :type: str
        """
        self._url = url

    @property
    def cert_id(self):
        """Gets the cert_id of this HttpForwarding.

        证书id，通过证书上传接口上传证书获取Id

        :return: The cert_id of this HttpForwarding.
        :rtype: str
        """
        return self._cert_id

    @cert_id.setter
    def cert_id(self, cert_id):
        """Sets the cert_id of this HttpForwarding.

        证书id，通过证书上传接口上传证书获取Id

        :param cert_id: The cert_id of this HttpForwarding.
        :type: str
        """
        self._cert_id = cert_id

    @property
    def cn_name(self):
        """Gets the cn_name of this HttpForwarding.

        当sni_enable为true时，此字段需要填写，当sni_enbale为false时，此字段默认为*

        :return: The cn_name of this HttpForwarding.
        :rtype: str
        """
        return self._cn_name

    @cn_name.setter
    def cn_name(self, cn_name):
        """Sets the cn_name of this HttpForwarding.

        当sni_enable为true时，此字段需要填写，当sni_enbale为false时，此字段默认为*

        :param cn_name: The cn_name of this HttpForwarding.
        :type: str
        """
        self._cn_name = cn_name

    @property
    def sni_enable(self):
        """Gets the sni_enable of this HttpForwarding.

        需要https服务端和客户端都支持此功能，默认为false，设成true表明Https的客户端在发起请求时，需要携带cn_name；https服务端根据cn_name返回对应的证书；设为false可关闭此功能

        :return: The sni_enable of this HttpForwarding.
        :rtype: bool
        """
        return self._sni_enable

    @sni_enable.setter
    def sni_enable(self, sni_enable):
        """Sets the sni_enable of this HttpForwarding.

        需要https服务端和客户端都支持此功能，默认为false，设成true表明Https的客户端在发起请求时，需要携带cn_name；https服务端根据cn_name返回对应的证书；设为false可关闭此功能

        :param sni_enable: The sni_enable of this HttpForwarding.
        :type: bool
        """
        self._sni_enable = sni_enable

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
        if not isinstance(other, HttpForwarding):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
