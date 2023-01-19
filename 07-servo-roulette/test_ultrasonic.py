from machine import Pin
from ultrasonic import Ultrasonic
from time import sleep

# Ultrasonic
TRIGGER_PIN = 28
ECHO_PIN = 22

sr04 = Ultrasonic( TRIGGER_PIN, ECHO_PIN )

counter = 0
while True:
	counter += 1
	dist = sr04.distance_in_cm()
	print( "iteration %i : %s cm" % (counter,dist) )
	sleep( 1 )
