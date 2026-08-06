"""
This module contains all the devices suported by pykvision
such as NVRS, CAMERAS.
"""

from pykvision.client import ISAPIClient
from pykvision.models.schemes.system import DeviceInfo as DevInfo
from pykvision.models.interfaces import Capabilities



"""
TODO i think is better to create a interface, since NVR and Camera Objects
In The most part of the time will have the same methods. 
"""
class NVR:
    """
    This class is the logical representation of the Hikvision NVR recorder.
    use this interface to interact with the device.
    """
    def __init__(self,ip_address:str,username:str,passwd:str) -> None:
        """
        * ip addrs example : '192.168.1.4'
        * username example: 'admin'
        * passwd example: 'my_awsome_super_secure_password_123'
        """
        self.ip_address = ip_address
        self.username = username
        self.passwd = passwd
        self.isapi_client = ISAPIClient(self.ip_address,self.username,self.passwd)
        self.intelligent = self.isapi_client.generate_instance_intelligent()
        self.system = self.isapi_client.generate_instance_system()

    def get_intelligent_capabilities(self) -> Capabilities:
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
    def __init__(self,ip_address,username,passwd) -> None:
        self.ip_address = ip_address
        self.username = username
        self.passwd = passwd
