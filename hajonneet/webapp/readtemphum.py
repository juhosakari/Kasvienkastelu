def temphum():
    import pigpio
    from time import sleep
    import RPi.GPIO as GPIO  
    pi=pigpio.pi()
    import DHT22
    datapin=4
    s=DHT22.sensor(pi,datapin)
    s.trigger()
    sleep(2)
    t=s.humidity()
    h=s.temperature()
        #read soil moisture sensor
    GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
    GPIO.setup(18, GPIO.IN)
               # this will carry on until you hit CTRL+C  
    if GPIO.input(18):
        m="Soil is DRY"
        print("no water detected")
    else:
        print("water detected")
        m="Soil is WET"  
        
    
    #print(t,s)
    print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t,h))
    s.cancel
    pi.stop()
    
    return(t,h,m)
