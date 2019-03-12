def pump_on():
    import RPi.GPIO as GPIO  
    from time import sleep
    GPIO.setmode(GPIO.BCM)
    pump_pin=19
    pump2_pin=26
    #second pump is sonnected to pin 26
    #water sensors 18, 21
    watersensor_pin=21
    watersensor2_pin=18
    
    GPIO.setup(watersensor_pin, GPIO.IN)
    GPIO.setup(pump_pin, GPIO.OUT)
    
    GPIO.setup(watersensor2_pin, GPIO.IN)
    GPIO.setup(pump2_pin, GPIO.OUT)
 
    try:
        while True:# this will carry on until you hit CTRL+C
            if GPIO.input(watersensor_pin) or GPIO.input(watersensor2_pin):
                if GPIO.input(watersensor_pin):
                    print("no water detected in sensor_1")
                    GPIO.output(pump_pin, GPIO.HIGH)
                if GPIO.input(18):
                    print("no water detected in sensor_2")
                    GPIO.output(pump2_pin, GPIO.HIGH)
                sleep(2)
                GPIO.output(pump_pin, GPIO.LOW)
                GPIO.output(pump2_pin, GPIO.LOW)
            else:
                print("water detected")  
            # set port/pin value to 0/LOW/False  
            sleep(0.3)         # wait 0.1 seconds  
           
    finally:                   # this block will run no matter how the try block exits  
        GPIO.cleanup()         # clean up after yourself  
    
pump_on()
        

