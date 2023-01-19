""" Small class to propel the a Chassis with Servo-Controller DC Motor or
    Continuous Rotation Servo motor.

	Based on Zumo Châssis for PYBStick
	   https://github.com/mchobby/pybstick-projects/tree/master/zumo

	D.Meurisse for shop.mchobby.be
	02/10/2022, Domeu, Initial commit for Raspberry-Pi Pico
"""
from time import sleep_ms
from machine import Pin
from servo import Servo9090

class ServoCar:
	""" A mini class to drive a Zumo Chassis (POL-1418) + DFRobot Servo motor (DFR0399) """
	def __init__( self, left_servo, right_servo ):
		self._left  = Servo9090( Pin(left_servo) )
		#self.left.calibration(500, 2500, 1500, 2500, 2500)
		self._right = Servo9090( Pin(right_servo) )
		#self.right.calibration(500, 2500, 1500, 2500, 2500)
		self._moving = False
		self.stop()

	@property
	def is_moving( self ):
		return self._moving

	def stop( self ):
		self._right.angle = 0
		self._left.angle = 0
		self._moving = False

	def speed( self, speed ):
		""" Speed from -90 (backward) to +90 (forward) """
		self._right.angle = -1*speed
		self._left.angle = speed
		self._moving = True

	def right( self, speed, time_ms=None ):
		""" Turn right @ given speed. if time_ms is given, it stop after the given time """
		self._right.angle = speed
		self._left.angle = speed
		self._moving = True
		if time_ms:
			sleep_ms( time_ms )
			self.stop()

	def left( self, speed, time_ms=None ):
		""" Turn left @ given speed. if time_ms is given, it stop after the given time """
		self.right( -1*speed, time_ms )
