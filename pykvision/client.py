"""
This module is responsable for making the HTTP Requests to ISAPI
.
"""
import requests
from requests.auth import HTTPDigestAuth
from pykvision.models.schemes.system import System
from pykvision.endpoints import ISAPIEndpoints, IntelligentEndpoints, SystemEndpoints
from pykvision.services import IntelligentService, SystemService

class ISAPIClient:
    """
    This class is the logical representation of the ISAPI Connection, 
    and is responsable to make the HTTP requests, handle sessions, and return the 
    attributes of the devices.
    """
    def __init__(self,IPAdress:str,username:str,passwd:str) -> None:
        self.IPAdress = "http://" + IPAdress
        self.username = username
        self.passwd = passwd
        self.SystemService = SystemService() 
        self.IntelligentService = IntelligentService()
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(self.username,self.passwd)
        
    def get_system_device_info(self) -> None:
        device_info_endpoint = self.IPAdress + SystemEndpoints.DEVICE_INFO
        req = self.session.get(device_info_endpoint)
        self.SystemService.generate_device_info(req)
        
    def get_system_capabilities(self) -> None:
        system_capabilities_endpoint = self.IPAdress + SystemEndpoints.CAPABILITIES
        req = self.session.get(system_capabilities_endpoint)
        self.SystemService.generate_device_info(req)  
    def get_intelligent_capabilities(self) -> None:
        intelligent_capabilities_endpoint = self.IPAdress + IntelligentEndpoints.CAPABILITIES
        req = self.session.get(intelligent_capabilities_endpoint)
        self.IntelligentService.generate_capabilities(req)
        pass    
    def generate_instance_intelligent(self):
        self.get_intelligent_capabilities()
        return self.IntelligentService.intelligent
    def generate_instance_system(self):
        self.get_system_device_info()
        return self.SystemService.system