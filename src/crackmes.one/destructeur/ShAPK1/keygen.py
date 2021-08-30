#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import base64

BEGINNING = "beginning"
SERIAL = "NQALCgEDDDEzUjpTBwocBgcDPTIIGwIK"

serial_b64decoded = base64.b64decode(SERIAL)
serial_b64decoded_length = len(serial_b64decoded)

beginning_length = len(BEGINNING)
original_serial = ""

for i in range(serial_b64decoded_length):
    xored_value = (serial_b64decoded[i] ^ 
        ord(BEGINNING[i % beginning_length]))
    original_serial += chr(xored_value)

# the original code 
print(original_serial)
