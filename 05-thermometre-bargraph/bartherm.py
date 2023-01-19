from machine import Pin, ADC
import time

BASE_LED_GPIO = 8
MAX_LED = 10 # from GPIO 8..17

COLD_TEMP  = 20 #16 # 20
WARM_TEMP  = 25 #30 # 25

adc = ADC( Pin(26) ) # ADC(0) on GPIO26
leds = []
for index in range( MAX_LED ):
	leds.append( Pin(BASE_LED_GPIO+index, Pin.OUT, value=0) )
#for led in leds:
#	print( led )

def map(x, in_min, in_max, out_min, out_max):
	# return float
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

temp = 0
try:
	while True:
		# Read temp
		val = 0
		for i in range(20):
			val += adc.read_u16() # 0-65535
		val = val/20

		volts = 3.3 * val / 65535
		# convert voltage to temperature
		temp += (volts-0.55)*100
		temp /= 2
		print( 'Val: %5i,  Volts: %5.3f, Temp: %5.3f' % (val,volts,temp) )
		if temp > WARM_TEMP:
			temp = WARM_TEMP
		elif temp < COLD_TEMP:
			temp = COLD_TEMP
		# Calculate led to light
		on_idx = int( map( temp, COLD_TEMP, WARM_TEMP, 0, MAX_LED-1 ) )
		# Update all the LEDs
		for index, led in enumerate( leds ):
			led.value( index==on_idx )
		time.sleep_ms( 500 )
finally:
	# Switch off
	for led in leds:
		led.value( 0 )
