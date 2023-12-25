import network
import time

_MAX_WAIT_MS = 20_000

class WifiConnector:
    def __init__(self,
                 network_ssid,
                 network_password):
        self.__wlan = network.WLAN(network.STA_IF)
        self.__wlan.active(True)

        self.__network_ssid = network_ssid
        self.__network_password = network_password

    @property
    def is_connected(self):
        return self.__wlan.status() == 3

    @property
    def public_interface(self):
        return self.__wlan.ifconfig()[0]

    def connect(self, on_connecting):
        self.__wlan.connect(self.__network_ssid, self.__network_password)

        connection_initiated = time.ticks_ms()

        while time.ticks_ms() - connection_initiated < _MAX_WAIT_MS:
            if self.is_connected:
                return True
            
            on_connecting()

        if self.is_connected:
            return True

        return False
