"""
This module is responsable for making the HTTP Requests to ISAPI
.
"""
from enum import StrEnum
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
from pykvision.models.exceptions import ISAPIAutenticationError, ISAPIInvalidEndpointError, ISAPIInvalidEndpointMethodError
from pykvision.models.consts import ISAPI_HTTP_METHODS

class ISAPIClient:
    """
    This class is the logical representation of the ISAPI Connection, 
    and is responsible to make the HTTP requests, handle sessions, and return the 
    attributes of the devices.
    """
    def __init__(self,config:ConfigConnection) -> None:
        if config.use_https:
            self.http_scheme:str =  "https"
            self.port:int = 443
        else:
            self.port:int = 80
            self.http_scheme:str = "http"   
        self.ip_url:str = f"{self.http_scheme}://{config.ip_address}:{self.port}"
        self.username:str = config.username
        self.passwd:str = config.passwd
        self.session:requests.Session = requests.Session()
        self.session.auth = HTTPDigestAuth(self.username,self.passwd)

    def request(self,endpoint:str,method:ISAPI_HTTP_METHODS,data:dict | None=None,files=None,**kwargs) -> Response:
        response = self.session.request(url=endpoint,method=method,data=data,files=files,**kwargs)
        if response.status_code == 404:
            raise ISAPIInvalidEndpointError(response.status_code,response.url,response.text)
        elif response.status_code == 405:
            raise ISAPIInvalidEndpointMethodError(response.status_code,response.url,method,response.text)
        elif response.status_code == 401:
            raise ISAPIAutenticationError(response.text)
        return response
    
    def build_url(self,endpoint:StrEnum) -> str:
        url = self.ip_url + endpoint
        return url    

    def get_system_device_info(self) -> Response:
        device_info_endpoint = self.build_url(SystemEndpoints.DEVICE_INFO)
        response = self.request(device_info_endpoint,ISAPI_HTTP_METHODS.GET)
        return response
    
    def get_system_capabilities(self) -> Response:
        system_capabilities_endpoint = self.build_url(SystemEndpoints.CAPABILITIES)
        response = self.request(system_capabilities_endpoint,ISAPI_HTTP_METHODS.GET)
        return response 

    def get_intelligent_capabilities(self) -> Response:
        intelligent_capabilities_endpoint = self.build_url(IntelligentEndpoints.CAPABILITIES)
        response = self.request(intelligent_capabilities_endpoint,ISAPI_HTTP_METHODS.GET)
        return response
        
    def post_upload_person_db(self,person:Person,picture_upload_data:str) -> Response:
        """
        Make the HTTP POST request to upload the person info/picture in the face library </br>
        * Return: Status code
        """
        intelligent_fdlib_picture_upload_endpoint = self.build_url(IntelligentEndpoints.PICTURE_UPLOAD)
        picture_payload_info = picture_upload_data
        payload = {
            "FaceAppendData":picture_payload_info,
        }
        with person.image_path.open("rb") as image:
            files = {
                "importImage":(person.image_path.name,image,"image/jpeg")
            }
            response = self.request(
                intelligent_fdlib_picture_upload_endpoint,
                ISAPI_HTTP_METHODS.POST,
                data=payload,
                files=files)
            return response
        
    def get_fdlib(self) -> Response:
        fdlibs_endpoint = self.build_url(IntelligentEndpoints.FDLIB)
        response = self.request(fdlibs_endpoint,ISAPI_HTTP_METHODS.GET)
        return response