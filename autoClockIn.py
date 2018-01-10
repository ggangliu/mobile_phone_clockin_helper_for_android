# -*- coding:utf-8 -*-
from uiautomator import device as phone
import time, os


class autoClockInOut:
    def __init__(self):
        self.log_file = open("auto_clock.log", "w+")
        os.environ["ANDROID_HOME"] = "C:\\Users\\P0101236\\AppData\\Local\\Android\\android-sdk"
        self.auto_main()

    def auto_main(self):
        clock_times = [("2018-01-10 17:05:50", "2018-01-10 17:05:59"),
                       ("2018-01-10 17:30:50", "2018-01-10 17:30:59")]

        for clock_time in clock_times:
            self.log_file.write("%s\n" % clock_time.__str__())
            while 1:
                time.sleep(1)
                self.log_file.flush()
                if self.auto_clock(clock_time):
                    break

    def wakeup_input_passward(self):
        print "唤醒手机."
        phone.wakeup()
        print "滑动解锁屏幕."
        phone.swipe(535, 1847, 535, 1415)
        print "输入密码"
        phone.click(219, 924)  # 1
        phone.click(539, 1340)  # 8
        phone.click(855, 934)  # 3
        phone.click(857, 1329)  # 9

    def auto_clock(self, clock_time):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if (current_time >= clock_time[0] and current_time <= clock_time[1]):
            self.wakeup_input_passward()
            # de(text="考勤打卡").click()
            print "等待3秒后，打卡..."
            time.sleep(3)
            print "上班打卡..."
            print "打卡时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            phone.click(533, 1262)  # 上下班打卡
            time.sleep(5)
            phone.click(533, 1382)  # 我知道了
            # de.click(82,147) #返回菜单
            return 1
        else:
            print "打卡时间未到... ", current_time
            self.log_file.write("打卡时间未到... %s\n" % current_time)
            return 0


if __name__ == '__main__':
    auto_object = autoClockInOut()
