import subprocess, os, time, re

class AccessPoint():

    # nmcli radio wifi off
    # rfkill list
    def __init__(self):
        self._hostapd_driver = "nl80211"
        self.hostapd_process = None
        self._ssid = ""
        self._password = ""
        self._channel = ""
        self.ieee80211n = 1
        self.wmm_enabled = 1
        self.ctrl_interface = "/var/run/hostapd"
        self.ctrl_interface_group = 0
        self.key_mgtm = "WPA-PSK"

        self.clients = {}

    @property
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, value):
        # Do something if you want
        self._ssid = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        # Do something if you want
        self._password = value

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value


    def start_ap(self):

        from . import app_info, config
        from os import system
        from hostapdconf.parser import HostapdConf

        try:
            conf = HostapdConf(config.hostapd_conf)
        except FileNotFoundError:
            open(self._hostapd_conf,"w+")
            conf = HostapdConf(config.hostapd_conf)

        conf['ssid'] = self.ssid
        conf['interface'] = app_info.ap_iface
        conf['driver'] = self._hostapd_driver
        conf['channel'] = self.channel
        conf['ieee80211n'] = self.ieee80211n
        conf['wmm_enabled'] = self.wmm_enabled
        conf['ctrl_interface'] = self.ctrl_interface
        conf['ctrl_interface_group'] = self.ctrl_interface_group

        if self.password:
            conf['wpa'] = 3
            conf['wpa_passphrase'] = self.password
            conf['wpa_key_mgmt'] = self.key_mgtm
            conf['wpa_pairwise'] = "TKIP"
            conf['rsn_pairwise'] = "CCMP"

        conf.write()

        from . import services
        services.start_ap()


    def stop_ap(self):
        from os import system
        system("service hostapd stop")

    def setup_AP(self, ssid, password, channel):
        from . import app_info

        if not app_info.ap_iface:
            return False

        self.ssid = ssid

        if password:
            self.password = password

        if channel:
            if int(channel) < 0 or int(channel) > 16:
                return False
            self.channel = int(channel)

        self.start_ap()
        return True


    def get_vendor(self, mac_address):
        from netaddr import EUI
        try:
            vendor = EUI(mac_address).oui.registration().org
        except:
            vendor = "Unknown"
        return vendor

    def get_hostapd_interfaces(self):
        from . import config
        return os.listdir(config.hostapd_control_path)

    def get_clients(self, hostapd_iface):
        from . import config
        try:
            self.clients = {}
            hostapd_cli_cmd = [config.hostapd_cli_path,'-i', hostapd_iface, 'all_sta']
            hostapd_uptime = time.time() - int(os.stat('%s/%s' % (config.hostapd_control_path, hostapd_iface))[9])

            all_sta_output = subprocess.Popen(hostapd_cli_cmd,stdout=subprocess.PIPE).communicate()[0].decode()
            hostapd_output = subprocess.Popen([config.hostapd_cli_path,'status'], stdout=subprocess.PIPE).communicate()[0].decode().split('\n')

            channel = re.sub('channel=','',  hostapd_output[16])
            bssid = re.sub('bssid\[0\]=','', hostapd_output[24])
            ssid = re.sub('ssid\[0\]=','', hostapd_output[25])
            clientcount = int(re.sub('num_sta\[0\]=','', hostapd_output[26]))

            self.hostapd_stats = [ssid, bssid, channel, clientcount]

            macreg = r'^('+r'[:-]'.join([r'[0-9a-fA-F]{2}'] * 6)+r')$'
            stas = re.split(macreg, all_sta_output, flags=re.MULTILINE)

            mac = rx = tx = ctime = ''
            for sta_output in stas:
                for line in sta_output.split('\n'):
                    if re.match(macreg, line):
                        mac = line
                    if re.match('rx_packets', line):
                        rx = re.sub('rx_packets=','', line)
                    if re.match('tx_packets', line):
                        tx = re.sub('tx_packets=','', line)
                    if re.match('connected_time=',line):
                        ctime = re.sub('connected_time=','', line)

                if mac and rx and tx and ctime:
                    self.clients[mac] = {
                        'ctime': ctime,
                        'rx': rx,
                        'tx': tx,
                        'vendor': self.get_vendor(mac)
                    }

        except Exception as e:
            print(e)
        return self.clients
