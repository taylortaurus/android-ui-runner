# coding: utf-8
# author: chenhongqing
from Public.appBase import *
import sys
import unittest
import os
import time

app = appBase()
class tab_video(unittest.TestCase, BasePage):
    """TAB VIDEO下面的功能检查"""

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start(app.pkg_name)

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop(app.pkg_name)


    @testcase
    def test_01_video_show(self):
        """检查新增视频展示"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        app.rate_skip()
        test_video_name = self.d(resourceId=res['com.app.videoplayer:id/tvVideoName']).get_text(timeout=5)
        flag = test_video_name not in ['app_video.mp4', 'pdisk_video.mp4', 'vidmate_video.mp4']
        self.assertEqual(flag,True,msg='新增的测试视频没有展示')
        self.screenshot()

    @testcase
    def test_02_more_rename(self):
        """检查MORE-Rename操作"""
        #app.case_restart_check(text='VIDEO')
        app.case_restart_check(restart=True)
        self.d(text="VIDEO").click(timeout=5)
        test_video_name = self.d(resourceId=res['com.app.videoplayer:id/tvVideoName']).get_text(timeout=5)
        if test_video_name not in ['app_video.mp4','pdisk_video.mp4','vidmate_video.mp4']:
            self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
            self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
            self.d(text="Rename").click()
            self.d(resourceId=res['com.app.videoplayer:id/edt']).clear_text()
            self.assertTrue(self.d(text="Enter a name").exists(timeout=5), msg='清除文本失败')
            self.d.send_keys('test_video')
            self.d(text="Commit").click(timeout=5)
            self.assertTrue(self.d(text="test_video.mp4").exists(timeout=5), msg='重命名失败')
            self.screenshot()
        else:
            self.screenshot()


    @testcase
    def test_03_more_mp3(self):
        """检查视频MORE-Convert to mp3操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
        self.d(text="Convert to mp3").click(timeout=5)
        self.assertTrue(self.d(text="Got It").exists(timeout=50), msg='转mp3异常')
        self.screenshot()
        self.d(text="Got It").click()

    @testcase
    def test_04_more_background_play(self):
        """检查视频MORE-Background Play操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
        self.d(text="Background play").click()
        self.d(text="MUSIC").click()
        ###### 判断是否有音乐栏在
        # todo:检查名称
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                         msg='Background Play失败')
        self.screenshot()
        self.d(resourceId=res['com.app.videoplayer:id/ivClose']).click()  # 关闭播放栏
        self.d(text="VIDEO").click()

    @testcase
    def test_05_more_favorate(self):
        """检查视频MORE-Favorate操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
        self.d(text="Favorite").click()
        ###### 判断是否收藏
        self.assertTrue(self.d(text="Remove favorite").exists(timeout=5),msg='Favorate失败')
        self.screenshot()
        self.d.press("back")
        self.d(text="Playlist").click()
        self.d(text="Favorite Videos").click()
        ###### 判断applist是否有收藏记录
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='Playlist没有收藏记录')
        self.screenshot()
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click()  # 更多按钮
        self.d(text="Remove favorite").click()  # 取消收藏
        self.assertTrue(self.d(text="Add Videos").exists(timeout=5),msg='取消收藏失败')
        self.screenshot()
        self.d(resourceId=res['com.app.videoplayer:id/ivLeft']).click()  # 返回
        self.d(resourceId=res['com.app.videoplayer:id/textView'], text="Video").click()  # Video tab

    @testcase
    def test_06_more_fileinfo(self):
        """检查视频MORE-File Info操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
        self.d(scrollable=True).scroll.toEnd() #滚动到最底部
        self.d(text="File info").click(timeout=5)
        ###### 判断是否弹出信息弹窗
        self.assertTrue(self.d(text="Information").exists(timeout=5),msg='没有显示文件信息弹窗')
        self.d(text="More").click(timeout=5)
        self.assertTrue(self.d(text="Stream 1").exists(timeout=5),msg='more下面没有显示信息')
        self.screenshot()
        self.d(text="CLOSE").click()

    @testcase
    def test_07_more_add_to_playlist(self):
        """检查视频MORE-Add to playlist操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)# 点击more
        self.d(text="Add to playlist").click(timeout=5)
        self.d(text="New playlist").click(timeout=5)
        self.d.send_keys("aaaa888")
        self.d(text="Commit").click()
        self.d(text="Playlist").click()
        self.d(text="aaaa888").click(timeout=5)
        ###### 判断是否添加视频到playlist
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='添加playlist失败')
        self.screenshot()
        ###### 删除playlist记录
        self.d(resourceId=res['com.app.videoplayer:id/ivSkinMore']).click()
        self.d(text="Delete playlist").click(timeout=5)
        self.d(text="OK").click(timeout=5)
        time.sleep(2)
        self.assertFalse(self.d(text="aaaa888").exists(timeout=5),msg='删除playlist失败')
        self.screenshot()
        self.d(text="Video").click(timeout=5)

    @testcase
    def test_08_search_youtube_videoplay(self):
        """检查首页搜索youtube视频播放"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivSearch']).click(timeout=5) #点击搜索按钮
        self.d.send_keys("Happy Holi")
        self.d(text="SEARCH").click()  # 搜索

        ###### 检查搜索结果
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/ivCover']).exists(timeout=5),
                        msg='搜索无结果')
        self.screenshot()

        ###### 检查播放是否异常
        self.d(resourceId=res['com.app.videoplayer:id/ivCover']).click(timeout=5)
        self.d(text='Full screen').click(timeout=5)
        VdieoPlay.video_error_feedback()
        self.screenshot()

    @testcase
    def test_09_more_mute_play(self):
        """检查视频MORE-Mute play操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
        time.sleep(2)
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        self.d(text="Mute play").click(timeout=5)
        VdieoPlay.play_video_skip()

        ###### 时间走动验证
        video_play = VdieoPlay.video_play_time_check()
        self.assertNotEqual(video_play[0], video_play[1], msg='播放时间没有跑动')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_10_change_arrange(self):
        """检查视频排列展示"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)

        ###### 网络模式
        self.d(resourceId=res['com.app.videoplayer:id/ivChangeType']).click(timeout=5)
        time.sleep(2)
        self.assertFalse(self.d(resourceId='com.app.videoplayer:id/tvFolderName').exists(timeout=5),
                        msg='网络模式切换失败')
        self.screenshot()

        ###### 列表模式
        self.d(resourceId=res['com.app.videoplayer:id/ivChangeType']).click(timeout=5)
        time.sleep(2)
        self.assertTrue(self.d(resourceId='com.app.videoplayer:id/tvFolderName').exists(timeout=5),
                         msg='列表模式切换失败')

    @testcase
    def test_11_video_sort(self):
        """检查视频排序"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)

        ###### 按size排序
        self.d(resourceId=res['com.app.videoplayer:id/ivSort']).click(timeout=5)
        self.d(text='Size').click(timeout=5)
        self.d(text='OK').click(timeout=5)
        time.sleep(2)
        test_video_name = self.d(resourceId=res['com.app.videoplayer:id/tvVideoName']).get_text(timeout=5)
        self.assertEqual(test_video_name,'pdisk_video.mp4',msg='size排序切换失败')
        self.screenshot()

        ###### 按date排序
        self.d(resourceId=res['com.app.videoplayer:id/ivSort']).click(timeout=5)
        self.d(text='Date').click(timeout=5)
        self.d(text='OK').click(timeout=5)
        time.sleep(2)
        test_video_name = self.d(resourceId=res['com.app.videoplayer:id/tvVideoName']).get_text(timeout=5)
        self.assertEqual(test_video_name,'test_video.mp4', msg='date排序切换失败')
        self.screenshot()

    @testcase
    def test_12_more_delete(self):
        """检查视频MORE-Delete操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(resourceId=res['com.app.videoplayer:id/ivMore']).click(timeout=5)
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        self.d(text="Delete").click(timeout=5)
        self.d(text="OK").click(timeout=5)
        time.sleep(2)
        self.assertFalse(self.d(text="test_video.mp4").exists(timeout=5), msg='删除视频失败')
        self.screenshot()

    @testcase
    def test_13_app_video_play(self):
        """检查app下载视频播放"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(text="Video").click(timeout=5)
        self.d(text='app_video.mp4').click(timeout=5)  # 点击视频
        VdieoPlay.play_video_skip()

        ###### 时间走动验证 ######
        video_play = VdieoPlay.video_play_time_check()
        self.assertNotEqual(video_play[0], video_play[1], msg='播放时间没有跑动')
        self.screenshot()

        # ###### 暂停播放 ######
        # time.sleep(4)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # self.d(resourceId=res['com.app.videoplayer:id/play_btn']).click(timeout=5)
        # self.screenshot()
        # playtime_pre = self.d(resourceId=res['com.app.videoplayer:id/has_played']).get_text(timeout=5)
        # time.sleep(10)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # playtime_next = self.d(resourceId=res['com.app.videoplayer:id/has_played']).get_text(timeout=5)
        # if playtime_pre != playtime_next: raise ('播放时间没有跑动')
        #
        #
        # ###### 下一首 ######
        # time.sleep(4)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # video_title_1 = self.d(resourceId=res['com.app.videoplayer:id/player_title']).get_text(timeout=5)
        # time.sleep(4)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # self.d(resourceId=res['com.app.videoplayer:id/next_btn']).click(timeout=5)
        # video_title_2 = self.d(resourceId=res['com.app.videoplayer:id/player_title']).get_text(timeout=5)
        # if video_title_1 == video_title_2: raise ('下一首切换失败')
        #
        # ###### 上一首 ######
        # time.sleep(4)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # self.d(resourceId=res['com.app.videoplayer:id/previous_btn']).click(timeout=5)
        # video_title_3 = self.d(resourceId=res['com.app.videoplayer:id/player_title']).get_text(timeout=5)
        # if video_title_3 == video_title_2: raise ('上一首切换失败')
        #
        # ###### 后台播放 ######
        # time.sleep(4)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # self.d(resourceId=res['com.app.videoplayer:id/music']).click(timeout=5)
        # self.d(text='Back to video').click(timeout=5)
        # self.d.press('back')
        #
        # ###### 锁定屏幕 ######
        # time.sleep(4)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # self.d(resourceId=res['com.app.videoplayer:id/lock']).click(timeout=5)
        # self.screenshot()
        # time.sleep(5)
        # self.d.click(0.431, 0.232)  # 高亮屏幕
        # if self.d(resourceId=res['com.app.videoplayer:id/play_btn']).exists(timeout=5): raise ('锁屏失败')
        # self.d(resourceId=res['com.app.videoplayer:id/lock']).click(timeout=5)

        # todo: 外部拉起（pdisk\vidmate\本地）
        # todo: 播放细节检查：横竖屏、上下一首、后台播放、小窗播放、截屏、更多操作（软硬解、cut、equalizer、info、feedback、tutorials）

    @testcase
    def test_14_vidmate_video_play(self):
        """检查vidmate下载视频播放"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(text="Video").click(timeout=5)
        self.d(text='vidmate_video.mp4').click(timeout=5)  # 点击视频
        VdieoPlay.play_video_skip()

        ###### 时间走动验证
        video_play = VdieoPlay.video_play_time_check()
        self.assertNotEqual(video_play[0], video_play[1], msg='播放时间没有跑动')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_15_pdisk_video_play(self):
        """检查pdisk下载视频播放"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(text='pdisk_video.mp4').click(timeout=5)  # 点击视频
        VdieoPlay.play_video_skip()

        ###### 时间走动验证
        video_play = VdieoPlay.video_play_time_check()
        self.assertNotEqual(video_play[0], video_play[1], msg='播放时间没有跑动')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_16_play_histoty(self):
        """检查history视频播放"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(text="Video").click(timeout=5)

        ###### 判断是否有播放记录
        self.assertTrue(self.d(resourceId=res['com.app.videoplayer:id/img_video_history']).exists(timeout=5),
                        msg='播放本地视频无播放记录')
        self.screenshot()

        ###### history play
        self.d(resourceId=res['com.app.videoplayer:id/rlParent']).click(timeout=5)
        VdieoPlay.play_video_skip()

        ###### 时间走动验证
        video_play = VdieoPlay.video_play_time_check()
        self.assertNotEqual(video_play[0], video_play[1], msg='播放时间没有跑动')
        self.screenshot()
        self.d.press('back')

    @testcase
    def test_17_video_folder(self):
        """检查视频文件夹操作"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(text="Folder").click(timeout=5)

        ###### 判断文件夹展示
        folder_exist = self.d(text="app").exists(timeout=5) and self.d(text="VidMate").exists(timeout=5)
        self.assertTrue(folder_exist, msg='文件夹没有展示')
        self.screenshot()

        ###### 判断文件夹的视频展示
        self.d(text="app").click(timeout=5)
        self.assertTrue(self.d(text="app_video.mp4").exists(timeout=5), msg='文件夹没有展示视频文件')
        self.screenshot()
        self.d(text="FOLDER").click(timeout=5)
        self.assertTrue(self.d(text="download").exists(timeout=5), msg='download文件夹没有展示')
        self.screenshot()

        self.d.press('back')

        ###### 文件夹排列切换
        self.d(resourceId=res['com.app.videoplayer:id/ivChangeType']).click(timeout=5)
        self.assertTrue(self.d(resourceId="com.app.videoplayer:id/ivArrow").exists(timeout=5), msg='列表模式切换失败')
        self.screenshot()

        self.d(resourceId=res['com.app.videoplayer:id/ivChangeType']).click(timeout=5)
        time.sleep(5)
        self.assertFalse(self.d(resourceId="com.app.videoplayer:id/ivArrow").exists(), msg='网络模式切换失败')
        self.screenshot()

    @testcase
    def test_18_manage_scan_list(self):
        """扫描文件夹"""
        app.case_restart_check(text='VIDEO')
        self.d(text="VIDEO").click(timeout=5)
        self.d(text="Folder").click(timeout=5)

        ###### 判断文件夹的视频展示

        self.d(text="Manage your scan list").click(timeout=5)
        self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
        eyeID = res['com.app.videoplayer:id/recyclerView']
        self.d.xpath(
            f'//*[@resource-id="{eyeID}"]/android.view.ViewGroup[8]/android.widget.ImageView[2]').click(timeout=5)
        self.screenshot()
        self.d.press('back')
        self.assertFalse(self.d(text="VidMate").exists(timeout=5), msg='VidMate文件夹隐藏失败')
        self.screenshot()

        self.d(text="Manage your scan list").click(timeout=5)
        self.d.xpath(
            f'//*[@resource-id="{eyeID}"]/android.view.ViewGroup[1]/android.widget.ImageView[2]').click(timeout=5)
        self.d.press('back')
        self.assertTrue(self.d(text="VidMate").exists(timeout=5), msg='恢复文件夹失败')
        self.screenshot()



















