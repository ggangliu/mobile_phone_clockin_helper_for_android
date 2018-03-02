# -*- coding:utf-8 -*-

import time, os, math, sys
import ConfigParser
import subprocess
from PIL import Image
from uiautomator import device as Phone

target_color = (135, 162, 252, 255)

VERSION = "1.2.1"

def yes_or_no(prompt, true_value='y', false_value='n', default=True):
    """
    检查是否已经为启动程序做好了准备
    """
    default_value = true_value if default else false_value
    prompt = '{} {}/{} [{}]: '.format(prompt, true_value,
        false_value, default_value)
    i = input(prompt)
    if not i:
        return default
    while True:
        if i == true_value:
            return True
        elif i == false_value:
            return False
        prompt = 'Please input {} or {}: '.format(true_value, false_value)
        i = input(prompt)

def dump_device_info():
    """
    显示设备信息
    """
    size_str = os.popen('.\\Tools\\platform-tools\\adb shell wm size').read()
    device_str = os.popen('.\\Tools\\platform-tools\\adb shell getprop ro.product.device').read()
    Phone_os_str = os.popen('.\\Tools\\platform-tools\\adb shell getprop ro.build.version.release').read()
    density_str = os.popen('.\\Tools\\platform-tools\\adb shell wm density').read()
    print("""******************************\nScreen: {size}\nDensity: {dpi}\nDevice: {device}\nPhone OS: {Phone_os}\nHost OS: {host_os}
Python: {python}\n******************************""".format(
              size=size_str.strip(),
              dpi=density_str.strip(),
              device=device_str.strip(),
              Phone_os=Phone_os_str.strip(),
              host_os=sys.platform,
              python=sys.version
    ))

SCREENSHOT_WAY = 3


def pull_screenshot(file_name):
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序
    """
    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            '.\\Tools\\platform-tools\\adb shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        f = open(file_name, 'wb')
        f.write(binary_screenshot)
        f.close()
    elif SCREENSHOT_WAY == 0:
        os.system('.\\Tools\\platform-tools\\adb shell screencap -p /sdcard/screenshot.png')
        os.system('.\\Tools\\platform-tools\\adb pull /sdcard/screenshot.png .')


def check_screenshot():
    """
    检查获取截图的方式
    """
    global SCREENSHOT_WAY
    if os.path.isfile('screenshot.png'):
        try:
            os.remove('screenshot.png')
        except Exception:
            pass
    if SCREENSHOT_WAY < 0:
        print('暂不支持当前设备')
        sys.exit()
    pull_screenshot('./screenshot.png')
    try:
        Image.open('./screenshot.png').load()
        print('采用方式 {} 获取截图'.format(SCREENSHOT_WAY).decode('utf-8'))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot()

class AutoClockInOut:
    def __init__(self, config_file='config.ini'):
        self.clock_times = []
        self.log_file = open("auto_clock.log", "w+")
        self.get_config_from_file()
        self.auto_main()

    def get_config_from_file(self, config_file='config.ini'):
        '''
        Get config information from config_file, default it included in ./config/config.ini
        :param config_file:
        :return:
        '''
        cf = ConfigParser.ConfigParser()
        cf.read(config_file)
        for no in range(0, 10, 1):
            if cf.has_option("times_poll", "time%d" % no):
                time_point = cf.get("times_poll", "time%d" % no).split(', ')
                self.run_log("%s" % time_point)
                self.clock_times.append((time_point[0], time_point[1]))

    def run_log(self, str):
        print(str.decode('utf-8'))
        self.log_file.write(str+'\n')

    def auto_main(self):
        for clock_time in self.clock_times:
            self.run_log("%s\n" % clock_time.__str__())
            while 1:
                time.sleep(1)
                self.log_file.flush()
                if self.auto_clock(clock_time):
                    break

    def wakeup_input_passward(self):
        self.run_log("唤醒手机/Wake up mobile Phone...")
        Phone.wakeup()
        time.sleep(1)
        self.run_log("解锁屏幕/Unlock screen....")
        Phone.swipe(198, 1375, 948, 712)
        time.sleep(1)
        # self.run_log("输入密码/Input password...")
        # Phone.click(219, 924)  # 1
        # time.sleep(1)
        # Phone.click(539, 1340)  # 8
        # time.sleep(1)
        # Phone.click(855, 934)  # 3
        # time.sleep(1)
        # Phone.click(857, 1329)  # 9

    def get_screenshot(self, file_name):
        os.system('.\\Tools\\platform-tools\\adb shell screencap -p /storage/emulated/0/{}'.format(file_name))
        os.system('.\\Tools\\platform-tools\\adb pull /storage/emulated/0/{} .'.format(file_name))

    def auto_clock(self, clock_time):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if clock_time[1] >= current_time >= clock_time[0] or current_time > clock_time[1]:
            self.wakeup_input_passward()
            parse_succuss = False
            while not parse_succuss:
                Phone.press.home()
                time.sleep(1)
                Phone(text="享用").click()
                time.sleep(1)
                Phone(text="取消").click()
                Phone(text="取消").click()
                time.sleep(1)
                Phone(text="考勤打卡").click()
                self.run_log("等待10秒后，打卡/After waiting 10 seconds, clock in...")
                time.sleep(10)

                try:
                    pull_screenshot('screenshot.png')
                    im = Image.open('./{}'.format('screenshot.png'))
                    position = self.find_clockin_pos_from_image(im)
                    parse_succuss = True
                except IndexError:
                    Phone.press.back()

            # Phone.click(533, 1262)  # 上下班打卡
            Phone.click(position[0], position[1])
            self.run_log("打卡时间/The time of clock in: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            time.sleep(5)
            file_name = time.strftime("./clockin_record/%Y-%m-%d_%H-%M-%S_record.jpg", time.localtime(time.time()))
            pull_screenshot(file_name)
            time.sleep(3)
            Phone.press.back()
            time.sleep(1)
            Phone.press.back()
            Phone.sleep()
            return 1
        else:
            self.run_log("The time of clock-in don't come in... %s" % current_time)
            return 0

    def find_clockin_pos_from_image(self, im):
        width, height = im.size
        print width, height
        # print im.histogram()
        target_x = width / 2
        target_y = height / 2 + width / 6
        im_pixel = im.load()
        target_x = x = width / 2
        for y in range(height / 2, height / 2 + width / 2, 1):
            current_value = math.sqrt(
                (im_pixel[x, y][0] - target_color[0]) ** 2 + (im_pixel[x, y][1] - target_color[1]) ** 2 +
                (im_pixel[x, y][2] - target_color[2]) ** 2 + (im_pixel[x, y][3] - target_color[3]) ** 2)

            if current_value < 80:
                print current_value, x, y
                break

        for k in range(y + width / 2, y, -1):
            current_value = math.sqrt(
                (im_pixel[x, k][0] - target_color[0]) ** 2 + (im_pixel[x, k][1] - target_color[1]) ** 2 +
                (im_pixel[x, k][2] - target_color[2]) ** 2 + (im_pixel[x, k][3] - target_color[3]) ** 2)

            if current_value < 80:
                print current_value, x, k
                target_y = (k + y) / 2
                break

        print target_x, target_y, im_pixel[target_x, target_y]
        return target_x, target_y


def main():
    android_home = os.path.abspath(".") + "\\Tools"
    os.environ["ANDROID_HOME"] = android_home
    sys.path.append(android_home + "\\platform-tools")
    print('Version Number: {}'.format(VERSION))
    dump_device_info()
    check_screenshot()
    auto_object = AutoClockInOut()
    print('所有任务已执行结束'.decode('utf-8'))
    sys.exit()


if __name__ == '__main__':
    main()
