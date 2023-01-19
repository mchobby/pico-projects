from machine import Pin, I2C, PWM
from lcdi2c import LCDI2C
import time

BUZZER_PIN = 15
PLUS1_BTN_PIN = 16
PLUS5_BTN_PIN = 17
RESET_BTN_PIN = 18
START_BTN_PIN = 19 # Start/Stop

# value for state
CONFIGURE=1 # Configure time
RUNNING=2   # Countdown the time

# --- LCD ---
# Pico - GP8=sda, GP9=scl
i2c = I2C(0)
lcd = LCDI2C( i2c, cols=16, rows=2, address=0x27 )
lcd.clear()
lcd.backlight()
lcd.home()

# --- Buzzer ---
buz = PWM( Pin(BUZZER_PIN) )
buz.freq( 4000 ) # 4 KHz
buz.duty_u16( 0 ) # Off

# --- Buttons ---
plus1_btn = Pin( PLUS1_BTN_PIN, Pin.IN, Pin.PULL_UP )
plus5_btn = Pin( PLUS5_BTN_PIN, Pin.IN, Pin.PULL_UP )
reset_btn = Pin( RESET_BTN_PIN, Pin.IN, Pin.PULL_UP )
start_btn = Pin( START_BTN_PIN, Pin.IN, Pin.PULL_UP )
btns = [plus1_btn, plus5_btn, reset_btn, start_btn]
last_btn_values = {}
for btn in btns:
	last_btn_values['%r'%btn] = btn.value()

def get_pressed():
	# Check which button is pressed and released. If such then it is returned
	# into the list.
	global btns, last_btn_values
	_changed = []
	_result = []
	for btn in btns:
		if btn.value() != last_btn_values['%r'%btn]:
			_changed.append( btn ) # must be cheched again in 10ms
	time.sleep_ms(10)
	for btn in _changed:
		val = btn.value()
		if val != last_btn_values['%r'%btn]: # If still changed
			# Button released?
			if (last_btn_values['%r'%btn] == 0) and (val==1):
				_result.append( btn )
			# Remember new state
			last_btn_values['%r'%btn] = val
	return _result

def disp_configure( mins ):
	# Display configuration screen
	global lcd
	lcd.home()
	lcd.print("Configure:")
	lcd.set_cursor( (0,1) ) # second line
	lcd.print( "%s minutes" % mins )

def disp_running( mins, remain_sec ):
	# Display Running screen
	global lcd
	lcd.home()
	lcd.print("Running %s min." % mins)
	lcd.set_cursor( (1,1) ) # second line
	lcd.print( "%3i min %2i sec" % (abs(remain_sec)//60,abs(remain_sec)%60) )
	if remain<0:
		lcd.set_cursor( (0,1) ) # second line
		lcd.print('-')

state = CONFIGURE
minutes = 0

while True:
	pressed = get_pressed()
	# print( pressed )
	if (state==CONFIGURE) and (plus1_btn in pressed):
		minutes += 1

	if (state==CONFIGURE) and (plus5_btn in pressed):
		minutes += 5

	if (state==CONFIGURE) and (reset_btn in pressed):
		minutes = 0

	if start_btn in pressed:
		if (state==CONFIGURE) and (minutes>0):
			lcd.clear()
			start = time.time()
			state = RUNNING
		elif state==RUNNING:
			lcd.clear()
			buz.duty_u16( 0 ) # Buzzer OFF
			state = CONFIGURE

	if state==CONFIGURE:
		disp_configure( minutes )
	elif state==RUNNING:
		elapsed = time.time() - start # in seconds
		remain  = minutes*60 - elapsed
		disp_running( minutes, remain )
		if remain < 0:
			buz.duty_u16( 21845 if ((remain%2)==1) and (remain>-60) else 0 )
