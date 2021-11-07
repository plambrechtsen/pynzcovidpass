"""
  Quick and dirty test for NZ COVID Pass
  Using the python-cwt module: https://github.com/dajiaji/python-cwt

  Ministry of Health docs
  Spec: https://nzcp.covid19.health.nz/
  Github: https://github.com/minhealthnz/nzcovidpass-spec
  Prod Key: https://nzcp.identity.health.nz/.well-known/did.json
  
"""

import datetime
import json
import base64
import cwt
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

try:
    # Production Key - https://nzcp.identity.health.nz/.well-known/did.json
    # nzkey = COSEKey.from_jwk({
    #             "kty": "EC",
    #             "kid": "key-1",
    #             "crv": "P-256",
    #             "x": "DQCKJusqMsT0u7CjpmhjVGkHln3A3fS-ayeH4Nu52tc",
    #             "y": "lxgWzsLtVI8fqZmTPPo9nZ-kzGs7w7XO8-rUU68OxmI"
    #         })

    # Test key from https://nzcp.covid19.health.nz/#trusted-issuers
    nzkey = cwt.COSEKey.from_jwk({
        "kty": "EC",
        "kid": "key-1",
        "crv": "P-256",
        "x": "zRR-XGsCp12Vvbgui4DD6O6cqmhfPuXMhi1OxPl8760",
        "y": "Iv5SU6FuW-TRYh5_GOrJlcV_gpF_GpFQhCOD8LSk3T0"
    })
    QR = "NZCP:/1/2KCEVIQEIVVWK6JNGEASNICZAEP2KALYDZSGSZB2O5SWEOTOPJRXALTDN53GSZBRHEXGQZLBNR2GQLTOPICRUYMBTIFAIGTUKBAAUYTWMOSGQQDDN5XHIZLYOSBHQJTIOR2HA4Z2F4XXO53XFZ3TGLTPOJTS6MRQGE4C6Y3SMVSGK3TUNFQWY4ZPOYYXQKTIOR2HA4Z2F4XW46TDOAXGG33WNFSDCOJONBSWC3DUNAXG46RPMNXW45DFPB2HGL3WGFTXMZLSONUW63TFGEXDALRQMR2HS4DFQJ2FMZLSNFTGSYLCNRSUG4TFMRSW45DJMFWG6UDVMJWGSY2DN53GSZCQMFZXG4LDOJSWIZLOORUWC3CTOVRGUZLDOSRWSZ3JOZSW4TTBNVSWISTBMNVWUZTBNVUWY6KOMFWWKZ2TOBQXE4TPO5RWI33CNIYTSNRQFUYDILJRGYDVAYFE6VGU4MCDGK7DHLLYWHVPUS2YIDJOA6Y524TD3AZRM263WTY2BE4DPKIF27WKF3UDNNVSVWRDYIYVJ65IRJJJ6Z25M2DO4YZLBHWFQGVQR5ZLIWEQJOZTS3IQ7JTNCFDX"
    B32VAL = base64.b32decode(QR.split('/')[2])
    # Add Base32 padding back on if needed: https://nzcp.covid19.health.nz/#2d-barcode-encoding
    unpadded_length = len(B32VAL) % 8
    if unpadded_length != 0:
        B32VAL += (8 - unpadded_length) * '='

    decoded = cwt.decode(B32VAL, nzkey)
    print('Raw Response')
    print(decoded)
    print('Decoded Response')
    print('Issued ' + datetime.datetime.utcfromtimestamp(decoded[5]).strftime('%Y-%m-%d %H:%M:%S'))
    print('Expires ' + datetime.datetime.utcfromtimestamp(decoded[4]).strftime('%Y-%m-%d %H:%M:%S'))
    json_str = json.dumps(decoded['vc'], indent=4)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))

except Exception as err:
    print(err)
