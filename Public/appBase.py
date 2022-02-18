# coding: utf-8
import sys
import os
from Public.Decorator import *
import uiautomator2 as u2
from Public.common import common
from tenacity import *



cm = common()
#获取resourceID
condition = os.path.exists(cm.mapping_gp_path)
mapping_path = (cm.mapping_vid_path,cm.mapping_gp_path)[condition]
res = cm.parse_mapping_file(mapping_path, condition)

class appBase(common):
    """app基础处理"""

    def __init__(self):
        self.d = u2.connect()
        self.apk_path = cm.apk_rel_path
        self.pkg_name = cm.pkg_name
        self.d.screen_on() # 打开屏幕
        self.d.unlock() # 解锁屏幕
        self.d.press('home') # 回到桌面

    @exception_decoration
    def rate_skip(self):
        action.exist_click(text='Exit')

    @exception_decoration
    def case_restart_check(self,text=None,resourceId=None,restart=False):
        """用例是否重起检查"""
        if text is not None:
            self.d(text=text).click(timeout=2)
        elif resourceId is not None:
            self.d(resourceId=text).click(timeout=2)
        elif restart is True:
            raise Exception('restart')


    @exception_decoration
    def vip_check(self):
        """VIP检查"""
        self.d(text="ME").click(timeout=2)
        if not self.d(text='You are already a VIP').exists(timeout=5):  # vip标识
            self.d(text='3-Day Free Trial').click(timeout=2)
            self.d(text="CONTINUE").click(timeout=5)
            self.d(text="订阅").click(timeout=5)
            action.exist_click(text='以后再说')
            action.exist_click(text='不用了')
            action.exist_click(text='确定')
            action.exist_click(text='Done')
            self.d(text="xxx").click(timeout=5)
        print('vip检查通过')

    @exception_pass
    def startpage_handle(self):
        """启动开屏页处理"""
        self.d(resourceId="com.android.permissioncontroller:id/permission_allow_button").click(timeout=5)
        self.d(text="Skip").click(timeout=2)
        self.d(text="Got It").click(timeout=2)
        print('启动开屏页检查通过')

    @exception_pass
    def clear_home_xxx(self):
        """删除首页的xxx"""
        self.d(text="xxx").click(timeout=2)
        test_xxx_name = self.d(resourceId=res['com.app.xxxxxx:id/tvxxxName']).get_text(timeout=10)
        while test_xxx_name not in ['xxx_xxx.mp4','app_xxx.mp4','xxx_xxx.mp4']:
            self.d(resourceId=res['com.app.xxxxxx:id/ivMore']).click()
            self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
            self.d(text="Delete").click(timeout=2)
            self.d(text="OK").click(timeout=2)
            test_xxx_name = self.d(resourceId=res['com.app.xxxxxx:id/tvxxxName']).get_text(timeout=10)
        print('清理测试视频检查通过')

    @exception_pass
    def clear_downloaded_xxx(self):
        """删除下载管理器记录"""
        while not self.d(text='Go to download').exists(timeout=2):
            self.d(resourceId=res['com.app.xxxxxx:id/ivMore']).click(timeout=2)
            self.d(text="Delete").click(timeout=2)
            self.d(text="Confirm").click(timeout=2)
        print('清理下载管理器记录通过')

    @exception_pass
    def clear_music(self):
        """删除下音乐记录"""
        self.d(text="MUSIC").click(timeout=2)
        music_title = self.d(resourceId=res['com.app.xxxxxx:id/tvSongName']).get_text(timeout=2)
        while 'test_music1' not in music_title:
            self.d(resourceId=res['com.app.xxxxxx:id/ivMore']).click(timeout=2)
            self.d(scrollable=True).scroll.toEnd()  # 滚动到最底部
            self.d(text="Delete").click(timeout=2)
            self.d(text="OK").click(timeout=2)
            music_title = self.d(resourceId=res['com.app.xxxxxx:id/tvSongName']).get_text(timeout=2)
        self.d(text="xxx").click(timeout=2)
        print('清除音乐文件通过')

    @exception_pass
    def music_permission(self):
        """音乐权限处理"""
        self.d(text="Ok").click(timeout=3)
        self.d(text="允许").click(timeout=3)

    @retry(stop=stop_after_attempt(2))
    def download_xxx(self):
        """下载视频"""
        #下载新的视频
        self.case_restart_check(text='DOWNLOAD')
        self.d(text="DOWNLOAD").click(timeout=2)

        ###### 清理下载记录
        self.d(resourceId=res['com.app.xxxxxx:id/ivDownload']).click()
        self.clear_downloaded_xxx()
        self.d.press('back')

        self.d(resourceId=res['com.app.xxxxxx:id/clSearch']).click(timeout=2)
        self.d.send_keys("https://www.ted.com/talks/armand_d_angour_the_ancient_origins_of_the_olympics/up-next")
        self.d.press('enter')
        self.d(resourceId=res['com.app.xxxxxx:id/button_analytics']).click(timeout=10)
        time.sleep(10)
        if not str(self.d(resourceId=res['com.app.xxxxxx:id/text_size']).get_text(timeout=10)).__contains__('MB'):
            time.sleep(10)
        self.d(text="Download").click(timeout=5)
        self.d(text="view >").click(timeout=5)
        if not self.d(resourceId=res['com.app.xxxxxx:id/flCover']).exists(timeout=2): raise ('下载管理器没有视频')
        check_text = time.strftime("%Y-%m-%d", time.localtime())
        suc_text = self.d(resourceId=res['com.app.xxxxxx:id/tvDownloaded']).get_text(timeout=240)
        if check_text not in suc_text:
            raise ('测试视频下载超时未完成')
        self.d(resourceId=res['com.app.xxxxxx:id/ivLeft']).click(timeout=2)
        self.d.press('back')
        self.d.press('back')
        self.d(text="xxx").click(timeout=1)
        print('下载视频通过')


    @exception_pass
    def clear_notification(self):
        """清理通知栏消息"""
        self.d.open_notification()
        self.d(text='全部清除').click(timeout=2)


    def home_start(self,text=None,resourceId=None):
        """home键再打开app"""
        self.d.press('home')
        self.d.app_start(self.pkg_name)
        if text is not None:
            self.d(text=text).click(timeout=5)
        elif resourceId is not None:
            self.d(resourceId=resourceId).click(timeout=5)


    def xxx_xxx_check(self,xxxlink):
        """检查xxx热剧"""
        self.case_restart_check(text='DOWNLOAD')
        self.d(text="DOWNLOAD").click(timeout=2)
        self.d(resourceId=res['com.app.xxxxxx:id/clSearch']).click(timeout=2)
        self.d.send_keys(xxxlink)
        self.d.xpath('//*[@resource-id="app"]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[4]/android.view.View[1]').click(timeout=20)
        self.d(scrollable=True).scroll.toEnd()
        self.d.click(0.596, 0.808)
        self.d(resourceId=res['com.app.xxxxxx:id/iv_close']).click(timeout=20)
        self.d.click(0.431, 0.232)  # 高亮屏幕
        playtime_pre = self.d(resourceId=res['com.app.xxxxxx:id/has_played']).get_text(timeout=2)
        time.sleep(10)
        self.d.click(0.431, 0.232)  # 高亮屏幕
        playtime_next = self.d(resourceId=res['com.app.xxxxxx:id/has_played']).get_text(timeout=2)
        if playtime_pre == playtime_next: raise Exception('播放时间没有跑动')
        self.d.screenshot()




class VdieoPlay(appBase):

    d = u2.connect()

    @classmethod
    @exception_pass
    def play_xxx_skip(cls):
        """处理播放引导"""
        cls.d(resourceId=res['com.app.xxxxxx:id/svgOrientation']).click(timeout=5)
        cls.d(text="skip").click(timeout=2)  # 跳过播放引导
        cls.d(text="Skip").click(timeout=2)  # 跳过播放引导

    @classmethod
    def xxx_error_feedback(cls):
        """视频异常反馈"""
        if cls.d(text='Error!').exists(timeout=10):
            cls.d.screenshot()
            cls.d(text='Feedback').click(timeout=2)
            cls.d(text='Submit').click(timeout=2)
            raise Exception('视频异常')

    @classmethod
    def xxx_play_time_check(cls):
        """视频播放检查"""
        ###### 时间走动验证 ######
        cls.d.click(0.431, 0.232)  # 高亮屏幕
        playtime_pre = cls.d(resourceId=res['com.app.xxxxxx:id/has_played']).get_text(timeout=2)
        time.sleep(10)
        cls.d.click(0.431, 0.232)  # 高亮屏幕
        playtime_next = cls.d(resourceId=res['com.app.xxxxxx:id/has_played']).get_text(timeout=2)
        cls.d.screenshot()
        return playtime_pre, playtime_next

class action:

    d = u2.connect()

    @classmethod
    def exist_click(cls,text=None,resourceId=None):
        """存在操作"""
        if text is not None and cls.d(text=text).exists(timeout=3):
            cls.d(text=text).click()
        elif resourceId is not None and cls.d(resourceId=resourceId).exists(timeout=3):
            cls.d(resourceId=resourceId).click()

    @classmethod
    def screenshot_name(cls,name):
        """按照名称截图"""
        date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screenshot = name + '-' + date_time + '.PNG'
        # path = ReportPath().get_path() + '/' + screenshot
        path = os.path.join(ReportPath().get_path(), screenshot)
        cls.d.screenshot(path)
        return screenshot




if __name__ == '__main__':
    print(res['com.app.xxxxxx:id/tvGotIt'])



