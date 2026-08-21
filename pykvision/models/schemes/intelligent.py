"""
This module represents all the data contained in the
endpoints GET /ISAPI/Intelligent/...
"""
from dataclasses import dataclass,field
from pykvision.xmlparse import to_bool_xml
from pykvision.models.interfaces import Capabilities
from pykvision.models.dataclasses import FDlib


FIELD_MAP_CAPABILITIES = {
    "isFaceSupport":"is_face_support",
    "isBehaviorSupport":"is_behavior_support",
    "isLineDetectionSupport":"is_line_detection_support",
    "isFieldDetectionSupport":"is_field_detection_support",
    "isRegionEntraceSupport":"is_region_entrace_support",
    "isRegionExitingSupport":"is_region_exiting_support",
    "isLoiteringSupport":"is_loitering_support",
    "isGroupSupport":"is_group_support",
    "isRapidMoveSupport":"is_rapid_move_support",
    "isParkingSupport":"is_parking_support",
    "isUnattendedBaggageSupport":"is_unattended_baggage_support",
    "isAttendedBaggageSupport":"is_attended_baggage_support",
    "isTeacherSupport":"is_teacher_support",
    "isStudentSupport":"is_student_support",
    "isSupportUploadFacePictureByForm":"is_support_upload_face_picture_by_form",
    "isSupportSafetyHelmetDetection":"is_support_safety_helmet_detection",
    "isSupportMisinfoFilterStatisticalMode":"is_support_misinfo_filter_statistical_mode",
    "isSupportFaceScore":"is_support_face_score",
    "isSupportUploadFacePictureByUrl":"is_support_upload_face_by_url",
}

@dataclass(slots=True)
class IntelliCapabilities(Capabilities):
    is_face_support:bool=False
    is_behavior_support:bool=False
    is_line_detection_support:bool=False
    is_field_detection_support:bool=False
    is_region_entrace_support:bool=False
    is_region_exiting_support:bool=False
    is_loitering_support:bool=False
    is_group_support:bool=False
    is_rapid_move_support:bool=False
    is_parking_support:bool=False
    is_unattended_baggage_suport:bool=False
    is_attended_baggage_support:bool=False
    is_teacher_support:bool=False
    is_student_support:bool=False
    is_support_upload_face_picture_by_form:bool=False
    is_support_safety_helmet_detection:bool=False
    is_support_misinfo_filter_statistical_mode:bool=False
    is_support_face_score:bool=False
    is_support_upload_face_by_url:bool=False


FIELD_MAP_FD_LIB_CAPABILITIES = {
    "isSupport": "is_support_fc_search_data_package",
    "isSupportStandardSearch": "is_support_standard_search",
    "isSupportFaceDataExport": "is_support_face_data_export",
    "isSupportNewlyPictureUpload": "is_support_newly_pickture_upload",
    "isSupportFCSearchNormal": "is_support_fc_search_normal",
    "isSupportPrompt": "is_support_prompt",
    "isSupportFCSearchJsonFormat": "is_support_fc_search_json_format",
    "isSupportFCSearchDataPackageJsonFormat": "is_support_fc_search_data_package_json_format",
    "isSupportManualModeling": "is_support_manual_modeling",
    "isSupportAnalysisFace": "is_support_analysis_face",
    "isSupportFCSearch": "is_support_fc_search",
    "isSupportFDLibEachImport": "is_support_fd_lib_each_import",
    "isSupportManualModelingStatusSearch": "is_support_manual_modeling_status_search",
    "isSupportCustomFaceLibID": "is_support_custom_face_lib_id",
    "isSupportFDCapacity": "is_support_fd_capacity",
    "isSupportFaceScore": "is_support_face_score",
    "isSupportOccurrenceData": "is_support_occurrence_data",
    "isSupportFaceLibFormat": "is_support_face_lib_format",
    "isSupportSurplusCapacityAll": "is_support_surplus_capacity_all",
    "isSupportAsyncImportData": "is_support_async_import_data",
    "isSupportTaskStatusSearch": "is_support_task_status_search",
    "isSupportPICCertification": "is_support_pic_certification",
}


@dataclass(slots=True)
class FDLibCapabilities:
    is_support_fc_search_data_package:bool = False
    is_support_standard_search:bool = False
    is_support_face_data_export:bool = False
    is_support_newly_pickture_upload:bool = False
    is_support_fc_search_normal:bool = False 
    is_support_prompt:bool = False
    is_support_fc_search_json_format:bool = False
    is_support_fc_search_data_package_json_format:bool = False
    is_support_manual_modeling:bool = False
    is_support_analysis_face:bool = False
    is_support_fc_search:bool = False
    is_support_fd_lib_each_import:bool = False
    is_support_manual_modeling_status_search:bool = False
    is_support_custom_human_id:bool = False
    is_support_custom_face_lib_id:bool = False
    is_support_fd_capacity:bool = False
    is_support_face_score:bool = False
    is_support_occurrence_data:bool = False
    is_support_face_lib_format:bool = False
    is_support_surplus_capacity_all:bool = False
    is_support_async_import_data:bool = False
    is_support_task_status_search:bool = False
    is_support_pic_certification:bool = False
    support_upload_picture_type:tuple = ("binary","url")


@dataclass(slots=True)
class FDLib:
    fd_lib_cap:FDLibCapabilities = field(default_factory=FDLibCapabilities)
    fd_lib_list:list = field(default_factory=list)

@dataclass(slots=True)
class IntelligentScheme:
    """
    This is a dataclass representation of the XML response of endpoint Intelligent
    """
    capabilities:IntelliCapabilities = field(default_factory=IntelliCapabilities)
    fd_lib:FDLib = field(default_factory=FDLib)
    
    
    def set_capabilities(self,data:dict):
        for xml_name, attr_name in FIELD_MAP_CAPABILITIES.items():
            setattr(
                self.capabilities,
                attr_name,
                to_bool_xml(data.get(xml_name,False))
            )

    def set_fd_lib_capabilities(self,data:dict):
        for xml_name, attr_name in FIELD_MAP_FD_LIB_CAPABILITIES.items():
            setattr(
                self.fd_lib.fd_lib_cap,
                attr_name,
                to_bool_xml(data.get(xml_name, False))
            )
            
    def set_fd_lib_list(self,data:list[dict]):
        for i in data:
            fd_lib = FDlib(
                id=i["id"],
                fdid=i["FDID"],
                name=i["name"],
                face_lib_type=i["faceLibType"],
                total_face_num=i["totalFaceNum"],
                normal_face_num=i["normalFaceNum"],
                abnormal_face_num=i["abnormalFaceNum"]
            )
            self.fd_lib.fd_lib_list.append(fd_lib)
            