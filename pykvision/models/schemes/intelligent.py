"""
This module represents all the data contained in the
endpoints GET /ISAPI/Intelligent/...
"""
from dataclasses import dataclass,field
from pykvision.xmlparse import to_bool_xml
from pykvision.models.interfaces import Capabilities
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

@dataclass(slots=True)
class IntelligentScheme:
    """
    This is a dataclass representation of the XML response of endpoint Intelligent
    """
    capabilities:IntelliCapabilities = field(default_factory=IntelliCapabilities)
    
    def set_capabilities(self,data:dict):
        for xml_name, attr_name in FIELD_MAP_CAPABILITIES.items():
            setattr(
                self.capabilities,
                attr_name,
                to_bool_xml(data.get(xml_name,False))
            )