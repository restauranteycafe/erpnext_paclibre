# --- Preparando factura ---
import frappe
from lxml import etree

invoice = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00004")
csd = frappe.get_doc("Digital Signing Certificate", "RODRIGO KITIA CASTRO-01")

voucher = invoice.get_cfdi_voucher(csd)
#print(voucher)

# --- Preparando Cliente ---
from erpnext_paclibre.pac import CertificaCFDIClient

client = CertificaCFDIClient(
    username="",
    password=""
)

# --- Probando API ---
#client.get_fecha()

# --- Generando y Sellando XML ---
voucher.sign(csd.signer)
cfdi = voucher.process(True)

xml = etree.tostring(
    cfdi.to_xml(),
    xml_declaration=True,
    encoding="UTF-8",
)
# --- Guardando XML ---
'''
with open(
    "/home/frappe/frappe-bench/apps/erpnext_paclibre/tests/test_cfdi.xml",
    "wb",
) as f:
    f.write(xml)
'''

# --- Abriendo XML ---
'''
with open(
    "/home/frappe/frappe-bench/apps/erpnext_paclibre/tests/test_cfdi.xml",
    "rb",
) as f:
    xml = f.read()
'''

# --- Probando Timbrando ---
client.get_cfdi_test(xml)
