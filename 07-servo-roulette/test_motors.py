from machine import Pin
from servo import Servo9090
from time import sleep

# Robotic Plateform
RIGHT_SERVO = 15
LEFT_SERVO  = 16

left = Servo9090( Pin(LEFT_SERVO) )
right = Servo9090( Pin(RIGHT_SERVO) )

left.angle = +90
right.angle = -90

sleep( 2 )

left.angle = 0
right.angle = 0

sleep( 1 )

left.angle = -90
right.angle = +90

sleep( 2 )

left.angle = 0
right.angle = 0
