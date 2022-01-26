# coding: utf-8
# author: chenhongqing
from Public.appBase import *
import sys
import unittest
import os
import time

app = appBase()
class tab_music(unittest.TestCase, BasePage):
    """TAB MUSIC下面的功能检查
    # todo:Folder
    # todo:Album
    # todo:Artist
    """

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start(app.pkg_name)


    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop(app.pkg_name)


    @testcase
    def test_01_music_show(self):
        """检查音频文件展示"""
        app.case_restart_check(text='MUSIC')
        self.d(text="MUSIC").click(timeout=5)
        self.assertTrue(self.d(text="test_video").exists(timeout=5),msg='新增的音频文件没有展示')
        self.screenshot()

    @testcase
    def test_02_music_more_rename(self):
        """检查音频MORE-Rename"""
        app.case_restart_check(text='MUSIC')
        self.d(text="MUSIC").click(timeout=5)
        if self.d(text="test_video").exists(timeout=5):
            self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click()
            self.d(text="Rename").click(timeout=5)
            self.d(resourceId=res['com.app.videoplayer:id/edt']).clear_text()
            self.assertTrue(self.d(text="Enter a name").exists(timeout=5), msg='清除文本失败')
            self.d.send_keys('test_music0')
            self.d(text="Commit").click(timeout=5)
            self.assertTrue(self.d(text="test_music0").exists(timeout=5), msg='重命名失败')
            self.screenshot()
        else:
            print('test_video音频文件不存在')

    @testcase
    def test_03_music_play(self):
        """检查音频播放"""
        app.case_restart_check(text='MUSIC')
        self.d(text="MUSIC").click(timeout=5)
        self.d(text="test_music0").click()
        app.music_permission()  # 处理音乐权限
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivPlayOrPause']).exists(timeout=5),
                        msg='没有进入音频播放页')
        self.screenshot()

        ###### 暂停播放
        self.d(resourceId=res['com.app.videoplayer:id/ivPlayOrPause']).click()  # 暂停
        time_before = self.d(resourceId=res['com.app.videoplayer:id/tvStartTime']).get_text(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivPlayOrPause']).click()  # 播放
        time.sleep(5)
        time_after = self.d(resourceId=res['com.app.videoplayer:id/tvStartTime']).get_text(timeout=5)
        self.assertNotEqual(time_before, time_after, msg='播放时间没有走动')

        ###### 下一首
        self.d(resourceId=res['com.app.videoplayer:id/ivPlayNext']).click()  # 下一首
        action.exist_click(text='Exit')
        self.assertTrue(self.d(text="test_music1").exists(timeout=5), msg='切换下一首失败')

        ###### 上一首
        self.d(resourceId=res['com.app.videoplayer:id/ivPlayPre']).click()
        action.exist_click(text='Exit')
        self.assertTrue(self.d(text="test_music0").exists(timeout=5), msg='切换上一首失败')

        ###### 底部播放栏
        action.exist_click(text='Exit')
        self.d(resourceId=res['com.app.videoplayer:id/ivBack']).click()
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='底部没有播放栏')

        ###### 通知栏
        self.d.open_notification()
        app.clear_notification()
        self.assertTrue(self.d(text="app").exists(timeout=5), msg='通知栏没有播放记录')
        # todo:通知栏记录操作（暂停、关闭）
        self.d.press('back')

        ###### 关闭播放栏
        self.d(resourceId=res['com.app.videoplayer:id/ivClose']).click(timeout=5)
        self.screenshot()

    @testcase
    def test_04_music_more_favorite(self):
        """检查音频MORE-Favorite"""
        app.case_restart_check(text='MUSIC')
        self.d(text="MUSIC").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click()
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        self.d(text="Favorite").click(timeout=5)
        self.assertTrue(self.d(text="Remove favorite").exists(timeout=5),msg='收藏失败')
        self.screenshot()
        self.d.press('back')
        self.d(text="Playlist").click(timeout=5)
        self.d(text="Favorite").click(timeout=5)
        self.assertTrue(self.d(text="test_music0").exists(timeout=5),msg='Playlist没有收藏记录')
        self.screenshot()
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click()
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        self.d(text="Remove favorite").click(timeout=5)
        time.sleep(2)
        self.assertFalse(self.d(text="test_music0").exists(timeout=5),msg='取消收藏失败')
        self.screenshot()

    @testcase
    def test_05_music_more_fileinfo(self):
        """检查音频MORE-File info"""
        app.case_restart_check(text='MUSIC')
        self.d(text="MUSIC").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click()
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        self.d(text="File info").click(timeout=5)
        self.d(text="More").click(timeout=5)
        self.assertTrue(self.d(text="Stream 1").exists(timeout=5),msg='没有more信息')
        self.screenshot()
        self.d(text="CLOSE").click(timeout=5)
















