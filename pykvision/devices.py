"""
This module contains all the devices suported by pykvision
such as NVRS, CAMERAS.
"""

from pathlib import Path
from warnings import deprecated

from requests import Response

from pykvision.client import ISAPIClient
from pykvision.models.dataclasses import ConfigConnection, FaceAppendData, PictureUploadData
from pykvision.models.schemes.intelligent import IntelligentScheme
from pykvision.models.schemes.system import DeviceInfo as DevInfo, SystemScheme
from pykvision.models.interfaces import Capabilities
from pykvision.models.vca import Person
from pykvision.services import IntelligentService, SystemService



"""
TODO i think is better to create a interface, since NVR and Camera Objects
In The most part of the time will have the same methods. 
"""
class NVR:
    """
    This class is the logical representation of the Hikvision NVR recorder.
    use this interface to interact with the device.
    """
    def __init__(self,config:ConfigConnection) -> None:
        """
        * ip addrs example : '192.168.1.4'
        * username example: 'admin'
        * passwd example: 'my_awsome_super_secure_password_123'
        """
        self.config = config
        self.isapi_client = ISAPIClient(self.config)
        self.intelligent = self.__generate_intelligent_instance()
        self.system = self.__generate_system_instance()
        self.system_service = SystemService()
        self.intelligent_service = IntelligentService()
        self.fdlib_dict = self.generate_fdlib_list()
        
    def __generate_system_instance(self) -> SystemScheme:
        device_info = self.isapi_client.get_system_device_info()
        self.system_service.generate_device_info(device_info)
        capabilities = self.isapi_client.get_system_capabilities()
        self.system_service.generate_capabilities(capabilities)
        return self.system_service.system
    
    def __generate_intelligent_instance(self) -> IntelligentScheme:
        capabilities = self.isapi_client.get_intelligent_capabilities()
        self.intelligent_service.generate_capabilities(capabilities)
        fdlib_list = self.isapi_client.get_fdlib_list()
        self.intelligent_service.generate_fdlib_list(fdlib_list)
        return self.intelligent_service.intelligent
    
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
    
    def insert_person_in_face_library(self,person:Person) -> Response:
        """
        Recives a Person object and inserts into the face picture database </br>
        @ Return: Status code
        """
        picture_upload_data = self.intelligent_service.generate_picture_upload_xml_data(person.picture_upload_data)
        status = self.isapi_client.post_upload_person_db(person,picture_upload_data)
        return status
    
    def generate_fdlib_list(self):
        fdlib_dict = {}
        for fdlib in self.intelligent.fd_lib.fd_lib_list:
            fdlib_name = fdlib.name
            fdlib_dict[fdlib_name] = fdlib
        return fdlib_dict
        
    def get_fdlib_dict(self):
        return self.fdlib_dict    
    
class Camera:
    """
    This class is the logical representation of the Hikvision IP Camera.
    use this interface to interact with the device.
    """
    def __init__(self,config:ConfigConnection) -> None:
        self.ip_address = config.ip_address
        self.username = config.username
        self.passwd = config.passwd
