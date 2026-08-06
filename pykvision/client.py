"""
This module is responsable for making the HTTP Requests to ISAPI
.
"""
import requests
from requests.auth import HTTPDigestAuth
from pykvision.models.endpoints import IntelligentEndpoints, SystemEndpoints
from pykvision.services import IntelligentService, SystemService
from pykvision.models.schemes.intelligent import IntelligentScheme
from pykvision.models.schemes.system import SystemScheme

class ISAPIClient:
    """
    This class is the logical representation of the ISAPI Connection, 
    and is responsible to make the HTTP requests, handle sessions, and return the 
    attributes of the devices.
    """
    def __init__(self,ip_address:str,username:str="admin",passwd:str="admin",use_https:bool=False) -> None:
        if use_https:
            self.http_scheme =  "https"
            self.port = 443
        else:
            self.port = 80
            self.http_scheme = "http"   
        self.ip_url = f"{self.http_scheme}://{ip_address}:{self.port}"
        self.username = username
        self.passwd = passwd
        self.system_service = SystemService() 
        self.intelligent_service = IntelligentService()
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(self.username,self.passwd)
        
    def set_system_device_info(self) -> None:
        device_info_endpoint = self.ip_url + SystemEndpoints.DEVICE_INFO
        req = self.session.get(device_info_endpoint)
        self.system_service.generate_device_info(req)

    def set_system_capabilities(self) -> None:
        system_capabilities_endpoint = self.ip_url + SystemEndpoints.CAPABILITIES
        req = self.session.get(system_capabilities_endpoint)
        self.system_service.generate_capabilities(req) 

    def set_intelligent_capabilities(self) -> None:
        intelligent_capabilities_endpoint = self.ip_url + IntelligentEndpoints.CAPABILITIES
        req = self.session.get(intelligent_capabilities_endpoint)
        self.intelligent_service.generate_capabilities(req)
        
    def generate_instance_intelligent(self) -> IntelligentScheme:
        self.set_intelligent_capabilities()
        return self.intelligent_service.intelligent
    
    def generate_instance_system(self) -> SystemScheme:
        self.set_system_device_info()
        return self.system_service.system