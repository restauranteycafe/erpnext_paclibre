"""Exceptions for the Certifica CFDI PAC."""


class CertificaCFDIError(Exception):
    """Base exception for Certifica CFDI errors."""


class CertificaCFDISoapError(CertificaCFDIError):
    """SOAP communication error."""


class CertificaCFDIResponseError(CertificaCFDIError):
    """PAC returned an application-level error."""


class CertificaCFDIInvalidResponse(CertificaCFDIError):
    """PAC returned an unexpected response."""
