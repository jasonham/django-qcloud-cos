import os
from django.conf import settings
from django.core.files.storage import Storage
from django.core.exceptions import SuspiciousFileOperation
from django.utils.text import get_valid_filename
from django.utils.crypto import get_random_string
from qcloudcos.cos_object import CosObject


class QcloudStorage(Storage):
    def __init__(self, option=None):
        if not option:
            self.option = settings.QCLOUD_STORAGE_OPTION

    def _open(self, name, mode='rb'):
        cos = CosObject()
        response = cos.get_object(name, True)
        return response.content

    def _save(self, name, content):
        name = self._get_valid_name(name)
        name = self._get_available_name(name)
        content = content.read()
        cos_object = CosObject()
        response = cos_object.put_object(name, content)
        return response.request.path_url

    def _get_valid_name(self, name):
        dir_name, file_name = os.path.split(name)
        file_name = get_valid_filename(file_name)
        name = os.path.join(dir_name, file_name)
        return name

    def _get_available_name(self, name, max_length=None):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        while self.exists(name) or (max_length and len(name) > max_length):
            # file_ext includes the dot.
            name = os.path.join(dir_name, "%s_%s%s" % (file_root, get_random_string(7), file_ext))
            if max_length is None:
                continue
            # Truncate file_root if max_length exceeded.
            truncation = len(name) - max_length
            if truncation > 0:
                file_root = file_root[:-truncation]
                # Entire file_root was truncated in attempt to find an available filename.
                if not file_root:
                    raise SuspiciousFileOperation(
                        'Storage can not find an available filename for "%s". '
                        'Please make sure that the corresponding file field '
                        'allows sufficient "max_length".' % name
                    )
                name = os.path.join(dir_name, "%s_%s%s" % (file_root, get_random_string(7), file_ext))
        return name

    def exists(self, name):
        name = self._get_valid_name(name)
        cos = CosObject()
        response = cos.head_object(name, True)
        if response.status_code == 200:
            return True
        else:
            return False

    def url(self, name):
        if settings.COS_USE_CDN:
            cdn_host = 'file'
        else:
            cdn_host = 'cosgz'
        url = "http://%s-%s.%s.myqcloud.com%s" % (
            self.option['bucket'],
            self.option['Appid'],
            cdn_host,
            name,
        )

        return url

    def size(self, name):
        name = self._get_valid_name(name)
        cos = CosObject()
        response = cos.head_object(name, True)
        if response.status_code == 200:
            return response.headers['Content-Length']

    def delete(self, name):
        name = self._get_valid_name(name)
        cos = CosObject()
        cos.delete_object(name)
