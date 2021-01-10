# WLAN Radio using Raspberry Pi, and Arduino

Install mpc and pyserial.
Add startup.sh to crontab using @reboot.


# This and that
## Finding RPi

ping raspberrypi.local


## How to find which OS is on RPi?

cat /etc/os-release
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
NAME="Raspbian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"


## How to install Edimax Wlan Stick on RPi?

See
https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md


## How to install USB audio device on RPi?

See http://raspberry.tips/raspberrypi-tutorials/raspberry-pi-usb-soundkarte-unter-raspbian-einrichten

1. Identify your sound card:
    lsusb
    Bus 001 Device 005: ID 7392:7811 Edimax Technology Co., Ltd EW-7811Un 802.11n Wireless Adapter [Realtek RTL8188CUS]
    Bus 001 Device 004: ID 0d8c:000e C-Media Electronics, Inc. Audio Adapter (Planet UP-100, Genius G-Talk)
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. SMSC9512/9514 Fast Ethernet Adapter
    Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp. SMC9514 Hub
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub

    Here it is device 004.

2. Identify your sound card again
    aplay -l
    **** List of PLAYBACK Hardware Devices ****
    card 0: Headphones [bcm2835 Headphones], device 0: bcm2835 Headphones [bcm2835 Headphones]
      Subdevices: 8/8
      Subdevice #0: subdevice #0
      Subdevice #1: subdevice #1
      Subdevice #2: subdevice #2
      Subdevice #3: subdevice #3
      Subdevice #4: subdevice #4
      Subdevice #5: subdevice #5
      Subdevice #6: subdevice #6
      Subdevice #7: subdevice #7
    card 1: Device [Generic USB Audio Device], device 0: USB Audio [USB Audio]
      Subdevices: 0/1
      Subdevice #0: subdevice #0

3. Edit /etc/asound.conf
    sudo nano /etc/asound.conf

    pcm.!default {
        type hw
        card 1
    }

    ctl.!default {
        type hw
        card 1
    }

    sudo reboot

