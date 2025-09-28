src=software
output=/home/achimk/work/hwprojects/teatimer/build

compile:
	arduino-cli compile -v --fqbn arduino:avr:nano --build-path ./build software
upload:
	arduino-cli  upload -v -p /dev/ttyUSB0 -b arduino:avr:nano:cpu=atmega328old --build-path ./build software 

rupload:
	scp $(output)/$(src).ino.hex pi@192.168.0.10:/home/pi/hex
	ssh pi@192.168.0.10 sudo avrdude -p atmega328p -c linuxgpio -U flash:w:hex/$(src).ino.hex:i

