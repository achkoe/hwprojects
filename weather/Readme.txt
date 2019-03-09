
Arduino Pin | LCD Pin | LCD Function
GND           1         VSS (selten: VDD)   GND (selten: +5 V)
5V            2         VDD (selten: VSS)   +5 V (selten: GND)
GND           3         VEE, V0, V5 Kontrastspannung (-5 V / 0 V bis 5 V)
11            4         RS  Register Select (0=Befehl/Status 1=Daten)
GND           5         RW  1=Read 0=Write
10            6         E   0=Disable 1=Enable
              7         DB0 Datenbit 0
              8         DB1 Datenbit 1
              9         DB2 Datenbit 2
              10        DB3 Datenbit 3
9             11        DB4 Datenbit 4
8             12        DB5 Datenbit 5
7             13        DB6 Datenbit 6
6             14        DB7 Datenbit 7
              15        A         LED-Beleuchtung, meist Anode
              16        K         LED-Beleuchtung, meist Kathode

LiquidCrystal(rs, enable, d4, d5, d6, d7)
LiquidCrystal(8, 7, 3, 4, 5, 6)


LCD/1 - Arduino/GND
LCD/2 - Arduino/5V
LCD/3 - Arduino/GND
LCD/4 - Arduino/D8 (RS)
LCD/5 - Arduino/GND
LCD/6 - Arduino/D7 (E)
LCD/11 - Arduino/D3 (DB4)
LCD/12 - Arduino/D4 (DB5)
LCD/13 - Arduino/D5 (DB6)
LCD/14 - Arduino/D6 (DB7)
LCD/15 - Arduino/GND
LCD/16 - Collector

Arduino/A4 - BME280/SDA
Arduino/A5 - BME280/SCL

Arduino/D9  - R10k/1
R10k/2 - Basis
Emitter - GND

Arduino/D10 - Pushbutton/1
Pushbutton/2 - GND
