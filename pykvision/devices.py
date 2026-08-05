"""
This module contains all the devices suported by pykvision
such as NVRS, CAMERAS.
"""

from pykvision.client import ISAPIClient
from pykvision.models.schemes.intelligent import Capabilities as InteliCap
from pykvision.models.schemes.system import DeviceInfo as DevInfo



class NVR:
    """
    This class is the logical representation of the Hikvision NVR recorder.
    use this interface to interact with the device.
    """
    def __init__(self,IPAdress:str,username:str,passwd:str) -> None:
        """
        * ip addrs example : '192.168.1.4'
        * username example: 'admin'
        * passwd example: 'my_awsome_super_secure_password_123'
        """
        self.IPAdress = IPAdress
        self.username = username
        self.passwd = passwd
        self.isapi_client = ISAPIClient(self.IPAdress,self.username,self.passwd)
        self.intelligent = self.isapi_client.generate_instance_intelligent()
        self.system = self.isapi_client.generate_instance_system()
    def get_intelligent_capabilities(self) -> InteliCap:
        """
        Return a Capabilities dataclass 
        """
        return self.intelligent.capabilities
    def get_system_device_info(self) -> DevInfo:
        """
        Return a DeviceInfo dataclass 
        """
        return self.system.deviceInfo
        
class Camera:
    """
    This class is the logical representation of the Hikvision IP Camera.
    use this interface to interact with the device.
    """
    def __init__(self,IPAdress,username,passwd) -> None:
        self.IPAdress = IPAdress
        self.username = username
        self.passwd = passwd
   
nvr_facial = NVR("192.168.1.94","usuario","senha")