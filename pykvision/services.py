"""
This module is responsable to handle all the logic 
of parsing xml requests and response to object.
such as logic of business. 
"""


from requests import Response

from pykvision.models.schemes.intelligent import IntelligentScheme
from pykvision.models.schemes.system import SystemScheme
from pykvision.xmlparse import dict_parse_xml, xml_parse_dict
from pykvision.models.endpoints import SystemEndpoints
from pykvision.models.dataclasses import PictureUploadData,FaceAppendData
from dataclasses import asdict
class SystemService:
    """
    This class represents the System service business logic, 
    and handle the parse beetwen the model and the HTTP response.
    """
    def __init__(self) -> None:
        self.system = SystemScheme()
    def generate_device_info(self,value:Response) -> None:
        """
        Recieve a HTTP Response of endpoint device_info, 
        converts the xml into a dict and generate the dataclass. 
        """
        dic = xml_parse_dict(value.text)
        self.system.set_device_info(dic["DeviceInfo"])
        pass    
    def generate_capabilities(self,value:Response) -> None:
        """
        Recieve a HTTP Response of endpoint capabilities,
        converts the xml into a dict and generate the dataclass. 
        """        
        dic = xml_parse_dict(value.text)
        self.system.set_capabilities(dic)
        pass        
    
class IntelligentService:
    def __init__(self) -> None:
        self.intelligent = IntelligentScheme()
        
    def generate_capabilities(self,value:Response):
        dic = xml_parse_dict(value.text)
        self.intelligent.set_capabilities(dic["IntelliCap"]) 

    def generate_fdlib_capabilities(self,value:Response):
        dic = xml_parse_dict(value.text)
        self.intelligent.set_fd_lib_capabilities(dic["FDLibCap"])

    def generate_picture_upload_xml_data(self,data:PictureUploadData) -> str:
        dic = {
            "PictureUploadData": asdict(data)
            }
        xml = dict_parse_xml(dic)
        return xml