from xml.dom import minidom
from Crypto.Util import number
from Crypto.Util.asn1 import DerSequence
from Crypto.PublicKey import RSA
from binascii import a2b_base64
import base64

def GetLong(nodelist):
  rc = []
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc.append(node.data)
  string = ''.join(rc)
  return number.bytes_to_long(base64.b64decode(string))

def pubkey_xml_to_pem(xmlkeydata):
    rsaKeyValue = minidom.parseString(xmlkeydata)
    modulus = GetLong(rsaKeyValue.getElementsByTagName('Modulus')[0].childNodes)
    exponent = GetLong(rsaKeyValue.getElementsByTagName('Exponent')[0].childNodes)
    publicKey = RSA.construct((modulus, exponent))
    return publicKey

def privkey_xml_to_pem(xmlkeydata):
    rsaKeyValue = minidom.parseString(xmlkeydata)
    modulus = GetLong(rsaKeyValue.getElementsByTagName('Modulus')[0].childNodes)
    exponent = GetLong(rsaKeyValue.getElementsByTagName('Exponent')[0].childNodes)
    d = GetLong(rsaKeyValue.getElementsByTagName('D')[0].childNodes)
    p = GetLong(rsaKeyValue.getElementsByTagName('P')[0].childNodes)
    q = GetLong(rsaKeyValue.getElementsByTagName('Q')[0].childNodes)
    qInv = GetLong(rsaKeyValue.getElementsByTagName('InverseQ')[0].childNodes)
    privateKey = RSA.construct((modulus, exponent, d, p, q, qInv))
    return privateKey

def pubkey_pem_to_xml(pubkeypem):
    publicKey = RSA.importKey(pubkeypem)
    xml = '<RSAKeyValue>'
    xml += '<Modulus>'
    xml += base64.standard_b64encode(number.long_to_bytes(publicKey.n))
    xml += '</Modulus>'
    xml += '<Exponent>'
    xml += base64.standard_b64encode(number.long_to_bytes(publicKey.e))
    xml += '</Exponent>'
    xml += '</RSAKeyValue>'
    return xml

def privkey_pem_to_xml(privkeypem):
    lines = privkeypem.replace(" ", '').split()
    keyDer = DerSequence()
    keyDer.decode(a2b_base64(''.join(lines[1:-1])))
    xml = '<RSAKeyValue>'
    xml += '<Modulus>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[1]))
    xml += '</Modulus>'
    xml += '<Exponent>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[2]))
    xml += '</Exponent>'
    xml += '<D>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[3]))
    xml += '</D>'
    xml += '<P>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[4]))
    xml += '</P>'
    xml += '<Q>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[5]))
    xml += '</Q>'
    xml += '<DP>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[6]))
    xml += '</DP>'
    xml += '<DQ>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[7]))
    xml += '</DQ>'
    xml += '<InverseQ>'
    xml += base64.standard_b64encode(number.long_to_bytes(keyDer[8]))
    xml += '</InverseQ>'
    xml += '</RSAKeyValue>'
    return xml