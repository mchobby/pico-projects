from machine import Pin
from servocar import ServoCar
from time import sleep

# Robotic Plateform
RIGHT_SERVO = 15
LEFT_SERVO  = 16

car = ServoCar( left_servo = LEFT_SERVO, right_servo = RIGHT_SERVO )

car.speed( 80 ) # Move forward @ speed
sleep( 2 )

car.stop()
sleep( 1 )

car.speed( -80 ) # Move backward
sleep( 2 )

car.stop()

car.right( 50 ) # turn right
sleep( 2 )

car.left( 50 ) # turn right
sleep( 2 )

car.stop()
