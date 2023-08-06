import sys
import os
from concurrent.futures import as_completed, ProcessPoolExecutor

sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from s3.minio.minio import YcMinio

# 约定：dataset下的所有方法均是对数据集的操作，非clint调用的地方，严禁出现bucket之类的存储对象用语
# 本类用来解决各个存储对象之间的差异，通过type构造不同的客户端解决问题，类似工厂类
# bucket = dataset
# object = record
class Dataset():
    def __init__(self, access_key, secret_key, endpoint="http://127.0.0.1:8888/", type="minio"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint = endpoint
        if type == "minio":
            self.client = YcMinio(self.access_key, self.secret_key, self.endpoint)

    def ListAllDataset(self, datasetName="", recu=False):
        if datasetName == "":
            self.client.ListAllBucket()
        else:
            self.client.ListObjects(datasetName, recursive=recu)

    def CreateDataset(self, datasetName):
        self.client.CreateBucket(datasetName)

    def PutFilesToDataset(self, datasetName, rootPath, ext="", batchNum=0):
        total = 0        
        i = 0
        for root, dir, files in os.walk(rootPath):
            for fileName in files:
                if fileName.endswith(ext):
                    total += 1

        dirname = os.path.dirname(rootPath)
        for root, dir, files in os.walk(rootPath):
            for fileName in files:
                if fileName.endswith(ext):
                    filePath = os.path.join(root, fileName)
                    objectName = filePath.replace(dirname, "")
                    self.PutFileToDataset(datasetName, objectName, filePath)
                    i += 1
                    per = (i * 100) // total
                    showText = filePath + " =====> " + objectName
                    process = "\r[%3s%%]: %s\n" % (per, showText)
                    print(process, end='', flush=True)

        print("success total:" + str(total))
    
    def PutFileToDataset(self, datasetName, objectName, filePath):
        self.client.PutObject(datasetName, objectName, filePath)

    def DeleteFromDataset(self, datasetName, objectName):
        self.client.DeleteObject(datasetName, objectName)
        