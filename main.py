import numpy as np
import pygame
import cv2
import time
pygame.init()
yellowLower = (20,100,100)
yellowUpper = (30,255,255)
greenLower = (40,100,50)
greenUpper = (70,255,255)

camera = cv2.VideoCapture(0)
while True:
    ret, frame = camera.read()
    frame = cv2.resize(frame, (1250,800))

    snare = cv2.imread("drum.png")
    snare = cv2.resize(snare, (200,200))
    frame[600:800,200:400] = snare

    bassdrum = cv2.imread("bassdrum.png")
    bassdrum = cv2.resize(bassdrum, (200,200))
    frame[600:800,550:750] = bassdrum

    tomtoms = cv2.imread("tomtoms.png")
    tomtoms = cv2.resize(tomtoms, (200,200))
    frame[600:800,900:1100] = tomtoms

    cymbol = cv2.imread("cymbol.png")
    cymbol = cv2.resize(cymbol, (200,200))
    frame[250:450,50:250] = cymbol

    cowbell = cv2.imread("cowbell.jpg")
    cowbell = cv2.resize(cowbell, (200,200))
    frame[250:450,1000:1200] = cowbell

    
    cymbol = pygame.mixer.Sound('cymbol.wav')
    snare = pygame.mixer.Sound('snare.wav')
    bassdrum = pygame.mixer.Sound('bassdrum.wav')
    cowbell = pygame.mixer.Sound('cowbell.wav')
    tomtoms = pygame.mixer.Sound('tomtoms.wav')

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask2 = cv2.inRange(hsv, greenLower, greenUpper)
    cv2.imshow("mask",mask)
    cv2.imshow("mask2",mask2)
    mask = cv2.erode(mask, None, iterations=2)
    mask2 = cv2.erode(mask2, None, iterations=2)

    mask = cv2.dilate(mask, None, iterations=2)
    mask2 = cv2.dilate(mask2, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    center2 = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))


        if radius > 0:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            x=int(x)
            y=int(y)
            r=int(radius)
            
            if (x>50 and x<250 and y<300 and y>100):
                cymbol.play()
            if (x>200 and x<400 and y<650 and y>450):
                snare.play()
            if (x>550 and x<750 and y<650 and y>450):
                bassdrum.play()
            if (x>900 and x<1100 and y<650 and y>450):
                tomtoms.play()
            if (x>1000 and x<1200 and y<300 and y>100):
                cowbell.play()


    if len(cnts2) > 0:
        c2 = max(cnts2, key=cv2.contourArea)
        ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
        M2 = cv2.moments(c2)
        center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))

        if radius2 > 0:
            cv2.circle(frame, (int(x2), int(y2)), int(radius2),(0, 255, 255), 2)
            cv2.circle(frame, center2, 5, (0, 0, 255), -1)
            x2=int(x2)
            y2=int(y2)
            r2=int(radius2)
           
            if (x2>50 and x2<250 and y2<300 and y2>100):
                cymbol.play()
            if (x2>200 and x2<400 and y2<650 and y2>450):
                snare.play()
            if (x2>550 and x2<750 and y2<650 and y2>450):
                bassdrum.play()
            if (x2>900 and x2<1100 and y2<650 and y2>450):
                tomtoms.play()
            if (x2>1000 and x2<1200 and y2<300 and y2>100):
                cowbell.play()
   
    frame = cv2.flip(frame,1)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
