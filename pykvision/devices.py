"""
This module contains all the devices suported by pykvision
such as NVRS, CAMERAS.
"""

from pykvision.client import ISAPIClient
from pykvision.models.intelligent import Intelligent



class Nvr:
    def __init__(self,IPAdress,username,passwd) -> None:
        self.IPAdress = IPAdress
        self.username = username
        self.passwd = passwd
        self.intelligent = Intelligent()
        self.isapi_client = ISAPIClient(self.IPAdress,self.username,self.passwd)
        self.__set_intelligent()
    def __set_intelligent(self):
        self.isapi_client.get_intelligent_capabilities()
        self.intelligent = self.isapi_client.get_intelligent
        pass
    @property
    def get_intelligent_capabilities(self):
        return self.intelligent.capabilities

        
class Camera:
    def __init__(self,IPAdress,username,passwd) -> None:
        self.IPAdress = IPAdress
        self.username = username
        self.passwd = passwd
   
nvr_facial = Nvr("192.168.1.94","usuario","senha")