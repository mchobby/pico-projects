##
# servo.py : class to controle servo motor for Raspberry-Pi Pico
#
# Copyright 2022 - Meurisse Domniique <info@mchobby.be>
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
from machine import PWM

class Servo:
	""" Controle servo de 0 à 180°. Signal de 0.5 à 2.5ms """
	def __init__(self, pin ):
		self.s = PWM( pin )
		self.s.freq( 50 )
		self._angle = None
		self.detach()

	def detach( self ):
		# Desactiver l asservissement moteur
		self.s.duty_ns( 0 ) # Pas de signal

	def attach( self ):
		# reactiver l'asservissement au dernier angle connu
		if self._angle:
			self.angle = self._angle

	@property
	def angle( self ):
		return self._angle

	@angle.setter
	def angle( self, degrees ):
		assert 0<=int(degrees)<=180, "Invalid angle"
		self._angle = int(degrees)
		# Map angle to nanoseconds
		ns = 500000 + 2000000/180*self._angle
		self.s.duty_ns( int(ns) )


class Servo9090:
	""" Controle servo de -90° à +90°. Signal de 0.5 à 2.5ms """
	def __init__(self, pin ):
		self._servo = Servo( pin )
		self.detach = self._servo.detach
		self.attach = self._servo.attach

	@property
	def angle( self ):
		if self._servo.angle == None:
			return None
		else:
			return self._servo.angle-90

	@angle.setter
	def angle( self, degrees ):
		assert -90<=int(degrees)<=90, "Invalid angle"
		self._servo.angle = degrees+90
