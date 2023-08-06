import os
try:
    from obs import ObsClient
    from obs import PutObjectHeader 
except:
    os.system("pip3 install huawei-obs")
    from obs import ObsClient
    from obs import PutObjectHeader 
import sys
import argparse
try:
    from tqdm import tqdm
except:
    os.system("pip3 install tqdm")
    from tqdm import tqdm
"""
TODO 文件上传  网络流上传
TODO sqlite 数据库学习 和 创建
TODO 通用obs的创建和使用
TODO 正规表格识别
"""



SIGN = "obs://"
# 2RQK5UOUHJQONX2HRZMH,tTYwPIrZzs3Szj4XpOvthcMTQfYA3690wgPfP87X

headers = PutObjectHeader() 
headers.contentType = 'text/plain' 

def helpArgConstruct(parse,name,help_):
    parse.add_argument(name,help=help_)

def arget():
    # TODO  argparse 解析  --u --d
    parser = argparse.ArgumentParser()
    helpArgConstruct(parser,"--obspath","the obs path is like 'obs://dpn/dataset/xxxx.xx' ")
    helpArgConstruct(parser,"--localpath","local machine like d://xxx not contain '/' at last")
    helpArgConstruct(parser, "--type","download 0      upload 1")
    # helpArgConstruct(parser,"--localpath","local machine like d://xxx not contain '/' at last")
    args = parser.parse_args()
    return args.obspath,args.localpath,int(args.type)


def constructObs(access_key_id='2RQK5UOUHJQONX2HRZMH', secret_access_key='tTYwPIrZzs3Szj4XpOvthcMTQfYA3690wgPfP87X', server='https://obs.cn-north-4.myhuaweicloud.com'):
    obsClient = ObsClient(
        access_key_id='2RQK5UOUHJQONX2HRZMH',
        secret_access_key='tTYwPIrZzs3Szj4XpOvthcMTQfYA3690wgPfP87X',
        server='https://obs.cn-north-4.myhuaweicloud.com'
    )
    return obsClient
# obs://dpn/dataset/
def downloadFile(obsPath,downloadPath):
    ObsClient = constructObs()
    assert obsPath.startswith(SIGN)
    if obsPath.endswith("/"):
        downloadFolder(ObsClient,obsPath,downloadPath)
    else:
        downloadSingleFile(ObsClient,obsPath,downloadPath)
    ObsClient.close()

def downloadSingleFile(ObsClient,obsPath,downloadPath,pathMatch=False):
    if pathMatch==True:
        assert obsPath.startswith(SIGN)
        tmp = obsPath[6:].split("/")
        bucketName,objectKeyPrefix = tmp[0],"/".join(tmp[1:-1])
        abspath = os.path.abspath(downloadPath)
        downloadPath = os.path.join(abspath,objectKeyPrefix)
    downloadFileTool(ObsClient,obsPath,downloadPath)

def downloadFileTool(ObsClient,obsPath,downloadPath,folderType=False):
    if obsPath.startswith(SIGN):
        tmp = obsPath[len(SIGN):].split("/")
        bucketName,objectKey = tmp[0],"/".join(tmp[1:])
        filename = tmp[-1]
    else:
        return
    if not os.path.isdir(downloadPath):
        os.makedirs(downloadPath)

    saveFileName = downloadPath + "/" + filename
    try:
        resp = ObsClient.getObject(bucketName=bucketName,objectKey=objectKey,downloadPath=saveFileName)
    except:
        import traceback
        print(traceback.format_exc())
        return 

def downloadFolder(ObsClient,obsPath,downloadPath):
    list_object = listObjects(ObsClient,obsPath)
    for each_object_path in tqdm(list_object,desc="downloading   "):
        downloadSingleFile(ObsClient,each_object_path,downloadPath,pathMatch=True)

def listObjects(ObsClient,obsPath,max_keys=1000000):
    assert obsPath.startswith(SIGN)
    assert obsPath.endswith("/")
    bucket = obsPath[len(SIGN):].split("/")[0]
    prefix = obsPath[len(SIGN)+len(bucket)+1:]
    list_object = []
    count = 0
    markey = None
    try:
        getans = ObsClient.listObjects(bucket, prefix=prefix,max_keys=max_keys)
        list_object =  getans['body']['contents']
        markey = list_object[-1]
        while True and len(list_object) % 1000 == 0:
            getans = ObsClient.listObjects(bucket, prefix=prefix, marker=markey ,max_keys=max_keys)
            more_list_object = getans['body']['contents']
            if len(more_list_object) < 1:
                break
            markey = more_list_object[-1]
            list_object += more_list_object
    except:
        print("[ERROR] get the list objects of "+ obsPath + " .Please check web connection .\n",getans)
    list_object = [i.key for i in list_object if not i.key.endswith("/")]
    list_object = [SIGN+bucket+"/"+i for i in list_object]
    return list_object

def makeValidPairs(self,local,obs):
    pass

def upload_local_folder(self,local,obs):
    bucket = obs[len(SIGN):].split("/")[0]
    prefix = obsPath[len(SIGN)+len(bucket)+1:]
    if os.path.isdir(local) or os.path.isfile(local):
        localfiles = os.path.abspath(local)
        resp = obsClient.putFile(bucket, 'objectkey', localfiles, headers=headers) 
    




if __name__ == "__main__":
    obspath,downloadpath = arget()
    # print(obspath,downloadpath)
    downloadFile(obspath,downloadpath)