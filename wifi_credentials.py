class WifiCredentials:
    def __init__(self,
                 network_ssid,
                 network_password):
        self.__network_ssid = network_ssid
        self.__network_password = network_password

    @property
    def network_ssid(self):
        return self.__network_ssid
    
    @property
    def network_password(self):
        return self.__network_password
    
    @staticmethod
    def from_ini(ini_file_path):
        credentials = {}

        with open(ini_file_path) as f:
            line = f.readline()
            while line:
                if '=' not in line:
                    line = f.readline()
                    continue

                s = line.split('=')

                if len(s) != 2:
                    continue

                credentials[s[0].strip()] = s[1].strip()
                
                line = f.readline()

        assert 'network_ssid' in credentials
        assert 'network_password' in credentials

        return WifiCredentials(credentials['network_ssid'], credentials['network_password'])
