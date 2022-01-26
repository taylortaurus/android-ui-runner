import os
import sys
import requests
import json
import subprocess
import jenkins
import re
from tqdm import trange
from tqdm import tqdm
from urllib.request import urlopen
import ssl
from Public.ReadConfig import ReadConfig
import time
from logzero import logger


class common(object):

    def __init__(self,mapping_type=None,mapping_channel=None):
        self.rc = ReadConfig()
        self.dingding_token = self.rc.get_dingding_token('app')
        # self.mapping_path = self.rc.get_mapping_path(mapping_type,mapping_channel)
        self.mapping_gp_path = self.rc.get_file_path('mapping_gp_path')
        self.mapping_vid_path = self.rc.get_file_path('mapping_vid_path')
        self.apk_path = self.rc.get_file_path('apk_path')
        self.pkg_name = self.rc.get_pkg_name()
        self.apk_rel_path =self.apk_path + self.file_name(self.apk_path,'.apk')
        self.mapping = {}

    def file_name(self, filedir, ftype) -> str:
        """获取文件名"""
        L = []
        for root, dirs, files in os.walk(filedir):
            for file in files:
                if os.path.splitext(file)[1] == ftype:
                    L.append(os.path.join(file))
                else:
                    L.append('no file')
        return L[0]

    def to_uiautomator_id(self,original_total_id) -> str:
        """匹配映射的resourceId"""
        split = original_total_id.split('.R.')
        pkg_name = split[0].strip()
        res_type_id = split[1]
        res_type = res_type_id.split('.')[0].strip()
        res_id = res_type_id.split('.')[1].strip()
        return f'{pkg_name}:{res_type}/{res_id}'

    def parse_mapping_file(self,file_path, is_aab=False) -> dict:
        """解析混淆后的mapping文件"""
        f = open(file_path, 'r')
        parse_started = False
        while True:
            line = f.readline().strip()
            if line == 'res id mapping:':
                parse_started = True
                continue
            if parse_started:
                if line == '':
                    break
                split = line.split('->')
                before = split[0].strip()
                if is_aab:
                    before = before.split(':')[1]
                after = split[1].strip()
                self.mapping[self.to_uiautomator_id(before)] = self.to_uiautomator_id(after)
        return self.mapping

    def dingding_robot(self,data,debug=False) -> str:
        """发送钉钉消息"""
        if debug is False:
            headers = {'content-type': 'application/json'}
            r = requests.post(self.dingding_token, headers=headers, data=json.dumps(data))
            r.encoding = 'utf-8'
            logger.info(r.text)
            return (r.text)
        else:
            return 'debug模式'

    def putcmd(self,cmd):
        """执行cmd命令"""
        cmd = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out = str(cmd.stdout.read(), encoding="utf-8")
        error = str(cmd.stderr.read(), encoding="utf-8")
        return out.strip(), error.strip()

    def _is_exits(self,path) -> bool:
        """判断文件是否存在"""
        return os.path.exists(path)

    def upload_file(self,file_path,timeout=None) -> str:
        """上传文件"""
        files = {'file': open(file_path, 'rb')}
        url = "http://161.117.69.170:82/upload_file"
        res = requests.post(url, files=files, timeout=timeout)
        return res['data']['url']

    def download_from_url(self,filelink=None, path=None, name=None):
        """下载文件"""
        os.system(f'rm -rf {path}*')
        logger.info(f'开始下载:{filelink}')
        ssl._create_default_https_context = ssl._create_unverified_context
        file_size = int(urlopen(filelink).info().get('Content-Length', -1))
        if os.path.exists(path+name):
            first_byte = os.path.getsize(path+name)
        else:
            first_byte = 0
        if first_byte >= file_size:
            return file_size
        header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=filelink.split('/')[-1])
        req = requests.get(filelink, headers=header, stream=True)
        with(open(path+name, 'ab')) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
        pbar.close()
        if name.endswith('.zip') is True:
            logger.info("开始解压ZIP")
            os.system(f'unzip {path}{name} -d  {path}')
        return file_size

    def download_file(self, filelink=None, path=None, name=None) -> int:
        """下载文件"""
        os.system(f'rm -rf {path}*')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        r = requests.get(filelink, timeout=600,headers=headers)
        with open(path + name, "wb") as code:
            code.write(r.content)
        if name.endswith('.zip') is True:
            os.system(f'unzip {path}/{name} -d  {path}')
        if r.status_code == 200:
            logger.info(f'下载文件成功:{filelink}')
        else:
            logger.info(f'下载文件失败:{filelink}')
        return r.status_code

    def join(self,str,seq):
        """字符串拼接"""
        return str.join(seq)


if __name__ == '__main__':
    a = common()
    print(a.apk_rel_path)
