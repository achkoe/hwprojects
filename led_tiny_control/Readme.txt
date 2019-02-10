Programmers connection
======================

Programmers     ATTiny85
Pin             Pin

1               5, MOSI
5               1, RESET
7               7, SCK
9               6, MISO
2               8, VDD
10              4, VSS



Old stuff, not valid for this
=============================

sudo avrdude -p t167 -c linuxgpio -U flash:r:content.hex:h -U lfuse:r:lfuse.hex:h
sudo avrdude -p m32 -c linuxgpio -U flash:r:content.hex:h -U lfuse:r:lfuse.hex:h
avrdude -p m328p -c avrispmkII -P usb -U flash:w:irdecode.hex -U lfuse:w:0xE4:m

avrdude -p m32 -c avrispmkII -P usb -U flash:w:irdecode.hex -U lfuse:w:0xE4:m

avrdude -p m32 -c avrispmkII -P usb -U flash:r:content.hex:h -U lfuse:r:lfuse.hex:h

avrdude -p t85 -c avrispmkII -P usb -U flash:w:dice.hex

avrdude -p t13 -c avrispmkII -P usb -U flash:w:dice.hex  -U lfuse:w:0x6B:m


==================================================================================
0x62 = 0110 0010 = 0b0110 0010
0xE2 = 1110 0010
==================================================================================
What happens when LFUSE is accidenty programmed?

unprogrammed Fuses OK (H:07, E:D9, L:62) LFUSE=0b 0110 0010
programmed   Fuses OK (H:07, E:D9, L:E4) LFUSE=0b 1110 0100

Thus CKDIV8 has changed from "off" to "on"
CKSEL has changed from "internal RC Oscillator @ 8MHz" to "Low Frequency Crystal Oscillator with Ceramic resonator" 32.768kHz Crystal
