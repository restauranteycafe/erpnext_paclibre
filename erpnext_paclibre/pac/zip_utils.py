"""ZIP/base64 helpers used by the Certifica CFDI PAC."""

import base64
import io
import zipfile


class ZipResponseError(Exception):
    """Raised when the PAC ZIP response cannot be decoded."""


def zip_xml(xml: bytes, filename: str = "cfdi.xml") -> bytes:
    """Pack XML into a ZIP archive."""

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(filename, xml)

    return buffer.getvalue()


def unzip_xml(data: bytes) -> bytes:
    """Extract the first XML file from a ZIP archive."""

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            xml_files = [
                name
                for name in archive.namelist()
                if name.lower().endswith(".xml")
            ]

            if not xml_files:
                raise ZipResponseError("PAC response ZIP contains no XML file.")

            return archive.read(xml_files[0])

    except zipfile.BadZipFile as exc:
        raise ZipResponseError("PAC response is not a valid ZIP archive.") from exc


def encode_zip(xml: bytes) -> str:
    """ZIP XML and encode it as base64 for SOAP."""

    return base64.b64encode(zip_xml(xml)).decode("ascii")


def decode_zip(value: bytes | str) -> bytes:
    """Decode a base64 ZIP returned by the PAC and extract its XML."""

    if isinstance(value, str):
        value = value.encode("ascii")

    try:
        zipped = base64.b64decode(value)
    except Exception as exc:
        raise ZipResponseError("PAC response is not valid base64.") from exc

    return unzip_xml(zipped)
