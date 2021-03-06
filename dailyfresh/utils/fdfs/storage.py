from fdfs_client.client import Fdfs_client

from django.core.files.storage import Storage
from django.conf import settings


class FDFSStorage(Storage):
    """
    fastdfs 文件储存类
    """
    def __init__(self, client_conf=None, base_url=None):
        """
        初始化相关配置
        """
        self.client_conf = settings.FDFS_CLIENT_CONF if client_conf is None else client_conf
        self.base_url = settings.FDFS_URL if base_url is None else base_url

    def _open(self, name, mode='rb'):
        """
        打开文件时使用
        """
        pass

    def _save(self, name, content):
        """
        保存文件时使用的方法

        :argument

        content: 包含文件内容的 File 类对象
        """
        client = Fdfs_client(self.client_conf)
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception("上传文件到 fast dfs 失败")
        # 获取返回的文件 ID
        filename = res.get('Remote file_id')
        return filename

    def exists(self, name):
        """
        Django 判断文件名是否可用
        """
        return False  # fast dfs 不存在同名问题,返回 false 即可

    def url(self, name):
        """
        返回文件的 url
        """
        return self.base_url + name
