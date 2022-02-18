### Android-UI-Runner

```
基于Uiautomator2+Python-Unittest的UI自动化测试框架
https://github.com/openatx/uiautomator2

uiautomator2是一个python库，用于Android的UI自动化测试，其底层基于Google uiautomator，Google提供的
uiautomator库可以获取屏幕上任意一个APP的任意一个控件属性，并对其进行任意操作

python-uiautomator2主要分为两个部分，python客户端，移动设备
	
1、python端: 运行脚本，并向移动设备发送HTTP请求
	
2、移动设备：移动设备上运行了封装了uiautomator2的HTTP服务，解析收到的请求，并转化成uiautomator2的代码。


整个过程
	
1、在移动设备上安装atx-agent(守护进程), 随后atx-agent启动uiautomator2服务(默认7912端口)进行监听
	
2、在PC上编写测试脚本并执行（相当于发送HTTP请求到移动设备的server端）
	
3、移动设备通过WIFI或USB接收到PC上发来的HTTP请求，执行制定的操作

```
<a  target="_blank">
<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1643183387082-0b352e36-56ba-4971-8e5d-228bd555885d.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0">
</a>
### 环境要求
```
1.安装uiautomator2: pip3 install -U uiautomator2
2.Python版本:3.6+ 
3.Android版本:4.4+
```

### 定位工具
```
安装weditor
pip3 install weditor
python3 -m weditor
```

### Unittest断言
```py
self.assertEqual(value1, value2, failedinfo) # 断言value1 == value2

self.assertNotEqual(value1, value2, failedinfo) # 断言value1 != value2

self.assertTrue(表达式, failedinfo) # 断言value为真

self.assertFalse(表达式, failedinfo) # 断言value为假
```

### 依赖安装
```
pip3 install -r requirements.txt
```
### 自动化服务
```
地址：http://14.23.91.210:8082/job/android-ui-runner
账号密码：android-ui-runner/zhuanhaiyuan
```
### 工程介绍
**Public：** 
```
- common.py 公共处理的方法
- Devices_new.py 获取atx-server上特定设备（get_online_devices()）、或config.ini下devices IP列表的在线设备（get_devices()）、有线连接电脑的设备自动连接u2（connect_devices()）
- BasePage.py 用于设备的初始化 u2.connect  已经一些公共模块的封装
- chromedriver.py 和Ports.py 结合使用，启动chromedriver以便实现u2的webview操作（目前还没做到根据设备的chromeversion 启动指定版本的chromedriver）
- Casestrategy.py 获取指定路径下的testcases
- Decorator.py 装饰器用例执行日志打印、错误后的处理（截图）
- Report.py  对生成的报告的一些操作，备份Testreport的报告到TestReport_backup下、多设备统一报告的生成、报告的文件夹压缩
- Test_data.py 在执行测试前的测试数据的生成，会在Plubic下生成data.json，测试执行的时候各个设设备更具自己的serial获取对应的测试数据
- Drivers.py  设备的获取，初始化准备，测试执行都是在这里完成的
- RunCases.py 存放测试报告/日志/截图的路径的生成，以及最终通过HTMLTestRunner来执行用例 
- config.ini 一些需要用到的数据，atx-server地址、测试设备的ip、测试数据等
- app.py 项目公共处理的步骤

```
**run_cases .py** 

```py
1.打包完成后，将apk、mapping等信息传给ui自动化的服务
2.下载apk和mapping文件到对应的目录
​3.根据mapping文件解析拿到混淆后的ResourceId
​4.执行完case将报告放到tomcat，钉钉发送结果

if __name__ == '__main__':
     fileinfo={
        "apk":{
            "file_link":apk_link,
            "file_dir":apk_dir,
            "file_name":apk_name
            },
        "mapping":{
            "file_link": mapping_link,
            "file_dir": mapping_dir,
            "file_name": 'mapping.zip'
        }
     }

    cm = common()
    filetypes = ['apk','mapping']
    #多进程下载apk和mapping文件
    pool = multiprocessing.Pool(processes=len(filetypes))
    for filetype in filetypes:
        pool.apply_async(cm.download_from_url,args=(fileinfo[filetype]['file_link'],
                                                fileinfo[filetype]['file_dir'],
                                                fileinfo[filetype]['file_name'],))
    pool.close()
    pool.join()
    # 匹配case
    cs = CaseStrategy(suite_path='testsuite',case_path='case',case_pattern='test*.py')
    cases = cs.collect_cases(suite=False)
    # 执行case
    result = Drivers().run(cases)
    pass_num = result['pass']
    fail_num = result['fail']
    error_num = result['error']
   
```

**Driver.py** 
```py
1.首先根据config.ini中`method`的值来判断从atx-serve获取online的设备 还是从config.ini中的ip来获取在线的设备
2.在获取到设备之后，根据设备生产data.json测试数据
​3.并行多设备执行测试
​4.测试完之后，杀掉执行过程中打开的所有的chromedriver进程
​5.最后在TestReport下生成统计测试报告（自动化测试报告.html)
   
    def run(self, cases):
        start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devives()
        if not devices:
            logger.info('There is no device found,test over.')
            return

        logger.info('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        runs = []
        for i in range(len(devices)):
            runs.append(RunCases(devices[i]))
        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_cases,
                             args=(run, cases,))
        logger.info('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        logger.info('All runs done........ ')
        ChromeDriver.kill()

        #  Generate statistics report  生成统计测试报告 将所有设备的报告在一个HTML中展示
        result = create_statistics_report(runs)
        return result[0]
```
**test_01_case.py** 

```
    def test_01_music_show(self):
        """检查音频文件展示"""
        app.case_restart_check(text='MUSIC')//j检查当前位置是否为（text='MUSIC'），不是增重启
        self.d(text="MUSIC").click(timeout=2)
        self.assertTrue(self.d(text="test_xxx").exists(timeout=2),msg='新增的音频文件没有展示')//断言成功通过，失败截图，下一个用例
        self.screenshot()
```        


#### Monkey执行
```py
进入Monkey目录，执行：python3 monkey_run.py 包名 执行时间（分钟） 点击延迟时间（毫秒）
例子：python3 monkey_run.py com.nemo.starhalo 10 200
报告在MaxiReport_History目录

说明：
client.log：手机设备的log
logcat.log：app的log
monkeyout.txt：monkey正常流的log
monkeyerr.txt：monkey的错误log
crash-dump.log：崩溃日志（如果发生崩溃才有）
oom-traces.log：内存溢出日志（发生了内存溢出才有）
```

### U2 API 


**应用操作**
```py
d.app_install('http://some-domain.com/some.apk') #引号内为下载apk地址

d.app_start('com.ruguoapp.jike') #引号内为包名称

sess = d.session("com.netease.cloudmusic") # start 网易云音乐，Session表示应用程序的生命周期

d.app_stop('com.example.hello_world')  #相当于'am force-stop'强制停止应用

d.app_clear('com.example.hello_world') #相当于'pm clear' 清空App数据

d.app_stop_all() # 停止所有

d.app_stop_all(excludes=['com.examples.demo']) # 停止所有应用程序，除了com.examples.demo

sess.close() # 停止网易云音乐
```

**跳过弹窗，禁止弹窗**

```py
d.disable_popups（）#自动跳过弹出窗口 

d.disable_popups（false）#禁用自动跳过弹出窗
```

**检测应用崩溃**
```py
# App正在运行时
sess(text="Music").click() # 操作是正常的

# App崩溃时
sess(text="Music").click() # 引发会话中断错误SessionBrokenError
```
**获取应用信息**
```py
d.app_info("com.examples.demo")
# 会输出
#{
#    "mainActivity": "com.github.uiautomator.MainActivity",
#    "label": "ATX",
#    "versionName": "1.1.7",
#    "versionCode": 1001007,
#    "size":1760809
#}

# 保存应用程序图标
img = d.app_icon("com.examples.demo")
img.save("icon.png")
```
**推拉文件**
```py
d.push("foo.txt", "/sdcard/") # push文件夹

d.push("foo.txt", "/sdcard/bar.txt") # push和重命名

# push fileobj
with open("foo.txt", 'rb') as f:
    d.push(f, "/sdcard/")

d.push("foo.sh", "/data/local/tmp/", mode=0o755) # 推动和更改文件访问模式

d.pull("/sdcard/tmp.txt", "tmp.txt") # 如果在设备上找不到文件，FileNotFoundError将引发

d.pull("/sdcard/some-file-not-exists.txt", "tmp.txt")
```
**操作屏幕**
```py
d.info.get（' screenOn '）#需要 Android> = 4.4

d.screen_on（）＃打开屏幕 

d.screen_off（）＃关闭屏幕

d.unlock()  # 解锁屏幕（相当于 发射活动:com.github.uiautomator.ACTION_IDENTIFY， 按home键）

d.freeze_rotation()# 冻结旋转

d.freeze_rotation(False)# 开启旋转

截图

# 截图并保存到电脑上的一个文件中，需要Android>=4.2。

d.screenshot("home.jpg")
 
# 得到PIL.Image格式的图像. 但你必须先安装pillow

image = d.screenshot() # default format="pillow"
image.save("home.jpg") # 或'home.png'，目前只支持png 和 jpg格式的图像
 
# 得到OpenCV的格式图像。当然，你需要numpy和cv2安装第一个

import cv2
image = d.screenshot(format='opencv')
cv2.imwrite('home.jpg', image)
 
# 获取原始JPEG数据

imagebin = d.screenshot(format='raw')
open("some.jpg", "wb").write(imagebin)
```
**操作通知栏**
```py
d.open_notification（）#下拉打开通知栏

d.open_quick_settings（）#下拉打开快速设置栏
```

**硬键盘和软键盘操作**
```py
d.press("home") # 点击home键

d.press("back") # 点击back键

d.press("left") # 点击左键

d.press("right") # 点击右键

d.press("up") # 点击上键

d.press("down") # 点击下键

d.press("center") # 点击选中

d.press("menu") # 点击menu按键

d.press("search") # 点击搜索按键

d.press("enter") # 点击enter键

d.press("delete") # 点击删除按键

d.press("recent") # 点击近期活动按键

d.press("volume_up") # 音量+

d.press("volume_down") # 音量-

d.press("volume_mute") # 静音

d.press("camera") # 相机

d.press("power") #电源键
```
**UI对象定位方式**
```py
text、resourceId、description、className、xpath、坐标

d(text="Settings").click()  #text定位单击

d(text="Settings", className="android.widget.TextView").click()

d(resourceId="com.ruguoapp.jike:id/tv_title", className="android.widget.TextView").click()   #resourceId定位单击

d(description="设置").click()  #description定位单击

d(description="设置", className="android.widget.TextView").click()

d(className="android.widget.TextView").click()  #className定位单击

d.xpath("//android.widget.FrameLayout[@index='0']/android.widget.LinearLayout[@index='0']").click()  #xpath定位单击

d.click(182, 1264) #坐标单击

d(text="Settings").click(timeout=10)  # 等待元素出现(最多10秒），出现后单击 

d(text='Skip').click_exists(timeout=10.0) # 在10秒时点击，默认的超时0

d(text="Skip").click_gone(maxretry=10, interval=1.0) # 单击直到元素消失，返回布尔 ，maxretry默认值10,interval默认值1.0 

d(text="Settings").click(offset=(0.5, 0.5)) # 点击基准位置偏移 点击中心位置，同d(text="Settings").click()

d(text="Settings").click(offset=(0, 0)) # 点击左前位置

d(text="Settings").click(offset=(1, 1)) # 点击右下

d(text="Settings").wait(timeout=3.0) ## 等待ui对象出现，返回布尔值

d(text="Settings").wait_gone(timeout=1.0)  # 等待ui对象的消失
```
**执行双击UI对象**
```py
d(text="设置").double_click() #双击特定ui对象的中心

d.double_click(x, y, 0.1)#两次单击之间的默认持续时间为0.1秒
```
**执行长按UI对象**
```py
d(text="Settings").long_click() # 长按特定UI对象的中心

d.long_click(x, y, 0.5) # 长按坐标位置0.5s默认
```
**将UI对象拖向另一个点或另一个UI对象**
```py
# Android<4.3不能使用drag.

d(text="Settings").drag_to(x, y, duration=0.5)  # 在0.5秒内将UI对象拖到屏幕点(x, y)

d(text="Settings").drag_to(text="Clock", duration=0.25) # 将UI对象拖到另一个UI对象的中心位置，时间为0.25秒
```
**左右操作**
```py
d(text="Settings").swipe("right")

d(text="Settings").swipe("left", steps=10)

d(text="Settings").swipe("up", steps=20) # 1步约为5ms, 20步约为0.1s

d(text="Settings").swipe("down", steps=20)

d(text="Settings").gesture((sx1, sy1), (sx2, sy2), (ex1, ey1), (ex2, ey2))

d.swipe_ext("right") # 手指右滑，4选1 "left", "right", "up", "down"
d.swipe_ext("right", scale=0.9) # 默认0.9, 滑动距离为屏幕宽度的90%
d.swipe_ext("right", box=(0, 0, 100, 100)) # 在 (0,0) -> (100, 100) 这个区域做滑动

# 实践发现上滑或下滑的时候，从中点开始滑动成功率会高一些
d.swipe_ext("up", scale=0.8) # 代码会vkk

# 还可以使用Direction作为参数
from uiautomator2 import Direction

d.swipe_ext(Direction.FORWARD) # 页面下翻, 等价于 d.swipe_ext("up"), 只是更好理解
d.swipe_ext(Direction.BACKWARD) # 页面上翻
d.swipe_ext(Direction.HORIZ_FORWARD) # 页面水平右翻
d.swipe_ext(Direction.HORIZ_BACKWARD) # 页面水平左翻
```
**滚动操作**
```py
d(scrollable=True).fling() #向前投掷(默认)垂直(默认)

d(scrollable=True).fling.vert.forward()  #垂直向后滚动

d(scrollable=True).fling.vert.backward()

d(scrollable=True).fling.horiz.toBeginning(max_swipes=1000)

d(scrollable=True).fling.toEnd() #滚动到结束

d(scrollable=True).scroll(steps=10)  # 向前滚动(默认)垂直(默认)

d(scrollable=True).scroll.horiz.forward(steps=100)  # 水平向前滚动

d(scrollable=True).scroll.vert.backward()  #垂直向后滚动

d(scrollable=True).scroll.horiz.toBeginning(steps=100, max_swipes=1000)  #滚动到开始水平

d(scrollable=True).scroll.toEnd() # 滚动到垂直结束

d(scrollable=True).scroll.to(text="Security") #垂直向前滚动，直到出现特定的ui对象
```
**拖动操作**
```py
d(text="设置").drag_to(500, 500, duration=0.1)  #在0.1秒内拖动到坐标（x,y）

d(text="设置").drag_to(text="安全中心", duration=0.2)
```
**获取/设置/清空编辑框内容**
```py
d(description="请输入QQ号码或手机或邮箱").get_text()

d(description="请输入QQ号码或手机或邮箱").set_text("1234")

d(description="请输入QQ号码或手机或邮箱").clear_text()
```

**打开链接**
```py
d.open_url("https://www.baidu.com")

d.open_url("taobao://taobao.com")    # open Taobao app

d.open_url("appname://appnamehost")

```


