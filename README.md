
# pykvision

`pykvision` is a small Python library for working with Hikvision cameras and NVRs through the
ISAPI API. It handles HTTP requests, Digest Authentication, XML parsing, and converts device
information into Python dataclasses.

The project is still growing, but the main idea is simple: provide a convenient device-level API
for cameras and NVRs without forcing developers to manually handle every ISAPI response.

## How it works

The library is organized in layers:

1. A device class such as `NVR` represents the Hikvision product being used.
2. The device uses `ISAPIClient` internally to connect to the product using its IP address and
   credentials.
3. The client requests an ISAPI endpoint.
4. The XML response is parsed into a dictionary.
5. A service maps that data into Python models such as `SystemScheme` and `IntelligentScheme`.

The current models cover device information and capability information from system and intelligent
endpoints. `NVR` already wraps the intelligent capabilities flow, while the `Camera` class is still
being expanded.

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/HandreyGama/pykvision.git
cd pykvision
```

Create a virtual environment and install the project:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Then install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Or install the package in editable mode:

```bash
python -m pip install -e .
```

## Development dependencies

Install the dev requirements and run pytest:

```bash
python -m pip install -r dev-requirements.txt
python -m pytest -q
```

The current test suite is minimal and will grow as more endpoints and model mappings are added.

## Basic NVR example

For an NVR, use the device class instead of working with the ISAPI client directly:

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
capabilities = nvr.get_intelligent_capabilities()
print(capabilities.is_face_support)
print(capabilities.is_behavior_support)
```

The NVR must be reachable from your machine, and the account must have permission to access the
requested ISAPI endpoints. The `NVR` class uses `ISAPIClient` internally, so application code can
work with the device abstraction instead of managing the client directly.

`ISAPIClient` is still available as the lower-level layer when direct endpoint access is needed.

## Project structure

```text
pykvision/
├── __init__.py
├── __main__.py
├── client.py
├── devices.py
├── services.py
├── xmlparse.py
├── models/
│   ├── dataclasses.py
│   ├── endpoints.py
│   ├── exceptions.py
│   ├── interfaces.py
│   └── schemes/
│       ├── intelligent.py
│       └── system.py
├── tests/
├── docs/
├── README.md
├── CONTRIBUTE.md
├── LICENSE
├── requirements.txt
├── dev-requirements.txt
├── pyproject.toml
├── CHANGELOG.md
└── .gitignore
```

## Main modules and functions

### `ISAPIClient`

Responsible for:

- building the target URL;
- creating the HTTP session;
- handling Digest Authentication;
- making requests to ISAPI endpoints;
- returning parsed device data.

### `NVR`

High-level wrapper for Hikvision NVR devices. It exposes methods such as:

- `get_intelligent_capabilities()`
- `get_system_device_info()`
- `insert_new_person_picture(...)`

### `Camera`

Represents an IP camera and serves as a base for future expansions.

### `SystemService`

Handles XML responses for system endpoints, including:

- device info;
- system capabilities.

### `IntelligentService`

Handles intelligent endpoints, including:

- intelligent capabilities;
- FDLib capabilities;
- XML generation for face picture upload payloads.

## Usage examples

### Read device info

```python
from pykvision.devices import NVR
from pykvision.models.dataclasses import ConfigConnection

config = ConfigConnection(
    ip_address="192.168.1.100",
    username="admin",
    passwd="admin123",
    use_https=False,
)

nvr = NVR(config)
info = nvr.get_system_device_info()
print(info.device_name)
print(info.model)
```

### Connect directly to the client

```python
from pykvision.client import ISAPIClient
from pykvision.models.dataclasses import ConfigConnection

config = ConfigConnection(
    ip_address="192.168.1.100",
    username="admin",
    passwd="admin123",
    use_https=False,
)

client = ISAPIClient(config)
client.get_system_device_info()
client.get_intelligent_capabilities()
```

### Generate XML for picture upload

```python
from pykvision.models.dataclasses import FaceAppendData, PictureUploadData
from pykvision.services import IntelligentService

face = FaceAppendData(
    name="John",
    bornTime="1990-01-01",
    sex="male",
    customHumanID=1234,
)

payload = PictureUploadData(FDID="1", FaceAppendData=face)
service = IntelligentService()
xml = service.generate_picture_upload_xml_data(payload)
print(xml)
```

## Troubleshooting

### `No module named 'xmltodict'`

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

or:

```bash
python -m pip install xmltodict requests
```

### Authentication errors

If the connection returns HTTP 401 or Digest auth fails:

- confirm the username and password;
- confirm the device supports Digest Authentication;
- verify the user has permission to access the target endpoint;
- test the URL manually in a browser or curl.

### Connection or timeout issues

- verify the IP address is correct;
- confirm the device is reachable on the same network;
- check whether the HTTP port is open (80 or 443);
- if using HTTPS, validate the certificate and `use_https` flag.

### Empty or invalid XML responses

- confirm the correct endpoint URL is being used;
- verify the device supports that capability;
- inspect the raw response from the device directly;
- review the firmware version and endpoint behavior.

### Import problems

If importing the package fails:

```bash
python -m pip install -e .
```

or:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Testing

Run the test suite with:

```bash
python -m pip install -r dev-requirements.txt
python -m pytest -q
```

## Contributing

Contributions are welcome. Please see [CONTRIBUTE.md](CONTRIBUTE.md) for the contribution workflow and standards.

## License

This project is released under the license in [LICENSE](LICENSE).
