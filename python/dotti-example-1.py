#!/usr/bin/env python2.7

# Copyright (c) 2016 Martin F. Falatic

from __future__ import print_function

"""Bluetooth LE Python interface to the Witti Dotti device"""

import sys
import os
import time
import struct
import random
import bluepy.bluepy.btle as btle

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage:\n  %s <mac-address> [<address-type>]" % sys.argv[0])

    if not os.path.isfile(btle.helperExe):
        raise ImportError("Cannot find required executable '%s'" % btle.helperExe)

    device_mac = sys.argv[1]
    if len(sys.argv) == 3:
        address_type = sys.argv[2]
    else:
        address_type = btle.ADDR_TYPE_PUBLIC
    print("Connecting to: {}, address type: {}".format(device_mac, address_type))

    conn = btle.Peripheral(device_mac, address_type)
    newch = btle.Characteristic(conn, btle.UUID('fff3'), 0x29, 8, 0x2A)
    while 1:
        px = random.randrange(64)
        colR = random.randrange(256)
        colG = random.randrange(256)
        colB = random.randrange(256)
        newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px+1, colR, colG, colB))
        time.sleep(0.10)
        px = random.randrange(64)
        newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px+1, 0x00, 0x00, 0x00))
        time.sleep(0.1)
    conn.disconnect()
    exit()

    # try:
    # except BTLEException as e:

