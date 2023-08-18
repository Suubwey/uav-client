# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER_1 = 23
GPIO_ECHO_1 = 12

GPIO_TRIGGER_2  = 24
GPIO_ECHO_2 = 16

GPIO_TRIGGER_3 = 25
GPIO_ECHO_3 = 20

GPIO_TRIGGER_4 = 8
GPIO_ECHO_4 = 21

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)

GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)

GPIO.setup(GPIO_TRIGGER_3, GPIO.OUT)
GPIO.setup(GPIO_ECHO_3, GPIO.IN)

GPIO.setup(GPIO_TRIGGER_4, GPIO.OUT)
GPIO.setup(GPIO_ECHO_4, GPIO.IN)

def distance(trigger, echo):
    try:
        # set Trigger to HIGH
        GPIO.output(trigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        timeout = time.time()+0.1 # Adding a timeout to avoid infinite loop
        # save StartTime
        while GPIO.input(echo) == 0 and time.time() < timeout:
            StartTime = time.time()

        timeout = time.time()+0.1 # Resetting timeout
        # save time of arrival
        while GPIO.input(echo) == 1 and time.time() < timeout:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime

        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance
    except Exception as e:
        print(f"An error occurred while measuring distance: {e}")
        return None

if __name__ == '__main__':
    try:
        while True:
            dist1 = distance(GPIO_TRIGGER_1, GPIO_ECHO_1)
            print("Measured Distance 1 = %.1f cm" % dist1)
            time.sleep(0.1) # Adding a short delay
            dist2 = distance(GPIO_TRIGGER_2, GPIO_ECHO_2)
            print("Measured Distance 2 = %.1f cm" % dist2)
            time.sleep(0.1)
            dist3 = distance(GPIO_TRIGGER_3, GPIO_ECHO_3)
            print("Measured Distance 3 = %.1f cm" % dist3)
            time.sleep(0.1)
            dist4 = distance(GPIO_TRIGGER_4, GPIO_ECHO_4)
            print("Measured Distance 4 = %.1f cm" % dist4)
            time.sleep(1) 
            # Wait for 1 second before next measurement

    except KeyboardInterrupt:   
        print("Measurement stopped by User")
        GPIO.cleanup()
