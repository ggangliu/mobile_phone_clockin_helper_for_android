# -*- coding:utf-8 -*-
from uiautomator import device as phone
import time, os
import ConfigParser


class AutoClockInOut:
    def __init__(self, config_file='config.ini'):
        os.environ["ANDROID_HOME"] = "C:\\Users\\P0101236\\AppData\\Local\\Android\\android-sdk"
        self.clock_times = []
        self.log_file = open("auto_clock.log", "w+")
        self.get_config_from_file()
        self.auto_main()

    def get_config_from_file(self, config_file='config.ini'):
        # Get config information from config_file, default it included in ./config/config.ini
        cf = ConfigParser.ConfigParser()
        cf.read(config_file)
        for no in range(0, 10, 1):
            if cf.has_option("times_poll", "time%d" % no):
                time_point = cf.get("times_poll", "time%d" % no).split(', ')
                self.run_log("%s" % time_point)
                self.clock_times.append((time_point[0], time_point[1]))

    def run_log(self, str):
        print str
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
        self.run_log("Wake up mobile phone..")
        phone.wakeup()
        self.run_log("Unlock screen....")
        phone.swipe(535, 1847, 535, 1415)
        self.run_log("Input password...")
        phone.click(219, 924)  # 1
        phone.click(539, 1340)  # 8
        phone.click(855, 934)  # 3
        phone.click(857, 1329)  # 9

    def auto_clock(self, clock_time):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        if (current_time >= clock_time[0] and current_time <= clock_time[1]):
            self.wakeup_input_passward()
            # de(text="考勤打卡").click()
            self.run_log("After waiting 3 seconds, clock in...")
            time.sleep(3)
            phone.click(533, 1262)  # 上下班打卡
            self.run_log("The time of clock in: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            time.sleep(5)
            phone.click(533, 1382)  # 我知道了
            # de.click(82,147) #返回菜单
            return 1
        else:
            self.run_log("The time of clock-in don't come in... %s" % current_time)
            return 0

if __name__ == '__main__':
    auto_object = AutoClockInOut()
