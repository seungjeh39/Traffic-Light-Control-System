# Traffic Light Implementation (Interrupt) - Seungjeh Lee

import RPi.GPIO as GPIO
from time import sleep


LED1R_PIN = 13
LED1B_PIN = 19
LED1G_PIN = 26
LED2R_PIN = 21
LED2B_PIN = 20
LED2G_PIN = 16
BUTTON_PIN = 5
DISPLAY_A = 23
DISPLAY_B = 18
DISPLAY_C = 27
DISPLAY_D = 17
DISPLAY_E = 4
DISPLAY_F = 25
DISPLAY_G = 24
#DISPLAY_DP - don't need decimal point

GPIO.setmode(GPIO.BCM)

# RGB LED Light 1
RGB1 = [LED1R_PIN, LED1G_PIN, LED1B_PIN]
for pin in RGB1:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

# RGB LED Light 2
RGB2 = [LED2R_PIN, LED2G_PIN, LED2B_PIN]
for pin in RGB2:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

# Press Button
GPIO.setup(BUTTON_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

# 7-Segments Display
segments = (DISPLAY_A, DISPLAY_B, DISPLAY_C, DISPLAY_D, DISPLAY_E, DISPLAY_F, DISPLAY_G)
GPIO.setup(segments,GPIO.OUT,initial=0)
#            (a,b,c,d,e,f,g, dp)
numDict = {0:(1,1,1,1,1,1,0),
           1:(0,1,1,0,0,0,0),
           2:(1,1,0,1,1,0,1),
           3:(1,1,1,1,0,0,1),
           4:(0,1,1,0,0,1,1),
           5:(1,0,1,1,0,1,1),
           6:(1,0,1,1,1,1,1),
           7:(1,1,1,0,0,0,0),
           8:(1,1,1,1,1,1,1),
           9:(1,1,1,1,0,1,1),
           -1:(0,0,0,0,0,0,0)}

try:
    while True:
        GPIO.output(LED2G_PIN,1)    # light 2 stays green
        GPIO.wait_for_edge(BUTTON_PIN,GPIO.BOTH)   

        if not GPIO.input(BUTTON_PIN):   # button is pressed
            print("button pressed")
            GPIO.output(LED2G_PIN,0)
            
            for i in range(3):  # blue blink 3 times
                GPIO.output(LED2B_PIN,1)
                sleep(1)
                GPIO.output(LED2B_PIN,0)
                sleep(1)

            GPIO.output(LED2R_PIN,1)    # light 2 turns red
            GPIO.output(LED1R_PIN,0)
            GPIO.output(LED1G_PIN,1)    # light 1 turns green

            #countdown panel
            j = 0
            for x in range(9,-1,-1):
                GPIO.output(segments,numDict[x])
                sleep(1)

                if x == 4:
                    GPIO.output(LED1G_PIN,0)
                    GPIO.output(LED1B_PIN,1)
                elif x == 3 or x == 1:
                    GPIO.output(LED1B_PIN,0)
                elif x == 2:
                    GPIO.output(LED1B_PIN,1)
                elif x == 0:
                    GPIO.output(LED1R_PIN,1)
                    GPIO.output(LED2R_PIN,0)
                    GPIO.output(LED2G_PIN,1)
                    
                    while j < 4:    # button cooltime of 20 sec
                        sleep(1)
                        j += 1
                        
            GPIO.output(segments,numDict[-1])  # turns off 7-segments display
            
except KeyboardInterrupt:
    GPIO.cleanup()