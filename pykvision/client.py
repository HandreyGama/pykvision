"""
This module is responsable for making the HTTP Requests to ISAPI
.
"""
from pathlib import Path
from warnings import deprecated

from requests.models import Response
import requests
from requests.auth import HTTPDigestAuth
from pykvision.models.endpoints import IntelligentEndpoints, SystemEndpoints
from pykvision.models.vca import Person
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
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(self.username,self.passwd)
        
    def get_system_device_info(self) -> Response:
        device_info_endpoint = self.ip_url + SystemEndpoints.DEVICE_INFO
        req = self.session.get(device_info_endpoint)
        return req

    def get_system_capabilities(self) -> Response:
        system_capabilities_endpoint = self.ip_url + SystemEndpoints.CAPABILITIES
        req = self.session.get(system_capabilities_endpoint)
        return req 

    def get_intelligent_capabilities(self) -> Response:
        intelligent_capabilities_endpoint = self.ip_url + IntelligentEndpoints.CAPABILITIES
        req = self.session.get(intelligent_capabilities_endpoint)
        return req
        
    def post_upload_person_db(self,person:Person,picture_upload_data:str) -> Response:
        """
        Make the HTTP POST request to upload the person info/picture in the face library </br>
        * Return: Status code
        """
        intelligent_fdlib_picture_upload_endpoint = self.ip_url + IntelligentEndpoints.PICTURE_UPLOAD
        picture_payload_info = picture_upload_data
        payload = {
            "FaceAppendData":picture_payload_info,
        }
        with person.image_path.open("rb") as image:
            files = {
                "importImage":(person.image_path.name,image,"image/jpeg")
            }
            req = self.session.post(intelligent_fdlib_picture_upload_endpoint,data=payload,files=files)
            return req
        
    def get_fdlib_list(self) -> Response:
        fdlib_endpoint = self.ip_url + IntelligentEndpoints.FDLIB
        req = self.session.get(fdlib_endpoint)
        return req