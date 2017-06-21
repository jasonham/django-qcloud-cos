#!/usr/bin/env python
# coding=utf-8

import time
from urllib2 import quote
import hmac
import hashlib


class Auth(object):
    def __init__(self, appid, SecretID, SecretKey, bucket, region, method, objectName, head="", parameters="", sign_time="", key_time=""):
        """

        :param appid: 开发者访问 COS 服务时拥有的用户维度唯一资源标识，用以标示资源。
        :param SecretID: SecretID 是开发者拥有的项目身份识别 ID，用以身份认证
        :param SecretKey: SecretKey 是开发者拥有的项目身份密钥。
        :param bucket: 存储桶是 COS 中用于存储数据的容器，是用户存储在 Appid 下的第一级目录，每个对象都存储在一个存储桶中。
        :param region: 域名中的地域信息，枚举值：cn-east（华东），cn-north（华北），cn-south（华南），sg（新加坡）
        :param method: 指该请求的 HTTP 操作行为，例如 PUT/GET/DELETE，必须转为小写字符。
        :param objectName: 指该请求中的 URI 部分，即除去 http:// 协议和域名的部分（通常以 / 开始），并且不包含 URL 中的参数部分（通常以 ? 开始）。
        :param head: 指请求中的 HTTP 头部信息，用 key=value 的方式表达。头部的 key 必须全部小写，value 必须经过 URL Encode。如果有多个参数对可使用 & 连接。key值按字典序排序
        :param parameters: 指该请求中的参数部分（以 ? 开始的部分），用 key=value 的方式表达。
        :param sign_time: 无需指定 签名的有效起止时间，其使用 10 位 Unix 时间戳来表示，有效效力精确到秒。该字段通过分号区分起止，起时在前、止时在后。
        :param key_time: 无需指定 用户可以自定义 SignningKey 有效时间，使用 10 位 Unix 时间戳来表示，有效效力精确到秒。该字段通过分号区分起止，起始时间在前、终止时间在后。一般 q-key-time 的时间范围大于等于 q-sign-time。
        """
        self.appid = appid
        self.SecretID = SecretID
        self.SecretKey = SecretKey
        self.bucket = bucket
        self.region = region

        self.method = method
        self.objectname = objectName
        self.parameters = parameters.encode('utf-8')
        self.head = head

        if sign_time == "":
            self.q_sign_time = int(time.time())
        else:
            self.q_sign_time = int(sign_time)

        if key_time == "":
            self.q_key_time = int(self.q_sign_time) + 600
        else:
            self.q_key_time = int(key_time)

        self.sh1hash_formatstring = ''

    def get_signkey(self):
        q_time = '%s;%s' % (self.q_sign_time, self.q_key_time)
        signkey = hmac.new(bytearray(self.SecretKey, 'utf-8'), bytearray(q_time, 'utf-8'), hashlib.sha1).hexdigest()
        return signkey

    def format_args(self, args, isfullstring=True, isheader=True):
        my_f_args = ''
        if args != '':
            list_temp = []
            if isheader:
                str_temp = '%s-%s.%s.myqcloud.com' % (self.bucket, self.appid, self.region)
                list_temp = [('host', quote(str_temp, encoding='utf-8').lower())]

            try:
                args_list = args.split('&')
            except:
                args_list = args

            for n in args_list:
                arg = n.split(':')
                list_temp.append((arg[0].lower(), quote(arg[1], encoding='utf-8').lower()))

            list_temp.sort(key=lambda x: x[0])

            if isfullstring:
                for n in list_temp:
                    my_f_args += n[0] + '=' + n[1] + '&'
            else:
                for n in list_temp:
                    my_f_args += n[0] + ';'

            my_f_args = my_f_args[0:-1]

        return my_f_args

    def get_formatstring(self):
        format_method = self.method
        format_url = self.objectname
        format_parameters = self.format_args(self.parameters, True, False)

        format_head = self.format_args(self.head)
        format_string = "%s\n%s\n%s\n%s\n" % (format_method, format_url, format_parameters, format_head)

        return format_string

    def get_stringtosign(self):
        q_sign_time = '%s;%s' % (self.q_sign_time, self.q_key_time)
        formatstring = self.get_formatstring()
        sh1hash_formatstring = hashlib.sha1(formatstring.encode('utf-8')).hexdigest()
        stringtosign = "sha1\n%s\n%s\n" % (q_sign_time, sh1hash_formatstring)
        return stringtosign

    def get_signature(self):
        signature = hmac.new(
            bytearray(self.get_signkey(), 'utf-8'),
            bytearray(self.get_stringtosign(), 'utf-8'),
            hashlib.sha1
        ).hexdigest()
        return signature

    def get_authorization(self):
        header_list = self.format_args(self.head, False)
        signed_parameter = self.format_args(self.parameters, False, False)
        q_time = '%s;%s' % (self.q_sign_time, self.q_key_time)

        t_tuple = (self.SecretID, q_time, q_time, header_list, signed_parameter, self.get_signature())
        authorization = "q-sign-algorithm=sha1&" \
                        "q-ak=%s&" \
                        "q-sign-time=%s&" \
                        "q-key-time=%s&" \
                        "q-header-list=%s&" \
                        "q-url-param-list=%s&" \
                        "q-signature=%s" % t_tuple
        return authorization
