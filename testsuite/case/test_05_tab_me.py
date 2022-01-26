# coding: utf-8
# author: chenhongqing
from Public.appBase import *
import sys
import unittest
import os
import time
import re

app = appBase()
class tab_me(unittest.TestCase, BasePage):
    """TAB ME下面的功能检查"""
    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start(app.pkg_name)

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop(app.pkg_name)

    @testcase
    def test_01_me_vip(self):
        """检查订阅"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=5)
        if not self.d(text='You are already a VIP').exists(timeout=5):  # vip标识
            self.d(text='3-Day Free Trial').click(timeout=5)
            self.d(text="CONTINUE").click(timeout=5)
            self.d(text="订阅").click(timeout=5)
            action.exist_click(text='以后再说')
            action.exist_click(text='不用了')
            action.exist_click(text='确定')
            action.exist_click(text='Done')
            self.d(text="VIDEO").click(timeout=5)
        self.screenshot()

    @testcase
    def test_02_me_file_transfer(self):
        """检查传输功能"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=10)
        self.d(text="File Transfer").click(timeout=5)

        ###### Receive
        self.d(resourceId=res['com.app.videoplayer:id/ivReceive']).click(timeout=5)
        self.d(text="Allow").click(timeout=5)
        self.d(resourceId="com.android.permissioncontroller:id/permission_allow_foreground_only_button").click(timeout=5)
        self.assertTrue(self.d(text='Invite your friend to scan the QR code to transfer file.').exists(timeout=10),msg='打开二维码失败')
        self.screenshot()
        self.d.press('back')
        action.exist_click(text='Yes')

        ###### Send
        self.d(resourceId='com.app.videoplayer:id/ivSend').click(timeout=5)
        self.assertTrue(self.d(text='app_video.mp4').exists(timeout=10), msg='视频列表没有显示视频')
        self.d(text="MUSIC").click(timeout=5)
        self.assertTrue(self.d(text='test_music1').exists(timeout=10), msg='音乐列表没有显示音乐')
        self.screenshot()

        self.d(text="Folder").click(timeout=5)
        self.assertTrue(self.d(text='Download').exists(timeout=10), msg='音乐列表没有显示文件夹')
        self.screenshot()

        self.d(text="VIDEO").click(timeout=5)
        self.d(text="Folder").click(timeout=5)
        self.assertTrue(self.d(text='download').exists(timeout=10), msg='视频列表没有显示文件夹')
        self.screenshot()

        self.d(text="File").click(timeout=5)
        self.d(text="app_video.mp4").click(timeout=5)
        num = self.d(resourceId=res['com.app.videoplayer:id/tvNum']).get_text(timeout=5)
        self.assertEqual(num, '(1)', msg='红点数字不正确')
        self.screenshot()

        self.d(text="Send").click(timeout=5)
        self.d(text="Allow").click(timeout=5)
        self.d(text="允许").click(timeout=5)
        self.assertTrue(self.d(text='Scan QR code').exists(timeout=10), msg='打开扫码页失败')
        self.screenshot()



    @testcase
    def test_03_me_mp3_converter(self):
        """检查MP3 Converter"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=5)
        self.d(text="MP3 Converter").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivAdd']).click()
        self.d(text="Android").click(timeout=5)
        self.d(text="音乐盒.ogg").click(timeout=5)
        self.d(text="Convert").click(timeout=5)
        self.d(text="Got It").click(timeout=5)
        self.screenshot()
        self.assertTrue(self.d(text="音乐盒").exists(timeout=5),msg='没有发现音频文件')
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click()
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        self.d(text="Delete").click(timeout=5)
        self.d(text="OK").click(timeout=5)
        self.d.press('back')

    @testcase
    def test_04_me_downloads(self):
        """检查Downloads"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=10)
        self.d(text="Downloads").click(timeout=5)
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/flCover']).exists(timeout=5),
                        msg='下载管理器没有显示下载记录')
        self.screenshot()

        ###### 移动到隐私文件夹
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
        self.d(text='Move into Privacy Folder').click(timeout=5)
        self.d(text='Yes').click(timeout=5)


    @testcase
    def test_05_me_privacy_folder(self):
        """检查隐私文件夹"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=10)
        self.d(text="Downloads").click(timeout=5)
        self.assertTrue(self.d(text='Go to download').exists(timeout=5), msg='视频移入隐私文件夹失败')
        self.screenshot()
        self.d.press('back')



    @testcase
    def test_06_me_history(self):
        """检查History"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=10)
        self.d(text="History").click(timeout=10)
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='播放记录不存在')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_07_me_theme(self):
        """检查Theme"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=5)
        self.d(text="Featured Theme").click(timeout=5)
        self.d.click(0.274, 0.563)
        self.screenshot()

        ###### 白色主题
        self.d(text="Use").click(timeout=5)
        self.assertTrue(self.d(text="In use").exists(timeout=10), msg='切换白色主题失败')
        self.screenshot()
        self.d.press('back')
        time.sleep(2)

        ###### 黑色主题
        self.d.click(0.759, 0.263)
        self.d(text="Use").click(timeout=5)
        self.assertTrue(self.d(text="In use").exists(timeout=10), msg='切换黑色色主题失败')

        self.screenshot()
        self.d.press('back')
        self.d.press('back')

    @testcase
    def test_08_me_feedback(self):
        """检查Feedback"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=5)
        self.d(text="Help & Feedback").click(timeout=5)
        self.assertTrue(self.d(text="FAQ").exists(timeout=60), msg='打开反馈页面失败')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_09_me_rateus(self):
        """检查Rate us"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=5)
        self.d(text="Rate us").click(timeout=5)
        rateId = res['com.app.videoplayer:id/ratingBar']
        self.d.xpath(f'//*[@resource-id="{rateId}"]/android.widget.ImageView[5]').click(timeout=5)
        self.screenshot()
        self.d(text="Submit").click(timeout=5)
        self.assertTrue(self.d(text="卸载").exists(timeout=60),msg='跳转GP失败')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_10_me_media_manage(self):
        """检查Media management"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=10)

        ###### 从 Media management入口
        self.d(text="Media Manage").click(timeout=5)
        self.assertTrue(self.d(text='Internal storage').exists(timeout=5),
                        msg='进入媒体管理失败')

        ###### 视频展示
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='视频没有展示')

        ###### 总空间计算
        all_space_text = str(self.d(resourceId=res['com.app.videoplayer:id/tvStorageSpace']).get_text(timeout=5)) \
            .replace('Used','').replace(' ','').split('/')[0]
        all_space_count = int(re.sub(r'[^0-9]', '', all_space_text))
        self.assertNotEqual(all_space_count, 0, msg='统计总大小异常')


        ###### 视频空间计算
        video_space_text = self.d(resourceId=res['com.app.videoplayer:id/tvVideoCountSpace']).get_text(timeout=5)
        video_space_count = int(re.sub(r'[^0-9]', '', video_space_text))
        self.assertNotEqual(video_space_count, 0, msg='统计视频大小异常')

        ###### 音乐空间计算
        music_space_text = self.d(resourceId=res['com.app.videoplayer:id/tvAudioCountSpace']).get_text(timeout=5)
        music_space_count = int(re.sub(r'[^0-9]', '', music_space_text))
        self.assertNotEqual(music_space_count, 0, msg='统计音乐文件大小异常')

        self.screenshot()

        ###### VIDEO列表展示
        self.d(text="VIDEO").click(timeout=5)
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='视频没有展示')
        self.screenshot()
        self.d.press('back')

        ###### MUSIC列表展示
        self.d(text="MUSIC").click(timeout=5)
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/tvSongName']).exists(timeout=5),
                        msg='MUSIC列表音频没有展示')
        self.screenshot()
        self.d.press('back')

        ###### all列表的视频展示
        self.d(resourceId=res['com.app.videoplayer:id/all']).click(timeout=5)
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='ALL列表音频没有展示')
        self.screenshot()
        self.d.press('back')

        ###### 从Downloads入口
        self.d.press('back')
        self.d(text="Downloads").click(timeout=5)
        self.d(resourceId='com.app.videoplayer:id/ivArrow').click(timeout=5)
        self.assertTrue(self.d(text='Internal storage').exists(timeout=5),
                        msg='从下载管理器进入媒体管理失败')
        self.screenshot()
        self.d.press('back')
        self.d.press('back')



    # @testcase
    # def test_11_me_followus(self):
    #     """检查Follow us"""
    #     app.case_restart_check(text='ME')
    #     self.d(text="ME").click(timeout=5)
    #     self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
    #     self.d(text="Follow us").click(timeout=5)
    #     self.d(text="以上都不是").click(timeout=5)
    #     self.screenshot()
    #     self.d.press('back')

    @testcase
    def test_12_me_about(self):
        """检查About"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=5)
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        self.d(text="About").click(timeout=5)

        ###### Join our group
        self.d(text="Join our group").click(timeout=5)
        action.exist_click(resourceId='com.vivo.browser:id/vivo_upgrade_cancelBtnLayout')
        self.assertTrue(self.d(className="com.vivo.chromium.WebViewAdapter").exists(timeout=10),msg='打开Join our group失败')
        self.screenshot()
        app.home_start()

        ###### Official app Website
        action.exist_click(resourceId='com.vivo.browser:id/vivo_upgrade_cancelBtnLayout')
        self.d(text="Official app Website").click(timeout=5)
        self.assertTrue(self.d(className="com.vivo.chromium.WebViewAdapter").exists(timeout=10),msg='Official app Website')
        self.screenshot()
        app.home_start()

        ###### Share app
        action.exist_click(resourceId='com.vivo.browser:id/vivo_upgrade_cancelBtnLayout')
        self.d(text="Share app").click(timeout=5)
        self.assertTrue(self.d(text="分享方式").exists(timeout=10), msg='打开Share app失败')
        self.screenshot()
        app.home_start()

        ###### Youtube Channel
        self.d(text="Youtube Channel").click(timeout=5)
        self.assertTrue(self.d(text="app Official").exists(timeout=10), msg='打开Youtube Channel失败')
        self.screenshot()
        self.d.click(0.076, 0.071)

        ###### Thank You
        self.d(text="Thank You").click(timeout=5)
        self.assertTrue(self.d(text="Join us").exists(timeout=10), msg='打开Thank You失败')
        self.screenshot()



    @testcase
    def test_13_coin_center(self):
        """检查金币中心"""
        app.case_restart_check(text='ME')
        self.d(text="ME").click(timeout=5)

        ###### ME页面的金币数量检查
        me_coin = int(self.d(resourceId=res['com.app.videoplayer:id/tvCoin']).get_text(timeout=5))
        self.assertNotEqual(me_coin, 0, msg='coin数量为0')

        self.d(text="My coin").click(timeout=5)

        ###### 任务中心的金币数量检查
        task_coin_before = int(self.d(resourceId=res['com.app.videoplayer:id/tv_coins_value']).get_text(timeout=10))
        self.assertEqual(task_coin_before, me_coin, msg='me页面的coin数量和任务中心的coin数量不一致')

        ###### 签到检查
        self.d(text="CHECK-IN").click(timeout=5)
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/tv_coins_value']).exists(timeout=3),msg='签到UI没有改变')
        sign_coin = int(self.d(resourceId=res['com.app.videoplayer:id/tv_coins_value']).get_text(timeout=10))
        self.assertNotEqual(task_coin_before,sign_coin,msg='签到金币没有累计')
        self.screenshot()

        ###### 任务金币收集
        self.d(text="Collect").click(timeout=5)
        time.sleep(2)
        self.assertFalse(self.d(text='Play a video').exists(timeout=3),msg='任务没有消失')
        task_coin = int(self.d(resourceId=res['com.app.videoplayer:id/tv_coins_value']).get_text(timeout=10))
        self.assertNotEqual(sign_coin, task_coin, msg='收集play a video的金币没有累计')
        self.screenshot()
        self.d.press('back')














