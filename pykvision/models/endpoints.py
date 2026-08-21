"""
This module is responsable to contain all the endpoints of ISAPI
"""

from enum import StrEnum


class ISAPIEndpoints(StrEnum):
    API_ROOT = "/ISAPI"
    CONTENT_MGMT = f"{API_ROOT}/ContentMgmt"
    INTELLIGENT = f"{API_ROOT}/Intelligent"
    EVENT = f"{API_ROOT}/Event"
    IMAGE = f"{API_ROOT}/Image"
    SDT = f"{API_ROOT}/SDT"
    PTZ = f"{API_ROOT}/PTZCtrl"
    SECURITY = f"{API_ROOT}/Security"
    STREAMING = f"{API_ROOT}/Streaming"
    SYSTEM = f"{API_ROOT}/System"
    THERMAL = f"{API_ROOT}/Thermal"
    SMART = f"{API_ROOT}/Smart"
    

class ContentMgmtEndpoints(StrEnum):
    API_ROOT = ISAPIEndpoints.CONTENT_MGMT
    CAPABILITIES = f"{API_ROOT}/capabilities"

class SystemEndpoints(StrEnum):
    API_ROOT = ISAPIEndpoints.SYSTEM
    CAPABILITIES = f"{API_ROOT}/capabilities"
    DEVICE_INFO = f"{API_ROOT}/deviceInfo"
    
class IntelligentEndpoints(StrEnum):
    API_ROOT = ISAPIEndpoints.INTELLIGENT
    CAPABILITIES = f"{API_ROOT}/capabilities"
    FDLIB = f"{API_ROOT}/FDLib"
    PICTURE_UPLOAD = f"{FDLIB}/pictureUpload?type=concurrent"
