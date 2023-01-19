from machine import ADC, Pin
import time, os

DATA_FILE = 'data.csv' 
PAUSE_SEC = 1 # 5*60

# 0=Temp, 1=Lum, 2=Hum
adcs = [ADC(Pin(27)), ADC(Pin(26)), ADC(Pin(28))]

def adc_mv( index ):
        global adcs
        val = 0
        for i in range(20):
            val += adcs[index].read_u16()
        return int((val/20)*3300/65535)
        
def temp():
        mv = adc_mv(0)
        return ( (mv-550)/10, mv)

try:
    os.stat( DATA_FILE )
except:
    print( 'Creating file %s' % DATA_FILE )
    with open( DATA_FILE, 'w' ) as f:
        f.write( 'unix_time,temp_celsius,temp_mv,lum_mv,hum_mv\r\n' )
        f.close()

# Data capture loop
while True:
        start = time.time()
        tmp   = temp()
        data = (start,)+temp()+(adc_mv(1),adc_mv(2))
        print( (data[2],data[3],data[4]) )
        
             
        with open( DATA_FILE, 'a' ) as f:
            f.write( '%i,%5.2f,%i,%i,%i\r\n' % data )
            f.close()        
        
        while time.time() - start < PAUSE_SEC:
            time.sleep_ms( 200 )
        
