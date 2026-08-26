"""
This module represents all the data contained in the
endpoints GET /ISAPI/System/...
"""

from dataclasses import dataclass,field
from pykvision.models.interfaces import Capabilities
from pykvision.xmlparse import to_bool_xml

FIELD_MAP_DEVICE_INFO = {
    "deviceName": "device_name",
    "model": "model",
    "serialNumber": "serial_number",
    "macAddress": "mac_address",
    "firmwareVersion": "firmare_version",
    "firmwareReleasedDate": "firmware_released_date",
    "encoderVersion": "encoder_version",
    "encoderReleasedDate": "encoder_released_date",
    "deviceType": "device_type",
    "telecontrolID": "telecontrol_id",
    "hardwareVersion": "hardware_version",
    "decordChannelsNums": "decord_channel_nums",
    "VGANums": "vga_nums",
    "USBNums": "usb_nums",
    "regionVersion": "region_version",
}

FIELD_MAP_CAPABILITIES = {
    "SnmpCap": {
        "isSupport": "is_support",
    },
    "NetworkCap": {
        "isSupportWireless": "is_support_wireless",
        "isSupportWan": "is_support_wan",
        "isSupportBond": "is_support_bond",
        "isSupport8021x": "is_support_802_1x",
        "isSupportNtp": "is_support_ntp",
        "isSupportFtp": "is_support_ftp",
        "isSupportUpnp": "is_support_upnp",
        "isSupportPnp": "is_support_pnp",
        "isSupportDdns": "is_support_ddns",
        "isSupportHttps": "is_support_https",
        "isSupportExtNetCfg": "is_support_ext_net_cfg",
        "isSupportIpFilter": "is_support_ip_filter",
        "isSupportNetPreviewStrategy": "is_support_net_preview_strategy",
        "isSupportEzviz": "is_support_ezviz",
        "isSupportMacFilter": "Is_support_mac_filter",
        "isSupportIntegrate": "is_support_integrate",
        "isSupportEzvizTiming": "is_support_ezviz_timing",
        "isSupportResourceStatistics": "is_support_resource_statistics",
        "isSupportBandwidthLimit": "is_support_bandwidth_limit",
        "isSupportPoePortsDisableAdaptativeServer": "is_support_poe_ports_disable_adaptative_server",
        "isSupportPoeConfiguration": "is_support_poe_configuration",
        "isSupportGetLinkSocketIp": "is_support_get_link_socket_ip",
    },
    "IOCap": {
        "ioInputPortsNums": "io_input_ports_nums",
        "ioOutputPortsNums": "io_output_ports_ums",
        "softIoInputPortsNums": "soft_io_input_ports_nums",
        "isSupportIoOutputAdvanceParameter": "is_support_io_output_advance_parameter",
        "isSupportCombinationAlarm": "is_support_combination_alarm",
        "isSupportSetAllOutput": "is_support_set_all_output",
        "enabledIoOutputPortNums": "enabled_io_output_port_nums",
        "isSupportAlarmKeyParam": "is_support_alarm_key_param",
    },
    "SerialCap": {
        "rs485PortNums": "rs485_port_nums",
        "isSupportRS232Config": "is_support_RS232_config",
        "rs422PortNums": "rs422_port_nums",
        "rs232PortNums": "rs232_port_nums",
        "isSupportAuthenticationService": "is_support_authentication_service",
    },
    "VideoCap": {
        "videoInputPortNums": "video_input_port_nums",
        "videoOutputPortNums": "video_output_port_nums",
        "menuNums": "menu_nums",
        "isSupportCounting": "is_support_counting",
        "coutingType": "couting_type",
        "isSupportOutputResource": "is_support_output_resource",
        "isSupportMultiChannelCounting": "is_support_multi_channel_counting",
        "isSupportCoutingCollection": "is_support_couting_collection",
        "isSupportHeatmapCollection": "is_support_heatmap_collection",
        "channelFlexible": "channel_flexible",
        "isSupportMixedChannel": "is_support_mixed_channel",
        "isSupportMixedChannelStatus": "is_support_mixed_channel_status",
    },
    "AudioCap": {
        "audioInputNums": "audio_input_nums",
        "audioOutputNums": "audio_output_nums",
    },
    "SecurityCap": {
        "supportUsersNums": "support_users_nums",
        "userBondIpNums": "user_bond_ip_nums",
        "userBondMacNums": "user_bond_mac_nums",
        "securityVersion": "security_version",
        "keyIterateNum": "key_iterate_num",
        "isSupportUserCheck": "is_support_user_check",
        "isSupportGuidFileDataExport": "is_support_guid_file_data_export",
        "isSupportSecurityQuestionConfig": "is_support_security_question_config",
        "isSupportSecurityEmail": "is_support_security_email",
        "isSupportGetOnlineUserListSc": "is_support_get_online_user_list_sc",
        "isSupportOnvifUserManagement": "is_support_onvif_user_management",
        "isSupportConfigFileImport": "is_support_config_file_import",
        "isSupportConfigFileExport": "is_support_config_file_export",
        "supportIpcActivatePassword": "support_ipc_activate_password",
        "isSupportPictureUrlCertificate": "is_support_picture_url_certificate",
        "isSupportUnloggedUserPermissionConfig": "is_support_unlogged_user_permission_config",
        "isSupportUserNamePasswordCheckUpgrade": "is_support_user_name_password_check_upgrade",
        "isSupportDeviceCertificatesManagement": "is_support_device_certificates_management",
        "isSupportDeviceSelfSignCertExport": "is_support_device_self_sign_cert_export",
    },
    "EventCap": {
        "isSupportHdFull": "is_support_hd_full",
        "isSupportHdError": "is_support_hd_error",
        "isSupportNicBroken": "is_support_nic_broken",
        "isSupportIpConflict": "is_support_ip_conflict",
        "isSupportIllAccess": "is_support_ill_access",
        "isSupportViException": "is_support_vi_exception",
        "isSupportViMismatch": "is_support_vi_mismatch",
        "isSupportRecordException": "is_support_record_exception",
        "isSupportRaidException": "is_support_raid_exception",
        "isSupportPocException": "is_support_poc_exception",
        "isSupportSmartDetection": "is_support_smart_detection",
        "isSupportSpareException": "is_support_spare_exception",
        "isSupportHumanRecognition": "is_support_human_recognition",
        "isSupportFaceContrast": "is_support_face_contrast",
        "isSupportWhiteListFaceContrast": "is_support_white_list_face_contrast",
        "isSupportStudentsStoodUp": "is_support_students_stood_up",
        "isSupportFaceSnap": "is_support_face_snap",
        "isSupportPersonDensityDetection": "is_support_person_density_detection",
        "isSupportPersonQueueDetection": "is_support_person_queue_detection",
        "isSupportSafetyHelmetDetection": "is_support_safety_helmet_detection",
        "isSupportTeacherBehaviorDetect": "is_support_teacher_behavior_detect",
        "isSupportCityManagement": "is_support_city_management",
        "isSupportMixedTargetDetection": "is_support_mixed_target_detection",
        "isSupportFaceSnapModeling": "is_support_face_snap_modeling",
        "isSupportTriggerCapCheck": "is_support_trigger_cap_check",
        "isSupportPteEventCft": "is_support_pte_event_cft",
    },
}


@dataclass(slots=True)
class DeviceInfo:
    """
    Represents the endpoint:

        GET /ISAPI/System/deviceInfo
    """
    device_name:str = ""
    model:str = "" 
    serial_number:str=""
    mac_address:str=""
    firmare_version:str=""
    firmware_released_date:str=""
    encoder_version:str=""
    encoder_released_date:str=""
    device_type:str=""
    telecontrol_id:int=0
    hardware_version:str=""
    decord_channel_nums:int=0
    vga_nums:int=0
    usb_nums:int=0
    auxout_nums:int=0
    region_version:str=""
@dataclass(slots=True)
class SnmpCap:
    is_support:bool=False      
@dataclass(slots=True)
class NetwokCap:
    is_support_wireless:bool=False
    is_support_wan:bool=False
    is_support_bond:bool=False
    is_support_802_1x:bool=False
    is_support_ntp:bool=False
    is_support_ftp:bool=False
    is_support_upnp:bool=False
    is_support_pnp:bool=False 
    is_support_ddns:bool=False
    is_support_https:bool=False
    SnmpCap:SnmpCap = field(default_factory=SnmpCap)
    is_support_ext_net_cfg:bool=False
    is_support_ip_filter:bool=False 
    is_support_net_preview_strategy:bool=False 
    is_support_ezviz:bool=False 
    Is_support_mac_filter:bool=False 
    is_support_integrate:bool=False
    is_support_ezviz_timing:bool=False 
    is_support_resource_statistics:bool=False
    is_support_bandwidth_limit:bool=False 
    is_support_poe_ports_disable_adaptative_server:bool=False 
    is_support_poe_configuration:bool=False 
    is_support_get_link_socket_ip:bool=False
@dataclass(slots=True)
class IOCap:
    io_input_ports_nums:int =0
    io_output_ports_ums:int = 0
    soft_io_input_ports_nums:int = 0
    is_support_io_output_advance_parameter:bool = False
    is_support_combination_alarm:bool = False 
    is_support_set_all_output:bool = False 
    enabled_io_output_port_nums:int=0
    is_support_alarm_key_param:bool=False
@dataclass(slots=True)
class SerialCap:
    rs485_port_nums:int=0
    is_support_RS232_config:bool=False
    rs422_port_nums:int=0
    rs232_port_nums:int=0
    is_support_authentication_service:bool=False

@dataclass(slots=True)
class VideoCap:
    video_input_port_nums:int = 0
    video_output_port_nums:int = 0
    menu_nums:int = 0
    is_support_counting:bool = False
    couting_type:str = ""
    is_support_output_resource:bool = False
    is_support_multi_channel_counting:bool = False
    is_support_couting_collection:bool = False
    is_support_heatmap_collection:bool = False
    channel_flexible:list = field(default_factory=list)
    is_support_mixed_channel:bool = False
    is_support_mixed_channel_status:bool = False
@dataclass(slots=True)
class AudioCap:
    audio_input_nums:int = 0
    audio_output_nums:int = 0
@dataclass(slots=True)    
class SecurityCap:
    support_users_nums:int = 1
    user_bond_ip_nums:int = 1
    user_bond_mac_nums:int = 1
    security_version:str = ""
    key_iterate_num:int = 0
    is_support_user_check:bool = False
    is_support_guid_file_data_export:bool = False
    is_support_security_question_config:bool = False
    is_support_security_email:bool = False
    is_support_get_online_user_list_sc:bool = False
    is_support_onvif_user_management:bool = False
    is_support_config_file_import:bool = False
    is_support_config_file_export:bool = False
    support_ipc_activate_password:bool = False
    is_support_picture_url_certificate:bool = False
    is_support_unlogged_user_permission_config:bool = False
    is_support_user_name_password_check_upgrade:bool = False
    is_support_device_certificates_management:bool = False
    is_support_device_self_sign_cert_export:bool = False
@dataclass
class EventCap:
    is_support_hd_full:bool = False
    is_support_hd_error:bool = False
    is_support_nic_broken:bool = False
    is_support_ip_conflict:bool = False
    is_support_ill_access:bool = False
    is_support_vi_exception:bool = False
    is_support_vi_mismatch:bool = False
    is_support_record_exception:bool = False
    is_support_raid_exception:bool = False
    is_support_poc_exception:bool = False
    is_support_smart_detection:bool = False
    is_support_spare_exception:bool = False
    is_support_human_recognition:bool = False
    is_support_face_contrast:bool = False
    is_support_white_list_face_contrast:bool = False
    is_support_students_stood_up:bool = False
    is_support_face_snap:bool = False
    is_support_person_density_detection:bool = False
    is_support_person_queue_detection:bool = False
    is_support_safety_helmet_detection:bool = False
    is_support_teacher_behavior_detect:bool = False
    is_support_city_management:bool = False
    is_support_mixed_target_detection:bool = False
    is_support_face_snap_modeling:bool = False
    is_support_trigger_cap_check:bool = False
    is_support_pte_event_cft:bool = False

@dataclass(slots=True)
class SystemCapabilities(Capabilities):
    """
    Represents the endpoint:

        GET /ISAPI/System/capabilities
    """
    is_support_dst:bool=False
    NetworkCap:NetwokCap = field(default_factory=NetwokCap)
    IOCap:IOCap = field(default_factory=IOCap)
    SerialCap:SerialCap = field(default_factory=SerialCap)
    VideoCap:VideoCap = field(default_factory=VideoCap)
    AudioCap:AudioCap = field(default_factory=AudioCap)
    SecurityCap:SecurityCap = field(default_factory=SecurityCap)
    EventCap:EventCap = field(default_factory=EventCap)
    
@dataclass(slots=True)     
class Cpu:
    cpu_description:str=""
    cpu_utilization:str=""
@dataclass(slots=True)  
class Memory:
    memory_description:str="" 
    memory_usage:float=0.0
    memory_available:float=0.0

@dataclass(slots=True)   
class Status:
    cpu:Cpu=field(default_factory=Cpu)
    memoryList:list[Memory]=field(default_factory=list)
@dataclass(slots=True)
class SystemScheme:
    """
    This is a dataclass representation of the XML response of endpoint Intelligent
    """
    deviceInfo:DeviceInfo = field(default_factory=DeviceInfo)
    capabilities:SystemCapabilities = field(default_factory=SystemCapabilities)
    status:Status = field(default_factory=Status)

    def set_device_info(self,data:dict) -> None:
        for xml_name, attr_name in FIELD_MAP_DEVICE_INFO.items():
            setattr(self.deviceInfo, attr_name, to_bool_xml(data.get(xml_name,False)))

    def set_capabilities(self,data:dict) -> None:
        for cap_name, field_map in FIELD_MAP_CAPABILITIES.items():
            if cap_name == "SnmpCap":
                capability = self.capabilities.NetworkCap.SnmpCap
                capability_data = data.get("NetwokCap", {}).get(cap_name, {})
            else:
                capability = getattr(self.capabilities, cap_name)
                capability_data = data.get(cap_name, {})

            for xml_name, attr_name in field_map.items():
                setattr(
                    capability,
                    attr_name,
                    to_bool_xml(capability_data.get(xml_name, False)),
                )