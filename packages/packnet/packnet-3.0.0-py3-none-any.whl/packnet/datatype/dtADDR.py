"""

 PACKNET  -  c0mplh4cks

 DATATYPE
    ADDR



"""





# === Importing Dependencies === #
from struct import pack, unpack
from . import IP, MAC, INT







# === ADDR === #
class ADDR:
    def __init__(self, ip="255.255.255.255", port=0, mac="ff:ff:ff:ff:ff:ff", version=4):
        self.addr = [ip, port, mac]
        self.version = version


    def __str__(self):
        return f"['{self.ip}', {self.port}, '{self.mac}']"


    def __getitem__(self, key):
        if key == 0 or key == "ip":
            return self.ip
        elif key == 1 or key == "port":
            return self.port
        elif key == 2 or key == "mac":
            return self.mac
        else:
            raise IndexError


    def __setitem__(self, key, value):
        if key == 0 or key == "ip":
            self.ip = value
        elif key == 1 or key == "port":
            self.port = value
        elif key == 2 or key == "mac":
            self.mac = value
        else:
            raise IndexError


    @property
    def version(self):
        return self.ip.version


    @version.setter
    def version(self, value):
        self.ip.version = value


    @property
    def ip(self):
        return self.__ip


    @ip.setter
    def ip(self, value):
        self.__ip = IP(value) if type(value) == str else value


    @property
    def port(self):
        return self.__port


    @port.setter
    def port(self, value):
        self.__port = INT(value, 2, "big") if type(value) == int else value


    @property
    def mac(self):
        return self.__mac


    @mac.setter
    def mac(self, value):
        self.__mac = MAC(value) if type(value) == str else value


    @property
    def addr(self):
        return [ str(self.ip), int(self.port), str(self.mac) ]


    @addr.setter
    def addr(self, value):
        self.ip, self.port, self.mac = value
