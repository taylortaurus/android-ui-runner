#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../..')
sys.path.append('.')
import os
import json, re
import requests
import time
from Public.CaseStrategy import CaseStrategy
from Public.Drivers import Drivers
from Public.Report import *
from Public.common import common


if __name__ == '__main__':
    common_handle = common()
    cs = CaseStrategy(suite_path='testsuite',case_path='pdisk',case_pattern='test*.py')
    cases = cs.collect_cases(suite=False)
    result = Drivers().run(cases)
    pass_num = result['pass']
    fail_num = result['fail']
    error_num = result['error']
    print(f'成功用例数：{pass_num}')
    print(f'失败用例数：{fail_num}')
    print(f'错误用例数：{error_num}')
    print(f'报告地址：http://192.168.3.156:8181/TestReport/V2029_370fd6a9/TestReport.html')

    # Generate zip_report file  压缩测试报告文件
    # zip_report()
