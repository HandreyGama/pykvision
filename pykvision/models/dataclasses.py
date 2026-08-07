from dataclasses import dataclass

@dataclass
class ConfigConnection:
    ip_address:str
    username:str = "admin"
    passwd:str = "admin"
    use_https:bool = False

@dataclass
class FaceAppendData:
    name:str
    bornTime:str
    sex:str
    customHumanID:int 

@dataclass
class PictureUploadData:
    FDID:str
    FaceAppendData:FaceAppendData 