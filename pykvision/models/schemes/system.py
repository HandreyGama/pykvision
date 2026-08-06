"""
This module represents all the data contained in the
endpoints GET /ISAPI/System/...
"""

from dataclasses import dataclass,field
from pykvision.models.interfaces import Capabilities
from pykvision.xmlparse import to_bool_xml

FIELD_MAP = {
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
    firmware_releasedDate:str=""
    encoder_version:str=""
    encoder_releasedDate:str=""
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
class SystemCapabilities(Capabilities):
    """
    Represents the endpoint:

        GET /ISAPI/System/capabilities
    """
    is_supportDst:bool=False
    NetwokCap:NetwokCap = field(default_factory=NetwokCap)
    IOCap:IOCap = field(default_factory=IOCap)
    SerialCap:SerialCap = field(default_factory=SerialCap)
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
        for xml_name, attr_name in FIELD_MAP.items():
            setattr(self.deviceInfo, attr_name, to_bool_xml(data.get(xml_name,False)))

    def set_capabilities(self,data:dict) -> None:
        pass