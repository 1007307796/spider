import os

# 平台
PLATFORM = 'Android'

# 设备名称 通过 adb devices -l 获取
DEVICE_NAME = 'V1730EA'
# 键盘设置
# APP包名
APP_PACKAGE = 'com.tencent.mm'

# 入口类名
APP_ACTIVITY = 'com.tencent.mm.ui.LauncherUI'
ANDROID_PROCESS = 'com.tencent.mm:tools'
AUTOMATION_NAME = 'UiAutomator2'
# Appium服务器地址
DRIVER_SERVER = 'http://localhost:4723/wd/hub'
# 等待元素加载时间
TIMEOUT = 500
NEW_COMMAND_TIMEOUT = 6000

# 微信手机号密码
USERNAME = '18482153491'
PASSWORD = ''

# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 700

# 滑动间隔
SCROLL_SLEEP_TIME = 1