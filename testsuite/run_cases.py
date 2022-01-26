#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../..')
sys.path.append('.')
import os
import json, re
import requests
import time
import multiprocessing
from Public.CaseStrategy import CaseStrategy
from Public.Drivers import Drivers
from Public.Report import *
from Public.common import common
BASE_DIR = os.path.dirname(os.getcwd())
apk_dir = os.path.join(BASE_DIR, 'apk/app/')
mapping_dir = os.path.join(BASE_DIR, 'mapping/')
apk_link = os.environ["apk_link"]
apk_name = ('test.apk',os.environ["apk_name"])[os.environ["apk_name"] != 'NA']
mapping_link = os.environ["mapping_link"]
build_num = os.environ["build_num"]
pkg_branch = os.environ["pkg_branch"]

if __name__ == '__main__':

    fileinfo={
        "apk":{ "file_link":apk_link,"file_dir":apk_dir, "file_name":apk_name },
        "mapping":{"file_link": mapping_link,"file_dir": mapping_dir,"file_name": 'mapping.zip'}
    }

    cm = common()
    filetypes = ['apk','mapping']
    pool = multiprocessing.Pool(processes=len(filetypes))
    for filetype in filetypes:
        pool.apply_async(cm.download_from_url,args=(fileinfo[filetype]['file_link'],
                                                fileinfo[filetype]['file_dir'],
                                                fileinfo[filetype]['file_name'],))
    pool.close()
    pool.join()

    # cm.download_file(filelink=apk_link, path=apk_dir, name=apk_name)
    # cm.download_file(filelink=mapping_link, path=mapping_dir, name='mapping.zip')

    cs = CaseStrategy(suite_path='testsuite',case_path='case',case_pattern='test*.py')
    cases = cs.collect_cases(suite=False)
    result = Drivers().run(cases)
    pass_num = result['pass']
    fail_num = result['fail']
    error_num = result['error']
    os.rename('TestReport',f'TestReport_{build_num}')
    print(f'成功用例数：{pass_num}')
    print(f'失败用例数：{fail_num}')
    print(f'错误用例数：{error_num}')
    print(f'报告地址：http://192.168.13.59:8181/TestReport_{build_num}/V2029_370fd6a9/TestReport.html')

    msg_data = {
        "msgtype": "markdown",
        "markdown": {
            "title": f"app-UI测试报告(#{build_num})",
            "text": f"#### app-UI测试报告({pkg_branch}-#{build_num})" \
                    + f"\n  > ##### {apk_name}" \
                    + f"\n  > ##### 成功：{pass_num}" \
                    + f"\n  > ##### 失败：{fail_num}" \
                    + f"\n  > ##### 错误：{error_num}" \
                    + f"\n  > ##### [查看测试报告](http://192.168.13.59:8181/TestReport_{build_num}/V2029_370fd6a9/TestReport.html)"\
                    + f"\n  > ##### [查看错误日志](http://192.168.13.59:8181/TestReport_{build_num}/V2029_370fd6a9/logcat.log)"

        },
        "at": {
            "atMobiles": ["18926184988"],
            "isAtAll": False
        }
    }
    # 调试模式 debug=True
    cm.dingding_robot(msg_data,debug=False)
