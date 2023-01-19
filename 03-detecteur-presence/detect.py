from machine import Pin
import time

HIGH_MIN = 10

pir = Pin( 22, Pin.IN, Pin.PULL_UP )
relay = Pin( 19, Pin.OUT, value=False )

last_detect = time.time() - (HIGH_MIN+1)*60

def detected( sender ):
	global last_detect
	last_detect = time.time()

pir.irq( trigger=Pin.IRQ_FALLING, handler=detected )

while True:
	relay.value( (time.time()-last_detect) < (HIGH_MIN*60) )
	time.sleep_ms(300)
