#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
sys.path.append('..')
from Public.Drivers import Drivers
from Public.Report import *
from Public.maxim_monkey import Maxim
import unittest
from Monkey import login_steps

if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    # 命令执行：python3 monkey_run.py com.nemo.starhalo 10 200
    pkgname = sys.argv[1] # 包名
    runtime = sys.argv[2] # 执行时长
    throttle = sys.argv[3] # 点击延迟时间
    data = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    backup_report('./MaximReport', './MaximReport_History', data)
    cases = unittest.TestSuite()

    #cases.addTest(login_steps.abcd('test_install_login')) # 执行monkey前的操作
    command = Maxim().command(package=pkgname, runtime=runtime, mode='uiautomatordfs',
                              throttle=throttle,
                              options=' -v -v ', whitelist=True)

    Drivers().run_maxim(cases=cases, command=command, actions=True, widget_black=False)
