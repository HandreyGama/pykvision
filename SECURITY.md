# Security Policy

## Supported Versions

Security fixes are currently provided for the latest version of Pykvision available on the `main` branch.

| Version                  | Supported |
| ------------------------ | --------- |
| Latest release           | ✅         |
| Older releases           | ⚠️        |
| Unreleased / development | ❌         |

Because Pykvision is currently under active development, security support for older releases may vary.

## Reporting a Vulnerability

If you discover a security vulnerability in Pykvision, please **do not open a public GitHub issue**.

Instead, report the vulnerability privately so that it can be investigated and fixed before security-sensitive information becomes public.

When reporting a vulnerability, please provide as much information as possible, including:

* A description of the vulnerability.
* The affected Pykvision version or commit.
* The affected component, module, class, function, or endpoint.
* Steps to reproduce the issue.
* A proof of concept, if available.
* The potential impact of the vulnerability.
* Any suggested mitigation or fix, if available.

Please make sure that your report does **not** contain real credentials, passwords, API keys, private IP addresses, serial numbers, or other sensitive information from Hikvision devices.

### Reporting Through GitHub

If GitHub Security Advisories are enabled for this repository, please use the repository's **Security Advisories** feature to submit a private vulnerability report.

If private vulnerability reporting is not available, please contact the project maintainer through the contact method listed in the repository profile.

## What Should Be Reported?

Examples of security issues that should be reported privately include:

* Authentication bypasses.
* Credential leakage.
* Exposure of sensitive device information.
* Improper handling of authentication credentials.
* Vulnerabilities in HTTP requests made by Pykvision.
* XML injection or unsafe XML handling.
* Improper validation or sanitization of user-controlled data.
* Vulnerabilities that could allow unauthorized access to Hikvision devices.
* Remote code execution.
* Server-side request forgery (SSRF).
* Any vulnerability that could compromise the security of applications using Pykvision.

## Sensitive Information

Pykvision communicates with Hikvision devices through their ISAPI interface. Applications using Pykvision may therefore handle sensitive information such as:

* Device credentials.
* IP addresses.
* Network configuration.
* Device information.
* Face recognition data.
* Person information.
* Images.
* Access-control information.
* Other data exposed through Hikvision ISAPI endpoints.

Users are responsible for ensuring that sensitive information is handled securely in their applications.

### Credentials

Credentials should never be hard-coded into source code or committed to a repository.

For example, avoid:

```python
client = NVR(
    ip_addrs="192.168.1.100",
    username="admin",
    password="my-password"
)
```

Prefer using environment variables or another secure secret-management mechanism:

```python
import os

client = NVR(
    ip_addrs=os.environ["PYKVISION_HOST"],
    username=os.environ["PYKVISION_USERNAME"],
    password=os.environ["PYKVISION_PASSWORD"],
)
```

Never commit real credentials, `.env` files, private keys, or device configuration containing secrets.

## Responsible Disclosure

Please allow reasonable time for a vulnerability to be investigated and, when possible, fixed before publicly disclosing technical details.

After a security issue has been resolved, the project may publish a security advisory describing the vulnerability, its impact, and the affected versions.

Security researchers who responsibly disclose vulnerabilities may be credited in the corresponding security advisory, unless they prefer to remain anonymous.

## Security Best Practices

When using Pykvision in production environments:

1. Use strong and unique credentials for Hikvision devices.
2. Do not expose NVR or camera ISAPI interfaces directly to the public Internet unless absolutely necessary.
3. Restrict access to devices using firewalls, VLANs, VPNs, or other appropriate network controls.
4. Keep Hikvision firmware up to date.
5. Store credentials using environment variables or a dedicated secrets manager.
6. Avoid logging passwords, authentication headers, or sensitive device information.
7. Avoid committing real device information to public repositories.
8. Use HTTPS when supported and appropriate for the target device and network environment.
9. Keep Pykvision updated to the latest available release.
10. Treat face images, biometric information, and person data as sensitive information.

## Scope

This security policy covers vulnerabilities in the Pykvision library itself, including its:

* HTTP client implementation.
* Authentication handling.
* ISAPI endpoint implementations.
* XML serialization and parsing.
* Data models.
* Input validation.
* Request construction.
* Response processing.

Vulnerabilities that exist exclusively in Hikvision firmware, hardware, or the underlying ISAPI implementation should be reported to Hikvision through their appropriate security channels.

## Security Disclaimer

Pykvision is an independent open-source project and is not affiliated with or endorsed by Hikvision.

Pykvision provides an interface for interacting with Hikvision devices through their ISAPI interface. The security of the underlying device, firmware, network, and deployment environment remains the responsibility of the user.

---

Thank you for helping keep Pykvision and the applications built with it secure.
****
