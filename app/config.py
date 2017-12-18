

class Config():

    def __init__(self):
        self.hostapd_conf = "/etc/hostapd/hostapd.conf"
        self.hostapd_control_path = '/var/run/hostapd'
        self.hostapd_cli_path = '/usr/sbin/hostapd_cli'

        self.ifconfig_path = '/sbin/ifconfig'

        self.arp_path = '/usr/sbin/arp'
        self.arp_flags = '-an'
