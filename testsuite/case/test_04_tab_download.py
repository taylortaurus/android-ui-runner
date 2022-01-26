# coding: utf-8
# author: chenhongqing
from Public.appBase import *
import sys
import unittest
import os
import time

app = appBase()
class tab_download(unittest.TestCase, BasePage):
    """TAB DOWNLOAD下面的功能检查"""

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start(app.pkg_name)


    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop(app.pkg_name)


    @testcase
    def test_01_video_download(self):
        """检查视频下载"""
        app.case_restart_check(text='DOWNLOAD')
        self.d(text="DOWNLOAD").click(timeout=5)

        ###### 清理下载记录
        self.d(resourceId=res['com.app.videoplayer:id/ivDownload']).click()
        app.clear_downloaded_video()
        self.d.press('back')

        ###### 访问下载连接
        self.d(resourceId=res['com.app.videoplayer:id/clSearch']).click(timeout=5)
        self.d.send_keys("https://www.ted.com/talks/armand_d_angour_the_ancient_origins_of_the_olympics/up-next")
        self.d.press('enter')
        self.d(resourceId=res['com.app.videoplayer:id/button_analytics']).click(timeout=5)

        ###### 清理知栏消息
        app.clear_notification()
        self.d.press('back')

        ###### 检查下载管理器记录
        time.sleep(10)
        self.d(text="Download").click(timeout=5)
        self.d(text="view >").click(timeout=5)
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/flCover']).exists(timeout=1),
                        msg='下载管理器没有视频')
        self.screenshot()

        ###### 暂停下载
        self.d(resourceId=res['com.app.videoplayer:id/progress']).click()
        self.assertTrue(self.d(text='Paused').exists(timeout=5),msg='暂停下载失败')


        ###### 恢复下载
        self.d(resourceId=res['com.app.videoplayer:id/progress']).click()
        time.sleep(2)
        self.assertFalse(self.d(text='Paused').exists(timeout=5), msg='恢复下载失败')

        ###### 检查通知栏消息
        self.d.open_notification()
        self.assertTrue(self.d(text='app').exists(timeout=1),msg='通知栏没有下载消息')
        self.screenshot()
        self.d.press('back')

        ###### Downloading count
        downloading_count = int(self.d(resourceId=res['com.app.videoplayer:id/tvCount']).get_text())
        self.assertEqual(downloading_count, 1, msg='Downloading count计算错误')

        ###### 下载完成检查
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/tvDownloaded']).exists(timeout=540),
                        msg='下载完成超时')

        self.d(resourceId=res['com.app.videoplayer:id/ivLeft']).click(timeout=5)
        self.d.press('back')
        time.sleep(1)
        self.d(resourceId=res['com.app.videoplayer:id/ivSiteClose']).click(timeout=5)



    @testcase
    def test_02_playing_download(self):
        '''检查视频边播放边下载'''
        app.case_restart_check(text='DOWNLOAD')
        self.d(text="DOWNLOAD").click(timeout=5)

        ###### 访问下载连接
        self.d(resourceId=res['com.app.videoplayer:id/clSearch']).click(timeout=5)
        self.d.send_keys("https://www.ted.com/talks/armand_d_angour_the_ancient_origins_of_the_olympics/up-next")
        self.d.press('enter')
        self.d(resourceId=res['com.app.videoplayer:id/button_analytics']).click(timeout=5)

        ###### 在线播放
        time.sleep(10)
        self.d(text="Play").click()
        time.sleep(10)
        video_play = VdieoPlay.video_play_time_check()
        self.assertNotEqual(video_play[0], video_play[1], msg='播放时间没有跑动')
        self.screenshot()

        #todo:下载



    @testcase
    def test_03_bookmark(self):
        """检查bookmark功能"""
        app.case_restart_check(text='DOWNLOAD')
        self.d(text="DOWNLOAD").click(timeout=5)

        ###### 创建新的书签
        self.d(text="More").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/edtName']).set_text('google', timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/edtUrl']).set_text('https://google.com', timeout=5)
        self.d(text="Save").click(timeout=5)
        self.screenshot()

        ###### 打开书签
        self.d(text="google").click(timeout=5)
        self.assertTrue(self.d(text="Google").exists(timeout=10), msg='打开自建的书签失败')
        self.screenshot()
        self.d.click(0.076, 0.071)
        time.sleep(1)

        ###### 删除书签
        self.d(text="google").long_click(duration=5, timeout=10)
        BookMark_ID = res['com.app.videoplayer:id/rvBookMark']
        self.d.xpath(f'//*[@resource-id="{BookMark_ID}"]/android.view.ViewGroup[2]/android.widget.ImageView[2]').click()
        self.d(text='Ok').click(timeout=5)
        time.sleep(2)
        self.assertFalse(self.d(text='google').exists(timeout=5),msg='删除书签失败')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_04_whatsapp(self):
        """检查whatspp视频"""
        app.case_restart_check(text='DOWNLOAD')
        self.d(text="DOWNLOAD").click(timeout=5)
        self.d(text="Whatsapp").click(timeout=5)
        self.assertTrue(self.d(text='Open WhatsApp Status').exists(timeout=5),msg='打开whatsapp失败')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_05_youtube_video(self):
        """检查youtube视频"""
        app.case_restart_check(text='DOWNLOAD')
        self.d(text="DOWNLOAD").click(timeout=5)
        self.d(text="YouTube").click(timeout=5)
        self.d(text="Got it").click(timeout=10)
        time.sleep(5)
        self.screenshot()
