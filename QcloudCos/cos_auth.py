import random
import time
from urllib.parse import quote
import hmac
import hashlib
import binascii
import base64


class Auth(object):
    def __init__(self, appid, SecretID, SecretKey, bucket, region):
        """
        :param appid: 开发者访问 COS 服务时拥有的用户维度唯一资源标识，用以标示资源。
        :param SecretID: SecretID 是开发者拥有的项目身份识别 ID，用以身份认证
        :param SecretKey: SecretKey 是开发者拥有的项目身份密钥。
        :param bucket: 存储桶是 COS 中用于存储数据的容器，是用户存储在 Appid 下的第一级目录，每个对象都存储在一个存储桶中。
        :param region: 域名中的地域信息，枚举值：cn-east（华东），cn-north（华北），cn-south（华南），sg（新加坡）
        """
        self.appid = appid
        self.SecretID = SecretID
        self.SecretKey = SecretKey
        self.bucket = bucket
        self.region = region

        self.q_sign_time = int(time.time())
        self.q_key_time = self.q_sign_time + 60

    def get_signkey(self):
        q_time = '%s;%s' %s (self.q_sign_time, self.q_key_time)
        signkey = hmac.new(bytes(self.SecretKey,'utf-8'), bytes(q_time,'utf-8'), hashlib.sha1).hexdigest()
        return signkey

    def get_formatstring(self, http_string):
        format_method = http_string.split(str='', num=2)[0]




    # def __init__(self, appid, SecretID, SecretKey, bucket, file='', currentTime='', expiredTime='', rand=''):
    #     self.appid = appid
    #     self.SecretID = SecretID
    #     self.SecretKey = SecretKey
    #     self.bucket = bucket
    #     self.file = file
    #
    #     if currentTime == '':
    #         self.currentTime = int(time.time())
    #         self.expiredTime = self.currentTime + 60
    #         self.rand = random.randint(0, 9999999999)
    #     else:
    #         self.currentTime = currentTime
    #         self.expiredTime = expiredTime
    #         self.rand = rand
    #
    # def get_original(self):
    #     if self.file == '':
    #         t_tuple = (self.appid, self.bucket, self.SecretID, self.expiredTime, self.currentTime, self.rand)
    #         original = 'a=%s&b=%s&k=%s&e=%s&t=%s&r=%s&f=' % t_tuple
    #     else:
    #         t_tuple = (self.appid, self.bucket, self.file)
    #         filePath = '/%s/%s/%s' % t_tuple
    #         fileid = quote(filePath, safe='/', encoding='utf-8', errors=None)
    #         expired_time = 0
    #         t_tuple = (self.appid, self.bucket, self.SecretID, expired_time, self.currentTime, self.rand, fileid)
    #         original = 'a=%s&b=%s&k=%s&e=%s&t=%s&r=%s&f=%s' % t_tuple
    #
    #     return original
    #
    # def get_sign(self):
    #     original = self.get_original().encode('utf-8')
    #     secret_key = self.SecretKey.encode('utf-8')
    #     hmac_hexdigest = hmac.new(bytes(secret_key), bytes(original), hashlib.sha1).hexdigest()
    #     SignTmp = binascii.unhexlify(hmac_hexdigest)
    #     sign = base64.b64encode(SignTmp + original).decode('utf-8')
    #
    #     return sign
