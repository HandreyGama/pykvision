"""
This module is responsable for making the HTTP Requests to ISAPI
.
"""
from pathlib import Path

import requests
from requests.auth import HTTPDigestAuth
from pykvision.models.endpoints import IntelligentEndpoints, SystemEndpoints
from pykvision.services import IntelligentService, SystemService
from pykvision.models.schemes.intelligent import IntelligentScheme
from pykvision.models.schemes.system import SystemScheme
from pykvision.models.dataclasses import ConfigConnection,PictureUploadData
class ISAPIClient:
    """
    This class is the logical representation of the ISAPI Connection, 
    and is responsible to make the HTTP requests, handle sessions, and return the 
    attributes of the devices.
    """
    def __init__(self,config:ConfigConnection) -> None:
        if config.use_https:
            self.http_scheme =  "https"
            self.port = 443
        else:
            self.port = 80
            self.http_scheme = "http"   
        self.ip_url = f"{self.http_scheme}://{config.ip_address}:{self.port}"
        self.username = config.username
        self.passwd = config.passwd
        self.system_service = SystemService() 
        self.intelligent_service = IntelligentService()
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(self.username,self.passwd)
        
    def get_system_device_info(self) -> None:
        device_info_endpoint = self.ip_url + SystemEndpoints.DEVICE_INFO
        req = self.session.get(device_info_endpoint)
        self.system_service.generate_device_info(req)

    def get_system_capabilities(self) -> None:
        system_capabilities_endpoint = self.ip_url + SystemEndpoints.CAPABILITIES
        req = self.session.get(system_capabilities_endpoint)
        self.system_service.generate_capabilities(req) 

    def get_intelligent_capabilities(self) -> None:
        intelligent_capabilities_endpoint = self.ip_url + IntelligentEndpoints.CAPABILITIES
        req = self.session.get(intelligent_capabilities_endpoint)
        self.intelligent_service.generate_capabilities(req)
        
    def generate_instance_intelligent(self) -> IntelligentScheme:
        self.get_intelligent_capabilities()
        return self.intelligent_service.intelligent
    
    def generate_instance_system(self) -> SystemScheme:
        self.get_system_device_info()
        return self.system_service.system
    
    def post_face_picture_upload(self,PictureUploadData:PictureUploadData,image_path:Path):
        intelligent_fdlib_picture_upload_endpoint = self.ip_url + IntelligentEndpoints.PICTURE_UPLOAD
        picture_payload_info = self.intelligent_service.generate_picture_upload_xml_data(PictureUploadData)
        payload = {
            "FaceAppendData":picture_payload_info,
        }
        with image_path.open("rb") as image
        files = {
            "importImage":(image_path.name,image,"image/jpeg")
        }
        req = self.session.post(intelligent_fdlib_picture_upload_endpoint,data=payload,files=files)
        return req.status_code