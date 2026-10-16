"""Client for Certificación CFDI SAPI de CV."""

from __future__ import annotations

from lxml import etree

from .exceptions import CertificaCFDIInvalidResponse
from .soap import SoapClient
from .zip_utils import decode_zip, encode_zip


NAMESPACE = (
    "https://www.certificacfdi.mx/"
    "appcertificacfdi40/motorCFDI.asmx?WSDL"
)

ENDPOINT = (
    "https://www.certificacfdi.mx/"
    "appcertificacfdi40/motorCFDI.asmx"
)


class CertificaCFDIClient:
    """Client for the Certificación CFDI SOAP service."""

    def __init__(
        self,
        username: str,
        password: str,
        endpoint: str = ENDPOINT,
        timeout: int = 120,
    ):
        self.username = username
        self.password = password
        self.soap = SoapClient(
            endpoint=endpoint,
            timeout=timeout,
        )

    def _element(
        self,
        name: str,
        value: str | None = None,
    ) -> str:
        if value is None:
            value = ""

        escaped = (
            value.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

        return f"<{name}>{escaped}</{name}>"

    def _call(
        self,
        operation: str,
        fields: str,
    ) -> bytes:
        body = (
            f'<{operation} xmlns="{NAMESPACE}">'
            f"{fields}"
            f"</{operation}>"
        )

        action = f"{NAMESPACE}/{operation}"

        response = self.soap.call(
            action=action,
            body=body,
        )

        return self._extract_result(
            response=response,
            operation=operation,
        )

    def _extract_result(
        self,
        response: bytes,
        operation: str,
    ) -> bytes:
        try:
            root = etree.fromstring(response)
        except etree.XMLSyntaxError as exc:
            raise CertificaCFDIInvalidResponse(
                "Certifica CFDI returned invalid SOAP XML."
            ) from exc

        # SOAP Fault
        fault = root.find(
            ".//{http://schemas.xmlsoap.org/soap/envelope/}Fault"
        )

        if fault is not None:
            fault_text = " ".join(fault.itertext()).strip()

            raise CertificaCFDIInvalidResponse(
                f"Certifica CFDI SOAP Fault: {fault_text}"
            )

        result_name = f"{operation}Result"

        result = root.find(
            f".//{{{NAMESPACE}}}{result_name}"
        )

        if result is None:
            raise CertificaCFDIInvalidResponse(
                f"Certifica CFDI response does not contain "
                f"{result_name}."
            )

        return (
            result.text.encode("utf-8")
            if result.text
            else b""
        )

    def get_fecha(self) -> str:
        """Return the PAC server date/time."""

        response = self._call(
            "getFecha",
            "",
        )

        return response.decode("utf-8")

    def get_cfdi_test(self, xml: bytes) -> bytes:
        """Stamp a CFDI using the PAC test environment."""

        encoded_xml = encode_zip(xml)

        fields = "".join(
            [
                self._element("psUsuario", self.username),
                self._element("psPassword", self.password),
                self._element("pyXML", encoded_xml),
            ]
        )

        result = self._call(
            "getCFDiTest",
            fields,
        )

        return decode_zip(result)

    def get_timbre_cfdi_test(self, xml: bytes) -> bytes:
        """Return only the TFD using the PAC test environment."""

        encoded_xml = encode_zip(xml)

        fields = "".join(
            [
                self._element("psUsuario", self.username),
                self._element("psPassword", self.password),
                self._element("pyXML", encoded_xml),
            ]
        )

        result = self._call(
            "getTimbreCFDiTest",
            fields,
        )

        return decode_zip(result)

    def get_cfdi_v2_test(self, xml: bytes) -> bytes:
        """Stamp CFDI using the PAC CFDI v2 test method."""

        encoded_xml = encode_zip(xml)

        fields = "".join(
            [
                self._element("psUsuario", self.username),
                self._element("psPassword", self.password),
                self._element("pyXML", encoded_xml),
            ]
        )

        result = self._call(
            "getCFDIv2Test",
            fields,
        )

        return decode_zip(result)

    def get_timbre_cfdi_v2_test(self, xml: bytes) -> bytes:
        """Return TFD using the PAC CFDI v2 test method."""

        encoded_xml = encode_zip(xml)

        fields = "".join(
            [
                self._element("psUsuario", self.username),
                self._element("psPassword", self.password),
                self._element("pyXML", encoded_xml),
            ]
        )

        result = self._call(
            "getTimbreCFDIv2Test",
            fields,
        )

        return decode_zip(result)
