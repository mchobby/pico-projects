from machine import Pin
from ultrasonic import Ultrasonic
from servocar import ServoCar
from time import sleep, sleep_ms
from random import choice, randint

# Ultrasonic
TRIGGER_PIN = 28
ECHO_PIN = 22
# Robotic Plateform
RIGHT_SERVO = 15
LEFT_SERVO  = 16
# User Button
BTN_PIN = 5
LED_PIN = 25

sr04 = Ultrasonic( TRIGGER_PIN, ECHO_PIN )
car = ServoCar( left_servo = LEFT_SERVO, right_servo = RIGHT_SERVO )
sw = Pin( BTN_PIN, Pin.IN, Pin.PULL_UP )
led = Pin( LED_PIN, Pin.OUT )

# Wait button to be pressed
while sw.value():
	sleep( 0.100 )

# wait 10 secondes before start
for i in range(9):
	led.on()
	sleep_ms( 100 )
	led.off()
	sleep_ms( 900 )
# Final indicator
led.on()
sleep(1)
led.off()

try:
	while True:
		# if object detected
		while sr04.distance_in_cm() <= 25:
			# turn on right (positive speed) or left (negative speed) during a
			# random amount of time (400ms to 1.5s) to find an escape.
			car.right( speed = choice([-50,+50]), time_ms=randint(400,1500) )
		if not car.is_moving:
			car.speed( 80 ) # Move forward @ speed
		if sw.value()==0:
			break
finally:
	car.stop()
