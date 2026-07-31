# pykvision

`pykvision` is a small Python library for working with Hikvision cameras and NVRs through the
ISAPI API. It handles the HTTP connection, Digest Authentication, XML responses, and converts
device information into Python dataclasses.

The project is still growing, but the main idea is simple: provide a convenient device-level API
for cameras and NVRs without making users deal with every ISAPI response by hand.

## How it works

The library is organized in two layers:

1. A device class such as `Nvr` represents the Hikvision product being used.
2. The device uses `ISAPIClient` internally to connect with the product using its IP address and
	credentials.
3. The client requests an ISAPI endpoint.
4. The response XML is parsed into a dictionary.
5. A service maps that data into Python models such as `System` and `Intelligent`.

The current models cover device information and capability information from system and intelligent
endpoints. `Nvr` already wraps the intelligent capabilities flow, while the `Camera` class is still
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

## Basic NVR example

For an NVR, use the device class instead of working with the ISAPI client directly:

```python
from pykvision.devices import Nvr

nvr = Nvr("192.168.1.100", "admin", "your-password")

capabilities = nvr.get_intelligent_capabilities
print(capabilities.is_face_support)
print(capabilities.is_behavior_support)
```

The NVR must be reachable from your machine, and the account must have permission to access the
requested ISAPI endpoints. The `Nvr` class uses `ISAPIClient` internally, so application code can
work with the device abstraction instead of managing the client directly.

`ISAPIClient` is still available as the lower-level layer when direct endpoint access is needed.

> Note: `pykvision/devices.py` currently contains a development-time `nvr_facial` instance at the
> bottom of the file. Remove or comment out that line before importing `Nvr` in another application,
> otherwise it will try to connect to the hard-coded device during import.

## Project structure

```text
pykvision/
├── client.py       # Low-level ISAPI HTTP client
├── devices.py      # Camera and NVR device classes
├── endpoints.py    # ISAPI endpoint paths
├── exceptions.py   # Project exceptions
├── services.py     # XML parsing and model population
├── xmlparse.py     # XML/dictionary conversion helpers
├── models/         # Dataclasses for system and intelligent data
├── events/         # Event-related code
└── inteligent/     # Intelligent camera and NVR features

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
