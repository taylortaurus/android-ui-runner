# coding: utf-8
# author: chenhongqing

from Public.appBase import *
import sys
import unittest
import time

app = appBase()
class Install(unittest.TestCase, BasePage):
    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_stop_all()

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop(app.pkg_name)

    @testcase
    def test_01_install_apk(self):
        """安装apk"""
        self.d.app_uninstall(app.pkg_name)
        self.local_install(app.apk_path)

    @testcase
    def test_02_env_check(self):
        """执行环境检查"""
        # todo:准备一个文件夹放测试视频
        self.d.app_start(app.pkg_name)
        app.startpage_handle()
        app.rate_skip()
        app.vip_check()
        app.clear_home_xxx()
        app.clear_music()
        app.download_xxx()





