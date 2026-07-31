# pykvision

`pykvision` is a small Python library for working with Hikvision products through the ISAPI API.
It handles the HTTP connection, Digest Authentication, XML responses, and converts some camera
information into Python dataclasses.

The project is still growing, but the main idea is simple: make it easier to read Hikvision products
data from Python without dealing with every ISAPI response by hand.

## How it works

The library follows a small flow:

1. `ISAPIClient` connects to the camera using its IP address and credentials.
2. It requests an ISAPI endpoint.
3. The response XML is parsed into a dictionary.
4. A service maps that data into Python models such as `System` and `Intelligent`.

The current models cover device information and capability information from the system and
intelligent endpoints.

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

```bash
python -m pip install -e .
```

## Testing

Install the development dependencies and run pytest:

```bash
python -m pip install -r dev-requirements.txt
pytest
```

The test suite is currently minimal and will expand as more endpoints and models are added.

## Basic example

The client is initialized with the camera IP address, username, and password:

```python
from pykvision.client import ISAPIClient

client = ISAPIClient("192.168.1.100", "admin", "your-password")
client.get_system_device_info()

device_info = client.SystemService.sys.deviceInfo
print(device_info.model)
print(device_info.serialNumber)
```

The product must be reachable from your machine, and the account must have permission to access
the requested ISAPI endpoints.

> Note: `pykvision/client.py` currently contains a development-time example at the bottom of the
> file that makes a camera request when the module is imported. Remove or comment out those lines
> before using the client in another application.

## Project structure

```text
pykvision/
├── client.py       # HTTP client and camera requests
├── devices.py      # Device-related helpers
├── endpoints.py    # ISAPI endpoint paths
├── exceptions.py   # Project exceptions
├── services.py     # XML parsing and model population
├── xmlparse.py     # XML/dictionary conversion helpers
├── models/         # Dataclasses for system and intelligent data
├── events/         # Event-related code
└── inteligent/     # Intelligent camera features

tests/              # Automated tests
docs/               # Project documentation
```

## Contributing

Contributions are welcome. A practical way to get started is:

1. Fork the repository.
2. Create a branch for your change.
3. Make the change and add or update tests when possible.
4. Run `pytest` before opening a pull request.
5. Open a pull request with a short explanation of what changed and why.

Small improvements are useful too, especially better endpoint coverage, clearer models, and tests
using representative Hikvision XML responses.

## License

This project is released under the license in [LICENSE](LICENSE).
