import time

# The RPi/Python/LED interface
import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BCM) ## Use internal pin numbering

# Initialize LEDs
# Green light
GPIO.setup(25, GPIO.OUT) ## Setup GPIO pin 25 to OUT

# Initialize Pulse width modulation on GPIO 25. Frequency=100Hz and OFF
pG = GPIO.PWM(25, 100)
pG.start(0)

# Red light
GPIO.setup(22, GPIO.OUT) ## Setup GPIO pin 22 to OUT

# Initialize Pulse width modulation on GPIO 22. Frequency=100Hz and OFF
pR = GPIO.PWM(22, 100)
pR.start(0)

# Test light dimming and relative brightnesses
i = 0
while True:
    try:
        if (i == 100): direction = -1
        if (i == 0): direction = 1

        # The differnece in level of brightness is more perceptable at lower levels.
        # Therefore, square the intensity to change the brightness distribution. 
        redIntensity = (((i*.2)**2)/10000) * 100 
        greenIntensity = (((100-i)**2)/10000) * 100
        pR.ChangeDutyCycle(redIntensity)
        pG.ChangeDutyCycle(greenIntensity)
        i += direction
        time.sleep(.2)
        print(str(i))
        print(str(redIntensity))
        print(str(greenIntensity))

    except KeyboardInterrupt:
        pG.stop()
        pR.stop()
        GPIO.cleanup()
        quit()
