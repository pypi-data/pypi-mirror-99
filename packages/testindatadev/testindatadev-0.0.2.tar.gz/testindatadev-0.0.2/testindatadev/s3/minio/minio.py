from minio import Minio
from minio.error import InvalidResponseError as ResponseError

#约定：s3包下面的所有文件均是对存储对象的操作，里面所有的变量，单词，描述，均是和存储对象相关的，不允许出现dataset相关的用语
class YcMinio():
    def __init__(self, access_key, secret_key, endpoint, secure=False):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint = endpoint.replace("http://", "").replace("https://", "")
        self.secure = secure

        self.client = Minio(
            self.endpoint,
            access_key = self.access_key,
            secret_key = self.secret_key,
            secure = False
        )

    #创建bucket
    def CreateBucket(self, bucket_name, location='cn-north-1'):
        try:
            self.client.make_bucket(bucket_name, location)
        except ResponseError as err:
            print(err)
        
    #列出所有的Dataset
    def ListAllBucket(self):
        buckets = self.client.list_buckets()
        for bucket in buckets:
            print(bucket.name)

    #列出某个Dataset下面的所有文件
    def ListObjects(self, bucket_name, prefix=None, recursive=False):
        objects = self.client.list_objects(bucket_name, prefix, recursive)
        for obj in objects:
            print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified, obj.etag, obj.size, obj.content_type)

    #上传单个文件数据
    def PutObject(self, bucket_name, object_name, file_path, content_type='application/octet-stream', metadata=None):
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
        except ResponseError as err:
            print(err)

    #删除单个文件
    def DeleteObject(self, bucket_name, object_name):
        try:
            self.client.remove_object(bucket_name, object_name)
        except ResponseError as err:
            print(err)