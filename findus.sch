EESchema Schematic File Version 4
LIBS:roboter-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "FINDUS Liquid Handling Station"
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Regulator_Linear:AMS1117-3.3 U2
U 1 1 5CD3F77A
P 7350 3900
F 0 "U2" V 7700 3800 50  0001 L CNN
F 1 "AMS1117-3.3" V 6950 3450 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-223-3_TabPin2" H 7350 4100 50  0001 C CNN
F 3 "http://www.advanced-monolithic.com/pdf/ds1117.pdf" H 7450 3650 50  0001 C CNN
	1    7350 3900
	0    1    1    0   
$EndComp
$Comp
L Driver_Motor:Pololu_Breakout_DRV8825 A2
U 1 1 5CD41576
P 2900 2700
F 0 "A2" V 3000 2600 50  0000 L CNN
F 1 "DRV8825 z-Axis" V 2900 2300 50  0000 L CNN
F 2 "Module:Pololu_Breakout-16_15.2x20.3mm" H 3100 1900 50  0001 L CNN
F 3 "https://www.pololu.com/product/2982" H 3000 2400 50  0001 C CNN
	1    2900 2700
	0    1    1    0   
$EndComp
$Comp
L Connector:Screw_Terminal_01x02 J1
U 1 1 5CD469F5
P 900 3950
F 0 "J1" H 818 3625 50  0001 C CNN
F 1 "Screw_Terminal_01x02" H 1000 3550 50  0001 C CNN
F 2 "TerminalBlock_MetzConnect:TerminalBlock_MetzConnect_Type011_RT05502HBWC_1x02_P5.00mm_Horizontal" H 900 3950 50  0001 C CNN
F 3 "~" H 900 3950 50  0001 C CNN
	1    900  3950
	-1   0    0    1   
$EndComp
$Comp
L Device:CP1 C1
U 1 1 5CD4ABF7
P 1650 3900
F 0 "C1" H 1765 3946 50  0001 L CNN
F 1 "100µF" H 1500 4150 50  0000 L CNN
F 2 "Capacitor_Tantalum_SMD:CP_EIA-7343-20_Kemet-V" H 1650 3900 50  0001 C CNN
F 3 "~" H 1650 3900 50  0001 C CNN
	1    1650 3900
	1    0    0    -1  
$EndComp
$Comp
L Device:C C2
U 1 1 5CD4B60B
P 6800 4150
F 0 "C2" H 6915 4196 50  0001 L CNN
F 1 "100pF" H 6500 4050 50  0000 L CNN
F 2 "Capacitor_THT:C_Disc_D4.3mm_W1.9mm_P5.00mm" H 6838 4000 50  0001 C CNN
F 3 "~" H 6800 4150 50  0001 C CNN
	1    6800 4150
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5CD4BE6E
P 9950 4450
F 0 "R2" H 10020 4496 50  0001 L CNN
F 1 "R10K" V 10050 4350 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 9880 4450 50  0001 C CNN
F 3 "~" H 9950 4450 50  0001 C CNN
	1    9950 4450
	1    0    0    -1  
$EndComp
$Comp
L roboter-rescue:MP1584ENBB-mp1584EN U1
U 1 1 5CD45B96
P 5900 4150
F 0 "U1" H 6200 4747 60  0001 C CNN
F 1 "DC/DC 18/5V" H 6150 4650 60  0000 C CNN
F 2 "buck conv:MP1584_buck_module" H 5900 4150 60  0001 C CNN
F 3 "" H 5900 4150 60  0001 C CNN
	1    5900 4150
	1    0    0    -1  
$EndComp
$Comp
L Driver_Motor:Pololu_Breakout_DRV8825 A4
U 1 1 5CD683AD
P 4800 2700
F 0 "A4" V 4900 2550 50  0000 L CNN
F 1 "DRV8825 y-Axis" V 4800 2300 50  0000 L CNN
F 2 "Module:Pololu_Breakout-16_15.2x20.3mm" H 5000 1900 50  0001 L CNN
F 3 "https://www.pololu.com/product/2982" H 4900 2400 50  0001 C CNN
	1    4800 2700
	0    1    1    0   
$EndComp
$Comp
L Driver_Motor:Pololu_Breakout_DRV8825 A1
U 1 1 5CD68E91
P 2700 5050
F 0 "A1" V 2600 5100 50  0000 L CNN
F 1 "DRV8825   Pipette" V 2700 4600 50  0000 L CNN
F 2 "Module:Pololu_Breakout-16_15.2x20.3mm" H 2900 4250 50  0001 L CNN
F 3 "https://www.pololu.com/product/2982" H 2800 4750 50  0001 C CNN
	1    2700 5050
	0    -1   -1   0   
$EndComp
$Comp
L Driver_Motor:Pololu_Breakout_DRV8825 A3
U 1 1 5CD741DE
P 4600 5050
F 0 "A3" V 4500 4750 50  0000 L CNN
F 1 "DRV8825 x-Axis" V 4600 4650 50  0000 L CNN
F 2 "Module:Pololu_Breakout-16_15.2x20.3mm" H 4800 4250 50  0001 L CNN
F 3 "https://www.pololu.com/product/2982" H 4700 4750 50  0001 C CNN
	1    4600 5050
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x04_Male J2
U 1 1 5CD7D07E
P 2750 3450
F 0 "J2" V 2858 3594 50  0001 L CNN
F 1 "Conn_01x04_Male" V 2903 3594 50  0001 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 2750 3450 50  0001 C CNN
F 3 "~" H 2750 3450 50  0001 C CNN
	1    2750 3450
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x04_Male J4
U 1 1 5CD80276
P 4650 3450
F 0 "J4" V 4758 3594 50  0001 L CNN
F 1 "Conn_01x04_Male" V 4803 3594 50  0001 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 4650 3450 50  0001 C CNN
F 3 "~" H 4650 3450 50  0001 C CNN
	1    4650 3450
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x04_Male J3
U 1 1 5CD80FFA
P 2850 4250
F 0 "J3" V 2958 4394 50  0001 L CNN
F 1 "Conn_01x04_Male" V 3003 4394 50  0001 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 2850 4250 50  0001 C CNN
F 3 "~" H 2850 4250 50  0001 C CNN
	1    2850 4250
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x04_Male J5
U 1 1 5CD837BF
P 4750 4250
F 0 "J5" V 4858 4394 50  0001 L CNN
F 1 "Conn_01x04_Male" V 4903 4394 50  0001 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 4750 4250 50  0001 C CNN
F 3 "~" H 4750 4250 50  0001 C CNN
	1    4750 4250
	0    1    1    0   
$EndComp
$Comp
L Connector:Conn_01x06_Female FTDI1
U 1 1 5CD8555F
P 10050 1600
F 0 "FTDI1" V 9942 1212 50  0000 R CNN
F 1 "Conn_01x06_Female" V 9987 1848 50  0001 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x06_P2.54mm_Vertical" H 10050 1600 50  0001 C CNN
F 3 "~" H 10050 1600 50  0001 C CNN
	1    10050 1600
	0    -1   -1   0   
$EndComp
$Comp
L Switch:SW_Push SW1
U 1 1 5CD876A7
P 7600 4600
F 0 "SW1" H 7600 4885 50  0001 C CNN
F 1 "Reset" V 7600 4552 50  0000 R CNN
F 2 "Button_Switch_SMD:SW_Push_1P1T_NO_6x6mm_H9.5mm" H 7600 4800 50  0001 C CNN
F 3 "~" H 7600 4800 50  0001 C CNN
	1    7600 4600
	0    -1   -1   0   
$EndComp
$Comp
L Switch:SW_Push SW2
U 1 1 5CD87F39
P 10450 4600
F 0 "SW2" H 10450 4885 50  0001 C CNN
F 1 "Flash" V 10450 4552 50  0000 R CNN
F 2 "Button_Switch_SMD:SW_Push_1P1T_NO_6x6mm_H9.5mm" H 10450 4800 50  0001 C CNN
F 3 "~" H 10450 4800 50  0001 C CNN
	1    10450 4600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1100 3850 1100 3750
Wire Wire Line
	1100 3750 1650 3750
Wire Wire Line
	1100 3950 1100 4050
Wire Wire Line
	1100 4050 1650 4050
Wire Wire Line
	1900 3800 1900 3750
Wire Wire Line
	1900 3750 1650 3750
Connection ~ 1650 3750
Wire Wire Line
	5600 4000 5400 4000
Wire Wire Line
	1900 4000 1900 4050
Wire Wire Line
	1900 4050 1650 4050
Connection ~ 1650 4050
Wire Wire Line
	3500 2700 3500 3800
Wire Wire Line
	1900 3800 2100 3800
Connection ~ 3500 3800
Wire Wire Line
	3500 3800 4000 3800
Wire Wire Line
	5400 2700 5400 3800
Connection ~ 5400 3800
Wire Wire Line
	5400 3800 5600 3800
Wire Wire Line
	4000 5050 4000 3800
Connection ~ 4000 3800
Wire Wire Line
	4000 3800 5400 3800
Wire Wire Line
	2100 5050 2100 3800
Connection ~ 2100 3800
Wire Wire Line
	2100 3800 3500 3800
Wire Wire Line
	2600 3100 2600 3250
Wire Wire Line
	2600 3250 2650 3250
Wire Wire Line
	2700 3100 2700 3250
Wire Wire Line
	2700 3250 2750 3250
Wire Wire Line
	4500 3100 4500 3250
Wire Wire Line
	4500 3250 4550 3250
Wire Wire Line
	4600 3100 4600 3250
Wire Wire Line
	4600 3250 4650 3250
Wire Wire Line
	2900 4650 2900 4450
Wire Wire Line
	2900 4450 2850 4450
Wire Wire Line
	3000 4650 3000 4450
Wire Wire Line
	3000 4450 2950 4450
Wire Wire Line
	4800 4650 4800 4450
Wire Wire Line
	4800 4450 4750 4450
Wire Wire Line
	4900 4650 4900 4450
Wire Wire Line
	4900 4450 4850 4450
Wire Wire Line
	3500 4950 3500 4000
Connection ~ 3500 4000
Wire Wire Line
	5400 4950 5400 4000
Connection ~ 5400 4000
Wire Wire Line
	7050 3900 7050 4000
Wire Wire Line
	7050 4000 6800 4000
Connection ~ 6800 4000
Wire Wire Line
	7350 4300 7350 4200
Wire Wire Line
	6800 3800 6800 3600
Wire Wire Line
	6800 3600 7350 3600
Wire Wire Line
	7500 3000 7500 3800
Wire Wire Line
	7500 4300 7350 4300
Connection ~ 7350 4300
$Comp
L roboter-rescue:ESP-12-ESP8266 U3
U 1 1 5CDA3A88
P 9050 3900
F 0 "U3" H 9050 4981 50  0000 C CNN
F 1 "ESP-12" H 9050 4890 50  0000 C CNN
F 2 "esp8266:ESP-12E_SMD" H 9050 3900 50  0001 C CNN
F 3 "http://l0l.org.uk/2014/12/esp8266-modules-hardware-guide-gotta-catch-em-all/" H 9050 3900 50  0001 C CNN
	1    9050 3900
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5CDB63EA
P 8150 3300
F 0 "R1" H 8220 3346 50  0001 L CNN
F 1 "R10K" H 8220 3300 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 8080 3300 50  0001 C CNN
F 3 "~" H 8150 3300 50  0001 C CNN
	1    8150 3300
	1    0    0    -1  
$EndComp
$Comp
L Device:R R3
U 1 1 5CDB68B4
P 10450 3850
F 0 "R3" H 10520 3896 50  0001 L CNN
F 1 "R10K" V 10550 3750 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 10380 3850 50  0001 C CNN
F 3 "~" H 10450 3850 50  0001 C CNN
	1    10450 3850
	1    0    0    -1  
$EndComp
$Comp
L Device:R R4
U 1 1 5CDB7844
P 10700 3950
F 0 "R4" H 10770 3996 50  0001 L CNN
F 1 "R10K" V 10800 3900 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 10630 3950 50  0001 C CNN
F 3 "~" H 10700 3950 50  0001 C CNN
	1    10700 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	7500 3000 8150 3000
Wire Wire Line
	8150 3600 8150 3450
Wire Wire Line
	8150 3150 8150 3000
Connection ~ 8150 3000
Wire Wire Line
	8150 3000 9050 3000
Wire Wire Line
	8150 3800 7500 3800
Connection ~ 7500 3800
Wire Wire Line
	7500 3800 7500 4300
Wire Wire Line
	8150 3600 7600 3600
Wire Wire Line
	7600 3600 7600 4400
Connection ~ 8150 3600
Wire Wire Line
	10450 4000 10450 4400
Wire Wire Line
	7050 4000 7050 4800
Wire Wire Line
	7050 4800 7600 4800
Connection ~ 7050 4000
Wire Wire Line
	7600 4800 9050 4800
Connection ~ 7600 4800
Wire Wire Line
	9050 4800 9950 4800
Connection ~ 9050 4800
Wire Wire Line
	9050 3000 10450 3000
Wire Wire Line
	10450 3000 10450 3700
Connection ~ 9050 3000
Wire Wire Line
	9950 4100 10700 4100
Wire Wire Line
	9950 4000 10450 4000
Connection ~ 10450 4000
Wire Wire Line
	10450 3000 10700 3000
Wire Wire Line
	10700 3000 10700 3800
Connection ~ 10450 3000
Wire Wire Line
	9950 3700 10050 3700
Wire Wire Line
	9950 4600 9950 4800
Connection ~ 9950 4800
Wire Wire Line
	9950 4800 10450 4800
Wire Wire Line
	6800 2150 5100 2150
Wire Wire Line
	5100 2150 5100 2300
Wire Wire Line
	5100 2150 5000 2150
Wire Wire Line
	5000 2150 5000 2300
Connection ~ 5100 2150
Wire Wire Line
	3200 2150 3200 2300
Connection ~ 5000 2150
Wire Wire Line
	3200 2150 3100 2150
Wire Wire Line
	3100 2150 3100 2300
Connection ~ 3200 2150
Wire Wire Line
	4300 5450 4300 5600
Wire Wire Line
	4300 5600 4400 5600
Wire Wire Line
	4400 5600 4400 5450
Connection ~ 4300 5600
Wire Wire Line
	2500 5450 2500 5600
Wire Wire Line
	2500 5600 2400 5600
Wire Wire Line
	2400 5600 2400 5450
Connection ~ 2500 5600
Wire Wire Line
	10700 4100 10700 5700
Wire Wire Line
	5200 5700 5200 5450
Connection ~ 10700 4100
Wire Wire Line
	5200 5700 5100 5700
Wire Wire Line
	5100 5700 5100 5450
Connection ~ 5200 5700
Wire Wire Line
	5100 5700 5000 5700
Wire Wire Line
	5000 5700 5000 5450
Connection ~ 5100 5700
Wire Wire Line
	5000 5700 3700 5700
Wire Wire Line
	3300 5700 3300 5450
Connection ~ 5000 5700
Wire Wire Line
	3300 5700 3200 5700
Wire Wire Line
	3200 5700 3200 5450
Connection ~ 3300 5700
Wire Wire Line
	3200 5700 3100 5700
Wire Wire Line
	3100 5700 3100 5450
Connection ~ 3200 5700
Wire Wire Line
	2300 2300 2300 2000
Wire Wire Line
	2300 2000 2400 2000
Wire Wire Line
	4200 2000 4200 2300
Wire Wire Line
	4200 2000 4300 2000
Wire Wire Line
	4300 2000 4300 2300
Connection ~ 4200 2000
Wire Wire Line
	4300 2000 4400 2000
Wire Wire Line
	4400 2000 4400 2300
Connection ~ 4300 2000
Wire Wire Line
	2400 2300 2400 2000
Connection ~ 2400 2000
Wire Wire Line
	2400 2000 2500 2000
Wire Wire Line
	2500 2300 2500 2000
Connection ~ 2500 2000
Wire Wire Line
	2500 2000 3700 2000
Wire Wire Line
	3500 4000 3900 4000
Wire Wire Line
	9950 4200 9950 4300
Wire Wire Line
	3700 2000 3700 5700
Connection ~ 3700 2000
Wire Wire Line
	3700 2000 4200 2000
Connection ~ 3700 5700
Wire Wire Line
	2900 2300 2900 1900
Wire Wire Line
	2900 1900 3800 1900
Wire Wire Line
	4800 1900 4800 2300
Wire Wire Line
	10700 5700 5200 5700
Wire Wire Line
	9950 4200 10200 4200
Wire Wire Line
	10200 4200 10200 5800
Wire Wire Line
	10200 5800 4600 5800
Wire Wire Line
	4600 5800 4600 5450
Connection ~ 9950 4200
Wire Wire Line
	4600 5800 3800 5800
Wire Wire Line
	2700 5800 2700 5450
Connection ~ 4600 5800
Wire Wire Line
	3800 5800 3800 1900
Connection ~ 3800 5800
Wire Wire Line
	3800 5800 2700 5800
Connection ~ 3800 1900
Wire Wire Line
	3800 1900 4800 1900
Wire Wire Line
	4600 2000 4600 2300
Wire Wire Line
	4700 2300 4700 2100
Wire Wire Line
	9950 3900 10250 3900
Wire Wire Line
	10250 3900 10250 5900
Wire Wire Line
	10250 5900 4800 5900
Wire Wire Line
	4800 5900 4800 5450
Wire Wire Line
	7050 3900 7050 2300
Wire Wire Line
	7050 2300 10350 2300
Wire Wire Line
	10350 2300 10350 1800
Connection ~ 7050 3900
Wire Wire Line
	7050 4800 7050 5050
Connection ~ 7050 4800
Wire Wire Line
	4000 2800 3900 2800
Wire Wire Line
	3900 2800 3900 4000
Connection ~ 3900 4000
Wire Wire Line
	3900 4000 5400 4000
Wire Wire Line
	5600 4200 3900 4200
Wire Wire Line
	3900 4200 3900 5050
Wire Wire Line
	3900 5050 3500 5050
Wire Wire Line
	1900 4000 1950 4000
Wire Wire Line
	2100 2800 1950 2800
Wire Wire Line
	1950 2800 1950 4000
Connection ~ 1950 4000
Wire Wire Line
	1950 4000 3500 4000
Wire Wire Line
	5600 3550 4000 3550
Wire Wire Line
	4000 3550 2100 3550
Connection ~ 4000 3550
Wire Wire Line
	9950 3800 10300 3800
Wire Wire Line
	10300 3800 10300 6000
Wire Wire Line
	10300 6000 4700 6000
Wire Wire Line
	4700 6000 4700 5450
Wire Wire Line
	8000 6100 2900 6100
Wire Wire Line
	2900 6100 2900 5450
Wire Wire Line
	8150 6200 2800 6200
Wire Wire Line
	2800 6200 2800 5450
Wire Wire Line
	8150 4000 7750 4000
Wire Wire Line
	7750 4000 7750 1650
Wire Wire Line
	7750 1650 2700 1650
Wire Wire Line
	2700 1650 2700 2300
Wire Wire Line
	8150 3900 7900 3900
Wire Wire Line
	7900 3900 7900 1800
Wire Wire Line
	7900 1800 2800 1800
Wire Wire Line
	2800 1800 2800 2300
Wire Wire Line
	5600 4200 5600 5050
Wire Wire Line
	5400 5050 5600 5050
Connection ~ 5600 5050
Wire Wire Line
	5600 5050 7050 5050
Connection ~ 5600 4200
Wire Wire Line
	5600 3550 5600 4200
Wire Wire Line
	2950 3250 2900 3250
Wire Wire Line
	2900 3250 2900 3100
Wire Wire Line
	2850 3250 2850 3150
Wire Wire Line
	2850 3150 3000 3150
Wire Wire Line
	3000 3150 3000 3100
Wire Wire Line
	4850 3250 4800 3250
Wire Wire Line
	4800 3250 4800 3100
Wire Wire Line
	4750 3250 4750 3150
Wire Wire Line
	4750 3150 4900 3150
Wire Wire Line
	4900 3150 4900 3100
Wire Wire Line
	2650 4450 2650 4650
Wire Wire Line
	2650 4650 2700 4650
Wire Wire Line
	2750 4450 2750 4550
Wire Wire Line
	2750 4550 2600 4550
Wire Wire Line
	2600 4550 2600 4650
Wire Wire Line
	4550 4450 4550 4650
Wire Wire Line
	4550 4650 4600 4650
Wire Wire Line
	4650 4450 4650 4550
Wire Wire Line
	4650 4550 4500 4550
Wire Wire Line
	4500 4550 4500 4650
Wire Wire Line
	2100 2700 2100 3550
Wire Wire Line
	4000 2700 4000 3550
Wire Wire Line
	6800 4300 7350 4300
Wire Wire Line
	6800 2150 6800 3600
Connection ~ 6800 3600
Wire Wire Line
	3200 2150 3600 2150
Wire Wire Line
	3700 5700 3300 5700
Wire Wire Line
	3600 2150 3600 5600
Wire Wire Line
	2500 5600 3600 5600
Connection ~ 3600 2150
Wire Wire Line
	3600 2150 5000 2150
Connection ~ 3600 5600
Wire Wire Line
	3600 5600 4300 5600
Wire Wire Line
	9950 1800 9950 2000
Wire Wire Line
	10050 1800 10050 2000
Wire Wire Line
	9950 2000 9950 2100
Connection ~ 10050 2000
Wire Wire Line
	10050 2000 10050 3700
Wire Wire Line
	4600 2000 10050 2000
Wire Wire Line
	4700 2100 9950 2100
Connection ~ 9950 2100
Wire Wire Line
	9950 2100 9950 3600
Wire Wire Line
	8000 6100 8000 4200
Wire Wire Line
	8000 4200 8150 4200
Wire Wire Line
	8150 4100 8150 6200
$EndSCHEMATC
