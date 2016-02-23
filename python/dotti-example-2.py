#!/usr/bin/env python2.7

# Copyright (c) 2016 Martin F. Falatic

from __future__ import print_function

"""Bluetooth LE Python interface to the Witti Dotti device"""

import sys
import os
import time
import struct
import random
import timeit
import bluepy.bluepy.btle as btle

def demo0(hold_time, cycles):
    for n in range(cycles):
        for px_on in range(64):
            colR = colG = colB = 0
            newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px_on+1, colR, colG, colB))
            time.sleep(hold_time)

def demo1(hold_time, cycles):
    for n in range(cycles):
        for px_on in range(64):
            colR = random.randrange((px_on+1)*4)
            colG = random.randrange((px_on+1)*4)
            colB = random.randrange((px_on+1)*4)
            newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px_on+1, colR, colG, colB))
            time.sleep(hold_time)

def demo2(hold_time, cycles):
    for n in range(cycles*32):
        px_on = random.randrange(64)
        colR = random.randrange(256)
        colG = random.randrange(256)
        colB = random.randrange(256)
        newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px_on+1, colR, colG, colB))
        time.sleep(hold_time)
        px_off = px_on
        while px_off == px_on:
            px_off = random.randrange(64)
        newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px_off+1, 0x00, 0x00, 0x00))
        time.sleep(hold_time)

def demo3a(hold_time, cycles):
    for n in range(cycles):
        for px_on in range(64):
            colR = random.randrange(256)
            colG = random.randrange(256)
            colB = random.randrange(256)
            newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px_on+1, colR, colG, colB))
            time.sleep(hold_time)

def demo3b(hold_time, cycles):
    for n in range(cycles):
        colR = random.randrange(256)
        colG = random.randrange(256)
        colB = random.randrange(256)
        for px_on in range(64):
            newch.write(struct.pack('<BBBBBB', 0x07, 0x02, px_on+1, colR, colG, colB))
            time.sleep(hold_time)

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

    hold_time = 0.055 # Seems the max rate is about 0.055s/pixel (18 px/s)
    cycles = int(3.0)

    t_start_whole = time.time()

    demo0(hold_time=hold_time, cycles=1)

    t_start = time.time()
    demo1(hold_time=hold_time, cycles=cycles)
    t_delta = time.time()-t_start
    print("Elapsed = {}s @ {}s/pixel".format(t_delta, t_delta/(64.0*cycles)))

    t_start = time.time()
    demo2(hold_time=hold_time, cycles=cycles)
    t_delta = time.time()-t_start
    print("Elapsed = {}s @ {}s/pixel".format(t_delta, t_delta/(64.0*cycles)))

    t_start = time.time()
    demo3a(hold_time=hold_time, cycles=cycles)
    t_delta = time.time()-t_start
    print("Elapsed = {}s @ {}s/pixel".format(t_delta, t_delta/(64.0*cycles)))

    t_start = time.time()
    demo3b(hold_time=hold_time, cycles=cycles)
    t_delta = time.time()-t_start
    print("Elapsed = {}s @ {}s/pixel".format(t_delta, t_delta/(64.0*cycles)))

    demo0(hold_time=hold_time, cycles=1)

    try:
        input("Press enter to exit...")
    except SyntaxError:
        pass

    t_delta = time.time()-t_start_whole
    print("Elapsed = {}s".format(t_delta))
    conn.disconnect()
    exit()

    # try:
    # except BTLEException as e:

