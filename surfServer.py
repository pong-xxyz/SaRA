import cv2
import numpy as np
import Tkinter
import time
import socket

host = 'xxx.xxx.xxx.xx'    #ip address of computer where the surf program is run
port = xxxx                 #random unused port

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
print "server started"


MIN_MATCH_COUNT=10

def centeroid(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:,0, 0])
    sum_y = np.sum(arr[:,0, 1])
    return sum_x/length, sum_y/length



img1 = cv2.imread('teat.jpg',0) 

surf = cv2.xfeatures2d.SURF_create()
kp1, des1 = surf.detectAndCompute(img1,None)

cap = cv2.VideoCapture("http://192.168.43.216:8080/?action=stream")


while(True):

    ret, frame = cap.read()
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    kp2, des2 = surf.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
   

    if(len(kp1)>=2 & len(kp2)>=2): 
        matches = flann.knnMatch(np.asarray(des1,np.float32),np.asarray(des2,np.float32),k=2)
        
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
 
        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            matchesMask = mask.ravel().tolist()
            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            
            if M!= None:            
                dst = cv2.perspectiveTransform(pts,M)
               

                img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
                p,q = centeroid(dst)                                                                           #if obj found , save centroid in p,q else p,q=-1
            else:
                p = -1
                q = -1

        else:
            
            matchesMask = None
            p = -1
            q = -1
    else:
        p = -1
        q = -1



    cv2.imshow('frame',img2)    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        s.close()
        print "port closed"
        break
        

    data = p, q
    print "sending:"+str(data)
    s.sendto(str(data), ('xxx.xxx.xxx.xx', xxxx))   #ip addres of pi and port used by the 's' variable in navigator.py

    

cap.release()
cv2.destroyAllWindows()
        





