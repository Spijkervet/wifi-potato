import netifaces


class Interface():
    def __init__(self):
        self._sniff_iface = ""
        self._ap_iface = "wlan0"

    @property
    def sniff_iface(self):
        return self._sniff_iface

    @sniff_iface.setter
    def sniff_iface(self, value):
        self._sniff_iface = value

    @property
    def ap_iface(self):
        return self._ap_iface

    @ap_iface.setter
    def ap_iface(self, value):
        self._ap_iface = value

    def get_interfaces(self):
        return netifaces.interfaces()
