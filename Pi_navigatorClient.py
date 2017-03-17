import socket
import time
import RPi.GPIO as gpio
import sys

host = 'xxx.xxx.xx.xxx'                                      #address of the pi in the Lan, find through ifonfig
port = xxxx                                                  #random unused port, ie above 1000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))                                           #socket for getting data from surf program..ie centroid

host2 = 'xxx.xxx.xx.xx'                                        #address of the pi in the Lan, find through ifonfig
port2 = xxx                                                    #random unused port, diff from previous one , ie above 1000
e = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
e.bind((host2,port2))                                       #socket for getting distance from ultransonic sensor program
e.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)          #sets the buffer queue length to 1, ie. dont need to save previous values more than one in number

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(19, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

def rotateleft(tf):
    init()
    gpio.output(19,True)
    gpio.output(11,False)
    gpio.output(13,True)
    gpio.output(15,False)
    time.sleep(tf)
    gpio.cleanup()

def rotateright(tf):
    init()
    gpio.output(19,False)
    gpio.output(11,True)
    gpio.output(13,False)
    gpio.output(15,True)
    time.sleep(tf)
    gpio.cleanup()

def foreward(tf):
    init()
    gpio.output(19,False)
    gpio.output(11,False)
    gpio.output(13,True)
    gpio.output(15,True)
    time.sleep(tf)
    gpio.cleanup()



def search():
    while True:
        print "searching .."
        rotateright(0.030)                            
        data, addr = s.recvfrom(1024)                  #get centroid form surf program as string
        end = len(data)
        clon = data[1:(end-1)]
        p, q = map(float, clon.split(','))             # string decoded into float

        if (p == -1)&(q == -1):                      
            pass                                       #if object not found do nothing and go to next iteration

        else:                                          #if object found start to verify
            count = 0                                  
            r = time.time()
            t = time.time()
            while t-r < 1.5:                            #verification period = 1.5 sec, t=stop, r=start times respectively
                print "verifying"
                data, addr = s.recvfrom(1024)
                end = len(data)
                clon = data[1:(end-1)]
                p, q = map(float, clon.split(','))     

                if p!=-1 and q!=-1:                      #object found  
                    count = count+1                      #increment count if obj found
                t = time.time()                          #stop time increases till t-r < 1.5, ie. verification runs till 1.5 sec
        
            if count > 5:                               #if object found more than 5 time in verify period, search phase complete
                print "verified"
                break
            else:
                pass
                
    return 2


def allignment():
    flag = 0
    lag = 0
    while True:
        data, addr = s.recvfrom(1024)
        end = len(data)
        clon = data[1:(end-1)]
        p, q = map(float, clon.split(','))

        if p ==-1 and flag==0:                    #if obj dissapears durng allignment start timer
            start = time.time()
            flag = 1
            

        if p ==-1 and flag!=0:                    #if object not found still , increment counter
            stop = time.time()
            lag = stop - start                    # lag gives time elapsed for which object dosent appear once

        if lag > 5:                               #if object dissapears for more than 5 sec search again
            return 1

        if p<283.0 and p!=-1:
            print "rotating left"
            rotateleft(0.030)
            start = time.time()
            flag = 0                             #if the object appears even once reset timer

        if p>339.0:
            print "rotating right"
            rotateright(0.030)
            start = time.time()
            flag = 0

        if 283 < p < 339: 
            print 'aligned'
            start = time.time()
            break                                #if alligned break and go to ram(), to move closer to the target

    return 3

def ram():
    datak, adres= e.recvfrom(1024)
    d = float(datak)                            #get distance from ultrasonic sensor program
    print d
    flag=0
    lg=0

    while d>10:
        data, addr = s.recvfrom(1024)
        end = len(data)
        clon = data[1:(end-1)]
        p, q = map(float, clon.split(','))
        

        datak, adres = e.recvfrom(1024)
        d = float(datak)
        print d
        
        if 283 < p < 339:                       #if still alligned move foreward
            foreward(0.030)
            flag=0
        elif not(283 < p < 339) and p!=-1:      #if allignment lost goto allignment()
            r = allignment()
            flag=0
        else:                                   #if object lost for more than 5 sec go back to search()
            if flag==0:
                st = time.time()
                flag=1
            else:
                en = time.time()
                lg = en-st
                if lg>5:
                    return 1
                

    return 4

def pickup():                                      #pickup rputine to be written
    print "pickup routine"
    time.sleep(5)
    return 5

def fetch():
    print "fetching routine"
    time.sleep(5)
    return 6


def Main():
    c = 1
    try:
        while True:
            if c==1:                
                c = search()
            if c==2:
                c = allignment()
            if c==3:
                c = ram()
            if c==4:
                c = pickup()
            if c==5:
                c = fetch()
            if c==6:
                s.close()
                e.close()
                gpio.cleanup()
                print "port closed"
                break
                

    except KeyboardInterrupt:
        s.close()
        e.close()
        gpio.cleanup()
        print "port closed"

if __name__=='__main__':
    Main()
            
            
        
     

    
    
        

    
    
