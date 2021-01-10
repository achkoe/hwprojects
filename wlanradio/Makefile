all: compile upload

c compile:
	arduino-cli compile --fqbn arduino:avr:nano lcdarduino

u upload:
	# arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano simplecnccontrol
	arduino-cli upload -v -p /dev/ttyUSB0 -b arduino:avr:nano:cpu=atmega328old lcdarduino

.PHONY: compile c upload u
