from machine import Pin
import time

red = Pin( 8, Pin.OUT, value=1) # Rouge
ora = Pin( 9, Pin.OUT, value=0) # Orange
gre = Pin( 11, Pin.OUT, value=0) # Vert

walk_red = Pin( 21, Pin.OUT, value=1) # Pieton Rouge
walk_gre = Pin( 19, Pin.OUT, value=0) # Pieton Vert
walk_button = Pin( 18, Pin.IN, Pin.PULL_UP ) # Bouton

walk_click = 0
def walk_clicked( sender ):
 global walk_click 
 walk_click += 1

walk_button.irq( handler=walk_clicked, trigger=Pin.IRQ_FALLING )

while True:
 # Car driving
 red.off()
 ora.off()
 gre.on()
 walk_red.on()
 walk_gre.off()
 # Wait button press
 while walk_click == 0:
  time.sleep_ms( 200 )
 # Stopping car 
 ora.on()
 gre.off()
 time.sleep( 2 )
 red.on()
 ora.off()
 # Walking
 walk_gre.on()
 walk_red.off()
 time.sleep( 20 )
 # Stop Walker
 walk_red.on()
 walk_gre.off()
 time.sleep( 3 )
 # Reset counter
 walk_click = 0
