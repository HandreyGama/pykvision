"""
Virtual interface models for VCA objects in pykvision.

This module defines the virtual objects used to interact with Hikvision ISAPI
face and video analytics resources in a more Pythonic and easier way.

It contains abstractions for common VCA entities such as persons, vehicles,
database-related structures, and other virtual interfaces that mirror the
ISAPI data model expected by Hikvision devices and services.


@obs: module description generated with AI.
      check the information in the docs section for more accure info  
"""

from datetime import datetime
from pathlib import Path

from pykvision.models.dataclasses import FaceAppendData, PersonInfoExtend, PersonInfoExtendList, PictureUploadData

valid_keys:list[str] = ["id","enable","name","value"]

class Person:
    """
    Represents a person record to be inserted into a Hikvision face library.

    This virtual interface stores the data needed by ISAPI to register a person,
    including personal information, enrollment metadata, extra tags, and the
    payload objects used in upload requests.
    """

    def __init__(self,
                 name:str="",
                 born_time:str="",
                 sex:str="male",
                 certificateType:str="ID",
                 certificateNumber:int=0,
                 fdid:str="",
                 tags:list[dict]=[],
                 image_path:Path=Path()
                 ) -> None:
        self.name:str = name
        self.born_time:str = self.parse_datetime_format(born_time)
        self.certificateType:str = certificateType
        self.certificateNumber:int = certificateNumber
        self.fdid:str = fdid
        self.tags:list[dict] = tags
        self.sex:str = sex
        self.image_path:Path = image_path
        self.person_info_extend_list:PersonInfoExtendList = self.generate_person_info_extend_list()
        self.face_append_data:FaceAppendData = self.generate_face_append_data()
        self.picture_upload_data:PictureUploadData = self.generate_picture_upload_data()

    def generate_person_info_extend_list(self) -> PersonInfoExtendList:
        """
        Get a list with a dict with 4 values and generate the tag of the person in database
        * id:int
        * enable:bool
        * name:str
        * value:str
        """
        person_info_extend_list = PersonInfoExtendList()
        
        for d in self.tags:
            if not all(k in valid_keys for k in d):
                raise ValueError()
            person_info_extend = PersonInfoExtend()
            person_info_extend.id = d["id"]
            person_info_extend.enable = d["enable"]
            person_info_extend.name = d["name"]
            person_info_extend.value = d["value"]
            person_info_extend_list.PersonInfoExtend.append(person_info_extend)
        return person_info_extend_list
    def parse_datetime_format(self,str_date:str) -> str:
        parsed_date = datetime.strptime(str_date,"%d/%m/%Y")
        transformed_date = parsed_date.strftime("%Y-%d-%m")
        return transformed_date
    def generate_face_append_data(self) -> FaceAppendData:
        """
        Generate the FaceAppendData dataclass with the values given in constructor
        """
        face_append_data = FaceAppendData()
        face_append_data.name = self.name
        face_append_data.bornTime = self.born_time
        face_append_data.sex = self.sex
        face_append_data.certificateType = self.certificateType
        face_append_data.certificateNumber = self.certificateNumber
        face_append_data.PersonInfoExtendList = self.person_info_extend_list
        return face_append_data
    
    def generate_picture_upload_data(self) -> PictureUploadData:
        """
        Generate the PictureUploadData dataclass with the values given in constructor
        """
        picture_upload_data = PictureUploadData()
        picture_upload_data.FaceAppendData = self.face_append_data
        picture_upload_data.FDID = self.fdid 
        return picture_upload_data   
