import random
import time
from urllib.parse import quote
import hmac
import hashlib
import binascii
import base64


class Auth(object):
    def __init__(self, appid, SecretID, SecretKey, bucket, file='', currentTime='', expiredTime='', rand=''):
        self.appid = appid
        self.SecretID = SecretID
        self.SecretKey = SecretKey
        self.bucket = bucket
        self.file = file

        if currentTime == '':
            self.currentTime = int(time.time())
            self.expiredTime = self.currentTime + 60
            self.rand = random.randint(0, 9999999999)
        else:
            self.currentTime = currentTime
            self.expiredTime = expiredTime
            self.rand = rand

    def get_original(self):
        if self.file == '':
            t_tuple = (self.appid, self.bucket, self.SecretID, self.expiredTime, self.currentTime, self.rand)
            original = 'a=%s&b=%s&k=%s&e=%s&t=%s&r=%s&f=' % t_tuple
        else:
            fileid = quote(self.file, safe='/', encoding='utf-8', errors=None)
            expired_time = 0
            t_tuple = (self.appid, self.bucket, self.SecretID, expired_time, self.currentTime, self.rand, fileid)
            original = 'a=%s&b=%s&k=%s&e=%s&t=%s&r=%s&f=%s' % t_tuple

        return original

    def get_sign(self):
        original = self.get_original().encode('utf-8')
        secret_key = self.SecretKey.encode('utf-8')
        hmac_hexdigest = hmac.new(bytes(secret_key), bytes(original), hashlib.sha1).hexdigest()
        SignTmp = binascii.unhexlify(hmac_hexdigest)
        sign = base64.b64encode(SignTmp + original).decode('utf-8')

        return sign
