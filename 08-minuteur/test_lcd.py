from machine import Pin, I2C
from lcdi2c import LCDI2C

# Pico - GP8=sda, GP9=scl
i2c = I2C(0)

lcd = LCDI2C( i2c, cols=16, rows=2 )
lcd.clear()
lcd.backlight()
lcd.home()
lcd.print( 'Hello' )
