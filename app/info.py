from .interface import Interface
from .access_point import AccessPoint

class Info(AccessPoint, Interface):

    def __init__(self):
        AccessPoint.__init__(self)
        Interface.__init__(self)
        self.name = "WiFi Potato"
