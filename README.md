# Driving the Witti Dotti device via Bluetooth LE

## Disclaimer:
**I am not liable for any damage this may cause to your Dotti** - No changes are made to the Dotti's firmware, and my experience has been that any transient problems are easily rectified by powering down the Dotti for a few minutes (as well as resetting or rebooting the Linux device that's trying to communicate with the Dotti). The official (and unoffical) apps seem to continue to work just fine regardless of all that, once you power cycle the Dotti.

**I am not affiliated with Witti** - I bought this (on sale!) because I figured since there's already an opensource Android app out there for it (https://github.com/akinaru/dotti-bluetooth-android) that it just might be possible to make this work with the RPi2 - my bet paid off!

## Video of the first example in action!

<a href="http://www.youtube.com/watch?feature=player_embedded&v=dHzONPPgIac" target="_blank"><img src="http://img.youtube.com/vi/dHzONPPgIac/0.jpg" alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>

## Raspberry Pi + Python Interfacing
The Python part of this project leverages the bluepy project to interface to the Witti Dotti device from a Linux device (e.g., the Raspberry Pi 2)

### Configuration:
 - Witti Dotti (http://wittidesign.com/en/dotti/)
 - Raspberry Pi 2 running Raspbian Wheezy (with the latest updates)
 - Plugable USB Bluetooth 4.0 Low Energy Micro Adapter (model USB-BT4LE)
 - bluez (5.23-2+b1), blueman (1.99~alpha1-1+deb8u1), bluetooth (5.23-2) from Raspbian Wheezy repos
 - bluepy (https://github.com/IanHarvey/bluepy) (I used commit 04bcf93 which leverages bluez 5.29)
     - Interfaces with bluez via IPC using a helper executable

### Usage:
 - Install the Bluetooth stack as above
 - Clone this repo
 - Enter the `python` directory
 - Clone bluepy and build it per its instructions (you can clone, build and keep bluepy wherever you prefer but you may need to modify the path to the btle module accordingly in the examples)
 - Make sure the Bluetooth daemon is running and that you can connect to your Bluetooth controller
 - Use `bluetoothctl` to find your device's MAC address (important!)
 - Run an example, e.g. `dotti-example-1.py 5C:31:3E:00:00:01` **<-- replace with your Dotti's actual MAC address**
 - If all goes well, and your Bluetooth stack is running (and your adapter works with Bluetooth LE!) this should work
 - If it doesn't, ping me... I'm still learning how to communicate with this thing.

### Notes
 - Writing to the Dotti is slow, and I'm bypassing the callbacks to speed it up - this works to a point, but refresh rates are really low (if you go much faster then you end up having to reboot your RPi as well as the Dotti to get it back to connecting)
 - The Dotti is a neat device - and neater still when it's on sale!


