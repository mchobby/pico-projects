from machine import Pin, PWM, Timer
import time
import random

class HPin( Pin ):
    def __hash__( self ):
        return hash( '%r' % self )

btn_j1 = HPin( 10, Pin.IN, Pin.PULL_UP )
btn_j2 = HPin( 21, Pin.IN, Pin.PULL_UP )
btn_round = HPin( 16, Pin.IN, Pin.PULL_UP )

led_j1 = Pin( 9, Pin.OUT )
led_j2 = Pin( 22, Pin.OUT )
led_round = Pin( 17, Pin.OUT )

LED_OF = { btn_j1 : led_j1, btn_j2 : led_j2 }

# Notes = Cle,Frequence
# 523.25, 587.33, 659.26, 698.46, 783.99, 880, 987.77, 1046.50
NOTES = { 'C1':523, 'D1': 587, 'E1':659, 'F1':698, 'G1':784, 'A1':880, 'B1':988, 'C2': 1046 }

buz = PWM( Pin(14) )
buz.duty_u16( 0 )
def tone( freq ):
    global tone
    if freq==0:
        buz.duty_u16( 0 ) # stop sound
    else:
        buz.freq( freq )
        buz.duty_u16( 21845  ) # 30% duty

def play_string( s ):
    # Joue une séquence de note.durée_ms
    #play_string( "C1.100,E1.50,B1.300" )
    for substr in s.split(','):
        note,duration = substr.split('.')
        #print( note, duration )
        tone( NOTES[note] )
        time.sleep_ms( int(duration) )
    tone( 0 ) # silence 

# play_string( "C1.100,E1.50,B1.300" )
blink_led = None
def blinking( sender ):
    global blink_led
    if blink_led != None:
        blink_led.toggle()
        
timer=Timer(-1)
timer.init(period=100, mode=Timer.PERIODIC, callback = blinking )

def clear_all():
    global blink_led, led_j1, led_j2, led_round
    blink_led = None
    tone(0)
    led_j1.value( 0 )
    led_j2.value( 0 )
    led_round.value( 0 )


while True:
    # En attente d'un nouveau round
    blink_led = led_round
    while not( btn_round.value()==0 ):
        time.sleep_ms( 50 )
    # Bouton pressé
    clear_all()
    # Signal départ du round
    for i in range( 4 ):
        led_round.value( 1 )
        play_string( 'C1.200' )
        led_round.value( 0 )
        time.sleep_ms( 500 )
    play_string( 'C2.1000' )
    # Attendre un temps aléatoire
    pause = random.randint( 3, 12 )
    start = time.time() 
    while time.time() - start < pause:
        # Un joueur presse trop tôt ?
        if btn_j1.value()==0:
            blink_led = led_j1
        if btn_j2.value()==0:
            blink_led = led_j2
    # C'est le moment de jouer
    tone( NOTES['C2'] )
    led_round.value( 1 )
    # attendre un gagnant (10 sec max)
    start = time.time()
    winner = None 
    while time.time() - start < 10:
        for btn in (btn_j1, btn_j2):
            # s'il blink, il ne peut pas jouer 
            if LED_OF[ btn ] == blink_led:
                continue
            if btn.value()==0:
                clear_all()
                # Un gagnant!
                LED_OF[ btn ].value(1) # Allumer gagnant
                play_string('E1.200,D1.200,E1.200,D1.200,F1.800')
                # Arrête le while loop
                break
