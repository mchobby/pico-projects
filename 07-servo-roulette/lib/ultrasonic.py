##
# Ultrasonic library for MicroPython's Pico.
# Compatible with HC-SR04 and SRF04.
#
# Copyright 2014 - Sergio Conde Gómez <skgsergio@gmail.com>
# Improved by Mithru Vigneshwara
# Adapted by Meurisse D. (MCHobby.be) for the Pico
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from machine import Pin, time_pulse_us
from time import sleep_us


class Ultrasonic:
	def __init__(self, tPin, ePin):
		self.triggerPin = tPin
		self.echoPin = ePin

		# Init trigger pin (out)
		self.trigger = Pin(self.triggerPin)
		self.trigger.init(Pin.OUT)
		self.trigger.low()

		# Init echo pin (in)
		self.echo = Pin(self.echoPin)
		self.echo.init(Pin.IN)

	def distance_in_inches(self):
		return (self.distance_in_cm() * 0.3937)

	def distance_in_cm(self):
		# Send a 10us pulse.
		self.trigger.high()
		sleep_us(10)
		self.trigger.low()

		# Wait that Pin goes high then COUNT the time it stays HIGH
		usec = time_pulse_us( self.echo, 1)

		if usec < 0: # no echo response
			return 99999

		# Calc the duration of the recieved pulse, divide the result by
		# 2 (round-trip) and divide it by 29 (the speed of sound is
		# 340 m/s and that is 29 us/cm).
		dist_in_cm = (usec / 2) / 29

		return dist_in_cm
