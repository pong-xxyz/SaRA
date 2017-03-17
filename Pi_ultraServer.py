import RPi.GPIO as gpio
import time
import socket

host = 'xxx.xxx.xxx.xxx' #ip of the pi in the Lan
port = xxxx                # random unused port, has to be diff from ones used in other programs

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
print "started"

def distance():   

    gpio.setmode(gpio.BOARD)
    TRIG=7
    ECHO=12

    gpio.setup(TRIG,gpio.OUT)
    gpio.setup(TRIG,0)

    gpio.setup(ECHO,gpio.IN)

    time.sleep(0.1)


    gpio.output(TRIG,1)
    time.sleep(0.00001)
    gpio.output(TRIG,0)

    while gpio.input(ECHO) == 0:
          pass
    start = time.time()

    while gpio.input(ECHO) == 1:
          pass
    stop = time.time()

    dist=(stop-start) * 17000
    print(dist)

    gpio.cleanup() 
    return dist



try:
    while (True):
        d = distance()
        print "sending"+str(d)
        s.sendto(str(d),('xxx.xxx.xxx.xx',xxxx)) #IP address of pi and the port is the one used in navigator program, ie. the port used in 'e' variable

except KeyboardInterrupt:
    s.close()
    print "port closed"
    gpio.cleanup()





    
    
