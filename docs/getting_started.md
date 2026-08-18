# Creating your first device with pykvision

This guide explains how the `pykvision` framework is organized, how it communicates with Hikvision devices, and how the main data structures behave in practice.

The project follows a layered design: the user works with high-level device objects, those objects delegate to services, and the services use a low-level HTTP client to talk to the device ISAPI endpoints.

---

## 1. How the framework works

The main execution flow is:

```text
User code
  ↓
Device object (NVR / Camera)
  ↓
Service layer
  ↓
ISAPIClient
  ↓
Hikvision ISAPI endpoint
  ↓
XML response
  ↓
XML parser
  ↓
Python dataclass / schema
  ↓
Returned to the user
```

This separation keeps the library easy to use while still exposing the lower-level request/response details when needed.

### The main building blocks

#### Device layer

The device layer is the public entry point for users. In this project, `NVR` is the main device abstraction. It encapsulates:

- connection configuration;
- the HTTP client;
- access to system and intelligent services;
- common high-level operations for the device.

Example:

```python
from pykvision.devices import NVR
from pykvision.models.dataclasses import ConfigConnection

config = ConfigConnection(
    ip_address="192.168.1.100",
    username="admin",
    passwd="your-password",
    use_https=False,
)

nvr = NVR(config)
```

Once the device is created, you can call methods like:

```python
info = nvr.get_system_device_info()
capabilities = nvr.get_intelligent_capabilities()
```

The idea is that users should interact with a device abstraction rather than manually building URLs or handling XML conversions.

#### Service layer

The service layer takes care of endpoint-specific logic. It converts HTTP responses into meaningful Python models.

The project currently distinguishes between:

- `SystemService`: system endpoints such as device info and capabilities;
- `IntelligentService`: video analytics and intelligent features.

This layer is responsible for:

- requesting the correct endpoint;
- parsing the XML response;
- filling the appropriate dataclass or schema object;
- returning clean Python objects.

#### Client layer

`ISAPIClient` is the low-level HTTP client. It handles:

- URL construction;
- session creation;
- HTTP Digest Authentication;
- requests to Hikvision endpoints;
- raw response retrieval.

It does not contain business logic about a specific device feature; instead, it focuses on the transport layer.

Example:

```python
from pykvision.client import ISAPIClient
from pykvision.models.dataclasses import ConfigConnection

config = ConfigConnection(
    ip_address="192.168.1.100",
    username="admin",
    passwd="password",
    use_https=False,
)

client = ISAPIClient(config)
client.get_system_device_info()
client.get_intelligent_capabilities()
```

The client builds a URL like:

```text
http://192.168.1.100:80/ISAPI/System/deviceInfo
```

or

```text
https://192.168.1.100:443/ISAPI/Intelligent/capabilities
```

depending on the configuration.

---

## 2. Execution model

### Step 1: Create a configuration

The `ConfigConnection` dataclass is the starting point of every connection.

```python
from pykvision.models.dataclasses import ConfigConnection

config = ConfigConnection(
    ip_address="192.168.1.100",
    username="admin",
    passwd="admin123",
    use_https=False,
)
```

Fields:

- `ip_address`: the device IP or hostname.
- `username`: account username used for authentication.
- `passwd`: password used for authentication.
- `use_https`: when `True`, the library uses HTTPS and port `443`; otherwise it uses HTTP and port `80`.

This object centralizes the connection information and avoids spreading raw connection arguments all over the codebase.

### Step 2: Instantiate a device

The recommended public API is to create a device object, not to call the client directly in application code.

```python
from pykvision.devices import NVR

nvr = NVR(config)
```

During initialization, `NVR` creates:

- `self.isapi_client = ISAPIClient(self.config)`;
- `self.intelligent = self.isapi_client.generate_instance_intelligent()`;
- `self.system = self.isapi_client.generate_instance_system()`.

This means the device immediately loads the important data models for the system and intelligent domains, so those structures are ready to use.

### Step 3: Call a public device method

```python
info = nvr.get_system_device_info()
print(info.device_name)
print(info.model)
```

This method delegates to the underlying system service, which fetches the XML, parses it, and stores the result inside a `DeviceInfo` object.

### Step 4: Parse the XML response

The response from Hikvision is usually XML. `pykvision` normalizes that response to a Python dictionary and then fills the corresponding dataclass.

The actual conversion path is roughly:

```text
HTTP response text
  → xml_parse_dict(...)
  → dict structure
  → set_* method in service
  → dataclass attribute assignment
```

This keeps the XML conversion logic in a single place, instead of scattering parsing routines across many files.

---

## 3. Main project structure and responsibilities

The library is intentionally layered.

```text
pykvision/
├── client.py
├── devices.py
├── services.py
├── xmlparse.py
├── models/
│   ├── dataclasses.py
│   ├── endpoints.py
│   ├── exceptions.py
│   ├── interfaces.py
│   ├── vca.py
│   └── schemes/
│       ├── intelligent.py
│       └── system.py
```

### `client.py`

Contains the raw communication layer.

It is responsible for:

- building the correct HTTP URL;
- establishing a session;
- handling HTTP Digest Authentication;
- making GET/POST requests;
- exposing request methods to the rest of the framework.

### `devices.py`

Contains business-facing device abstractions like `NVR` and `Camera`.

These objects represent the actual hardware and provide a cleaner API for the end user.

### `services.py`

Holds endpoint-specific logic for each functional domain.

Its purpose is to:

- call the client;
- receive XML responses;
- convert them into Python structures;
- expose domain-specific methods.

### `models/`

Contains the data models that describe incoming data and API payloads.

This includes:

- `dataclasses.py`: generic data containers;
- `schemes/system.py`: system-level response schemas;
- `schemes/intelligent.py`: analytics and intelligent feature schemas;
- `vca.py`: virtual face/person abstractions used for upload workflows.

---

## 4. How the data structures behave

The project relies heavily on Python dataclasses to represent the API payloads and results. Dataclasses are chosen because they are simple, typed, and easy to inspect.

### `ConfigConnection`

```python
@dataclass
class ConfigConnection:
    ip_address: str
    username: str = "admin"
    passwd: str = "admin"
    use_https: bool = False
```

Behavior:

- stores connection information in one object;
- used to build the HTTP session;
- controls whether the client uses HTTP or HTTPS.

This is the starting point for all device communication.

### `PersonInfoExtend`

```python
@dataclass
class PersonInfoExtend:
    id: int = 0
    enable: bool = False
    name: str = ""
    value: str = "No Info provided"
```

Behavior:

- represents an optional metadata field attached to a person record;
- usually used when storing additional labels or attributes related to a face library person;
- becomes part of the more complete face payload.

### `PersonInfoExtendList`

```python
@dataclass
class PersonInfoExtendList:
    PersonInfoExtend: list = field(default_factory=list)
```

Behavior:

- wraps a list of `PersonInfoExtend` entries;
- acts as a container for custom person metadata;
- is then inserted into the face upload structure.

### `FaceAppendData`

```python
@dataclass
class FaceAppendData:
    name: str = "None"
    bornTime: str = "1990-01-01"
    sex: str = "male"
    certificateType: str = "ID"
    certificateNumber: int = 1
    PersonInfoExtendList: PersonInfoExtendList = field(default_factory=PersonInfoExtendList)
```

Behavior:

- represents the main body of the face registration payload;
- contains the personal identity fields required by Hikvision face registration;
- includes optional metadata entries used for extended person information.

This object is later converted into the XML payload required by the ISAPI upload call.

### `PictureUploadData`

```python
@dataclass
class PictureUploadData:
    FDID: str = ""
    FaceAppendData: FaceAppendData = field(default_factory=FaceAppendData)
```

Behavior:

- combines the target face library ID and the face record payload;
- used when uploading an image and associated person information;
- is one of the key objects in the face registration flow.

### `DeviceInfo`

```python
@dataclass(slots=True)
class DeviceInfo:
    device_name: str = ""
    model: str = ""
    serial_number: str = ""
    mac_address: str = ""
    firmare_version: str = ""
    firmware_released_date: str = ""
    encoder_version: str = ""
    encoder_released_date: str = ""
    device_type: str = ""
    telecontrol_id: int = 0
    hardware_version: str = ""
    decord_channel_nums: int = 0
    vga_nums: int = 0
    usb_nums: int = 0
    auxout_nums: int = 0
    region_version: str = ""
```

Behavior:

- represents the result of `GET /ISAPI/System/deviceInfo`;
- stores the main hardware and firmware details of the device;
- is filled by the `SystemService.generate_device_info()` method.

### `IntelliCapabilities`

```python
@dataclass(slots=True)
class IntelliCapabilities(Capabilities):
    is_face_support: bool = False
    is_behavior_support: bool = False
    ...
```

Behavior:

- represents the intelligent feature flags returned by the device;
- each field indicates whether a specific smart feature is supported;
- the library turns XML values such as `true` or `false` into Python booleans.

Examples of capabilities include:

- `is_face_support`
- `is_behavior_support`
- `is_line_detection_support`
- `is_group_support`
- `is_support_upload_face_picture_by_form`

### `SystemCapabilities`

This schema models the system capability payload for the device and is used to summarize the supported features of the system domain.

For example, it may include network support flags, serial support, and I/O-related capabilities.

### `Status`, `Cpu`, and `Memory`

These dataclasses represent runtime state information.

```python
@dataclass(slots=True)
class Cpu:
    cpu_description: str = ""
    cpu_utilization: str = ""

@dataclass(slots=True)
class Memory:
    memory_description: str = ""
    memory_usage: float = 0.0
    memory_available: float = 0.0
```

Behavior:

- `Cpu` describes CPU information and usage metrics.
- `Memory` captures memory usage and availability.
- `Status` groups both into a device status object.

### `Person`

The `Person` class is a convenience wrapper for creating face-library entries.

```python
person = Person(
    name="John",
    born_time="15/02/1990",
    sex="male",
    certificateType="ID",
    certificateNumber=12345,
    fdid="1001",
    tags=[{"id": 1, "enable": True, "name": "role", "value": "employee"}],
    image_path=Path("person.jpg"),
)
```

Behavior:

- accepts user-friendly values instead of raw ISAPI XML fragments;
- converts the birth date into the format expected by the device;
- builds `PersonInfoExtendList`, `FaceAppendData`, and `PictureUploadData` automatically;
- makes the face upload flow much easier for the user.

This is one of the most Pythonic parts of the library because it hides the XML details behind a high-level object.

---

## 5. What happens during a person upload

The face upload flow is a good example of the whole architecture in action.

```python
from pathlib import Path
from pykvision.devices import NVR
from pykvision.models.dataclasses import ConfigConnection
from pykvision.models.vca import Person

config = ConfigConnection(
    ip_address="192.168.1.100",
    username="admin",
    passwd="password",
    use_https=False,
)

nvr = NVR(config)

person = Person(
    name="John",
    born_time="15/02/1990",
    sex="male",
    certificateType="ID",
    certificateNumber=12345,
    fdid="1001",
    tags=[{"id": 1, "enable": True, "name": "role", "value": "employee"}],
    image_path=Path("person.jpg"),
)

status = nvr.insert_person_in_face_library(person)
print(status)
```

The flow is:

1. `Person` builds a valid face payload object.
2. `NVR.insert_person_in_face_library()` calls the internal client.
3. `ISAPIClient.post_upload_person_db()` sends the multipart request.
4. The payload is created by converting the dataclass structure into XML.
5. The device receives the face data and image and returns a status code.

The conversion from Python data to XML is centralized in the service layer, not repeated manually in user code.

---

## 6. Typical usage patterns

### Basic device info query

```python
from pykvision.devices import NVR
from pykvision.models.dataclasses import ConfigConnection

config = ConfigConnection(
    ip_address="192.168.1.100",
    username="admin",
    passwd="your-password",
    use_https=False,
)

nvr = NVR(config)
info = nvr.get_system_device_info()
print(info.model)
print(info.device_name)
```

### Intelligent capability query

```python
capabilities = nvr.get_intelligent_capabilities()
print(capabilities.is_face_support)
print(capabilities.is_behavior_support)
```

### Direct client access

```python
from pykvision.client import ISAPIClient

client = ISAPIClient(config)
client.get_system_device_info()
client.get_intelligent_capabilities()
```

This is useful when you want to access the lower-level request layer without going through the device abstraction.

---

## 7. Important design principles

The project deliberately follows a few core rules:

- keep the user-facing API simple;
- hide raw XML and endpoint strings when possible;
- use typed dataclasses instead of raw dictionaries everywhere possible;
- isolate HTTP and parsing logic from device behavior;
- use services and schemas to separate responsibilities.

This is why the library exposes `NVR` and `Camera`, rather than requiring developers to manually call raw `requests` code every time.

---

## 8. Practical advice for using the library

1. Always create a `ConfigConnection` first.
2. Use `NVR` for recorder-like devices and future device abstractions.
3. Prefer the high-level methods over direct endpoint calls when possible.
4. Treat the dataclasses as the data contracts returned by the device.
5. For face enrollment, build a `Person` object and let the framework generate the payload for you.
6. Keep credentials and device access restricted to trusted environments.

---

## 9. Final summary

`pykvision` is a small but structured framework for Hikvision ISAPI interactions. It aims to provide a clean Pythonic experience while preserving the real device semantics of the API.

The most important idea is this:

- `ConfigConnection` holds device access configuration;
- `NVR` and `Camera` represent physical devices;
- `ISAPIClient` handles HTTP communication;
- `Service` classes parse and organize responses;
- dataclasses and schema objects represent the data returned by the device;
- `Person` simplifies face-registration workflows.

With this design, the user can work with high-level device objects instead of manually dealing with XML, authentication, and endpoint details.

That is the core of how the framework is intended to work.
