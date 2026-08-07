"""
This module contains all the devices suported by pykvision
such as NVRS, CAMERAS.
"""

from pathlib import Path

from pykvision.client import ISAPIClient
from pykvision.models.dataclasses import ConfigConnection, FaceAppendData, PictureUploadData
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
    def __init__(self,config:ConfigConnection) -> None:
        """
        * ip addrs example : '192.168.1.4'
        * username example: 'admin'
        * passwd example: 'my_awsome_super_secure_password_123'
        """
        self.config = config
        self.isapi_client = ISAPIClient(self.config)
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
    def insert_new_person_picture(self,name,born_time,sex,custom_human_id,fdid,image_path:Path):
        if not image_path.exists():
            return False
        face_append_data = FaceAppendData(name,born_time,sex,custom_human_id)
        picture_upload_data = PictureUploadData(fdid,face_append_data)
        status = self.isapi_client.post_face_picture_upload(picture_upload_data,image_path)
        return status
        
class Camera:
    """
    This class is the logical representation of the Hikvision IP Camera.
    use this interface to interact with the device.
    """
    def __init__(self,config:ConfigConnection) -> None:
        self.ip_address = config.ip_address
        self.username = config.username
        self.passwd = config.passwd
