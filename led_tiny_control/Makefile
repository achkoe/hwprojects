TARGET=ledcontrol
MCU=attiny85
SOURCES=$(TARGET).c
OBJECTS=$(SOURCES:.c=.o) ws2812/ws2812_tinymega.o
CFLAGS=-c -Os -I ws2812
LDFLAGS=

PROGRAMMER=avrispmkII
PORT=-Pusb

#Ab hier nichts verändern

all: hex eeprom

hex: $(TARGET).hex

eeprom: $(TARGET)_eeprom.hex

$(TARGET).hex: $(TARGET).elf
	avr-objcopy -O ihex -j .data -j .text $(TARGET).elf $(TARGET).hex

$(TARGET)_eeprom.hex: $(TARGET).elf
	avr-objcopy -O ihex -j .eeprom --change-section-lma .eeprom=1 $(TARGET).elf $(TARGET)_eeprom.hex

$(TARGET).elf: $(OBJECTS)
	avr-gcc $(LDFLAGS) -mmcu=$(MCU) $(OBJECTS) -o $(TARGET).elf

.c.o:
	avr-gcc $(CFLAGS) -mmcu=$(MCU) $< -o $@

.s.o:
	avr-gcc -Wa,-gdwarf2 -x assembler-with-cpp -c -DF_CPU=8000000  -mmcu=$(MCU) -o $@ $<

size:
	avr-size --mcu=$(MCU) -C $(TARGET).elf

.PHONY: upload
upload:
	avrdude -b 115200 -V -p t167 $(PORT) -c$(PROGRAMMER) -Uflash:w:$(TARGET).hex:a

clean_tmp:
	rm -rf *.o
	rm -rf *.elf

clean:
	rm -rf *.o
	rm -rf *.elf
	rm -rf *.hex

