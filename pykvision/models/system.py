"""
This module represents all the data contained in the
endpoints GET /ISAPI/System/...
"""

from dataclasses import dataclass,field

from pykvision.xmlparse import to_bool_xml

FIELD_MAP = {
    "deviceName": "deviceName",
    "model": "model",
    "serialNumber": "serialNumber",
    "macAddress": "macAddress",
    "firmwareVersion": "firmareVersion",
    "firmwareReleasedDate": "firmwareReleasedDate",
    "encoderVersion": "encoderVersion",
    "encoderReleasedDate": "encoderReleasedDate",
    "deviceType": "deviceType",
    "telecontrolID": "telecontrolID",
    "hardwareVersion": "hardwareVersion",
    "decordChannelsNums": "decordChannelNums",
    "VGANums": "vgaNums",
    "USBNums": "usbNums",
    "regionVersion": "regionVersion",
}


@dataclass(slots=True)
class DeviceInfo:
    """
    Represents the endpoint:

        GET /ISAPI/System/deviceInfo
    """
    deviceName:str = ""
    model:str = "" 
    serialNumber:str=""
    macAddress:str=""
    firmareVersion:str=""
    firmwareReleasedDate:str=""
    encoderVersion:str=""
    encoderReleasedDate:str=""
    deviceType:str=""
    telecontrolID:int=0
    hardwareVersion:str=""
    decordChannelNums:int=0
    vgaNums:int=0
    usbNums:int=0
    auxoutNums:int=0
    regionVersion:str=""
@dataclass(slots=True)
class SnmpCap:
    isSupport:bool=False      
@dataclass(slots=True)
class NetwokCap:
    isSupportWireless:bool=False
    isSupportWan:bool=False
    isSupportBond:bool=False
    isSupport802_1x:bool=False
    isSupportNtp:bool=False
    isSupportFtp:bool=False
    isSupportUpnp:bool=False
    isSupportPNP:bool=False 
    isSupportDdns:bool=False
    isSupportHttps:bool=False
    SnmpCap:SnmpCap = field(default_factory=SnmpCap)
    isSupportExtNetCfg:bool=False
    isSupportIPFilter:bool=False 
    isSupportNetPreviewStrategy:bool=False 
    isSupportEZVIZ:bool=False 
    IsSupportMACFilter:bool=False 
    isSupportIntegrate:bool=False
    isSupportEZVIZTiming:bool=False 
    isSupportResourceStatistics:bool=False
    isSupportBandwidthLimit:bool=False 
    isSupportPOEPortsDisableAdaptativeServer:bool=False 
    isSupportPOEConfiguration:bool=False 
    isSupportGetLinkSocketIP:bool=False
@dataclass(slots=True)
class IOCap:
    IOInputPortsNums:int =0
    IOOutputPortsNums:int = 0
    SoftIOInputPortsNums:int = 0
    IsSupportIOOutputAdvanceParameter:bool = False
    isSupportCombinationAlarm:bool = False 
    isSupportSetAllOutput:bool = False 
    enabledIOOutputPortNums:int=0
    isSupportAlarmKeyParam:bool=False
@dataclass(slots=True)
class SerialCap:
    rs485PortNums:int=0
    isSupportRS232Config:bool=False
    rs422PortNums:int=0
    rs232PortNums:int=0
    isSupportAuthenticationService:bool=False

@dataclass(slots=True)
class Capabilities:
    """
    Represents the endpoint:

        GET /ISAPI/System/capabilities
    """
    isSupportDst:bool=False
    NetwokCap:NetwokCap = field(default_factory=NetwokCap)
    IOCap:IOCap = field(default_factory=IOCap)
    SerialCap:SerialCap = field(default_factory=SerialCap)
@dataclass(slots=True)     
class Cpu:
    cpuDescription:str=""
    cpuUtilization:str=""
@dataclass(slots=True)  
class Memory:
    MemoryDescription:str="" 
    MemoryUsage:float=0.0
    MemoryAvailable:float=0.0
@dataclass(slots=True)   
class Status:
    cpu:Cpu=field(default_factory=Cpu)
    MemoryList:list[Memory]=field(default_factory=list)
@dataclass(slots=True)

class System:
    """
    Represents the endpoint:

        GET /ISAPI/System/
    """
    deviceInfo:DeviceInfo = field(default_factory=DeviceInfo)
    capabilities:Capabilities = field(default_factory=Capabilities)
    status:Status = field(default_factory=Status)

    def set_device_info(self,data:dict) -> None:
        for xml_name, attr_name in FIELD_MAP.items():
            setattr(self.deviceInfo, attr_name, to_bool_xml(data.get(xml_name,False)))

    def set_capabilities(self,data:dict) -> None:
        pass