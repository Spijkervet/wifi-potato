import subprocess
import os, time

class Services():

    def __init__(self):
        self.hostapd = None
        self.dnsmasq = None

    def start_ap(self):
        from . import config
        self.kill_ap()
        time.sleep(1) # FIX THIS TO TASKS!!!!
        self.hostapd = subprocess.Popen(['hostapd ' + config.hostapd_conf + ' >./hostapd.log'], shell=True)

    def check_ap(self):
        if self.hostapd:
            if self.hostapd.poll() == None:
                return True
        return False

    def kill_ap(self):
        if self.check_ap():
            self.hostapd.kill()
        os.system("killall hostapd")
