"""
This module is responsable for store all the dataclasses
in the pykvision module, such as :
* ConfigConnection
* PersonInfoExtend
* FaceAppendData

"""

from dataclasses import dataclass, field

@dataclass
class ConfigConnection:
    ip_address:str
    username:str = "admin"
    passwd:str = "admin"
    use_https:bool = False

@dataclass
class PersonInfoExtend:
    id:int = 0
    enable:bool = False
    name:str = ""
    value:str = "No Info provided"
@dataclass
class PersonInfoExtendList:
    PersonInfoExtend:list = field(default_factory=list)

@dataclass
class FaceAppendData:
    name:str = "None"
    bornTime:str = "1990-01-01"
    sex:str = "male"
    certificateType:str = "ID"
    certificateNumber:int = 1 
    PersonInfoExtendList:PersonInfoExtendList = field(default_factory=PersonInfoExtendList)

@dataclass
class PictureUploadData:
    FDID:str=""
    FaceAppendData:FaceAppendData = field(default_factory=FaceAppendData)