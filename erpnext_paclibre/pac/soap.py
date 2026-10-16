"""SOAP transport for Certificación CFDI."""

import requests


SOAP11_ENVELOPE = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        {body}
    </soap:Body>
</soap:Envelope>
"""


class SoapError(Exception):
    """Raised when the SOAP service returns an HTTP error."""


class SoapClient:
    """Minimal SOAP 1.1 client for the Certifica CFDI service."""

    def __init__(self, endpoint: str, timeout: int = 120):
        self.endpoint = endpoint
        self.timeout = timeout

    def call(self, action: str, body: str) -> bytes:
        envelope = SOAP11_ENVELOPE.format(body=body)

        response = requests.post(
            self.endpoint,
            data=envelope.encode("utf-8"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": f'"{action}"',
            },
            timeout=self.timeout,
        )

        if not response.ok:
            raise SoapError(
                f"Certifica CFDI SOAP request failed "
                f"with HTTP {response.status_code}: {response.text}"
            )

        return response.content
