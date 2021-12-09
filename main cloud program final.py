import http.client as http
import urllib.parse
import urllib.request
import requests
import smbus
import time
import RPi.GPIO as GPIO
import subprocess
import RPi.GPIO as GPIO
import time
key = "FJCJRJK3MCFK99Z2"  

buttonPin = 12
ledPin    = 11


address = 0x48#default address of PCF8591
bus=smbus.SMBus(1)
cmd=0x40#command


def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       
    GPIO.setup(ledPin, GPIO.OUT)   
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   

def analogRead(chn):#read ADC value,chn:0,1,2,3
    value = bus.read_byte_data(address,cmd+chn)
    return value
    
def analogWrite(value):#write DAC value
    bus.write_byte_data(address,cmd,value)

def loop():
    if True:
        value = analogRead(0)#read the ADC value of channel 0
        analogWrite(value)#write the DAC value
        voltage = value / 255.0 * 5.0  #calculate the voltage value
        print ('ADC Value : %d, Voltage : %.2f'%(value,voltage))
        time.sleep(3.1)
        count =  1
   
    while (voltage<=2.7) and count<=100:
        params = urllib.parse.urlencode({'field1':voltage , 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.HTTPConnection("api.thingspeak.com:80")
	
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            print("Voltage high, Truck loaded")
            time.sleep(3)
            if   GPIO.input(buttonPin)==GPIO.LOW:  
                print ('BODY TIPPED UP','ADC Value : %d, Voltage : %.2f'%(value,voltage))
                time.sleep(3.1)
                
                if GPIO.input(buttonPin)!=GPIO.LOW:
                    print ('TIPPED DOWN','ADC Value : %d, Voltage : %.2f'%(value,voltage))
                    time.sleep(3)
               
                    if count>0:
                        (voltage<3.0)
                        print("TRUCK TRIP",count)
                        count=count+1
                        time.sleep(6)                    
            else:
                print("NO TRIP")
            
        except:
            print("NO trip")
            print("connection failed")

def destroy():
    
    GPIO.output(ledPin, GPIO.LOW)    #led off                                                                                    
    GPIO.cleanup()
    bus.close()

if __name__ == '__main__':
    try:
        setup()
        loop()
        
   
    except KeyboardInterrupt:
        destroy()     

