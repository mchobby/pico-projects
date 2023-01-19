from machine import Pin, ADC
from neopixel import NeoPixel
import time

MAX_LED    = 7
COLD_COLOR = (0,0,255) # R,G,B
WARM_COLOR = (255,0,0)
COLD_TEMP  = 16 # 20
WARM_TEMP  = 30 # 25

neo = NeoPixel( Pin(11), MAX_LED )
adc = ADC( Pin(26) ) # ADC(0) on GPIO26

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
		# Calculate color
		r = int( map( temp, COLD_TEMP, WARM_TEMP, COLD_COLOR[0], WARM_COLOR[0] ) )
		g = int( map( temp, COLD_TEMP, WARM_TEMP, COLD_COLOR[1], WARM_COLOR[1] ) )
		b = int( map( temp, COLD_TEMP, WARM_TEMP, COLD_COLOR[2], WARM_COLOR[2] ) )
		# Send to NeoPixel
		for i in range( MAX_LED ):
			neo[i] = (r,g,b)
		neo.write()
		time.sleep_ms( 500 )
finally:
	neo.fill( (0,0,0) )
	neo.write()
