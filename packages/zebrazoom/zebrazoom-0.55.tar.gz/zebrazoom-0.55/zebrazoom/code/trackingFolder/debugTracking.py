import cv2
import math

def debugTracking(nbTailPoints, i, firstFrame, output, outputHeading, frame2, hyperparameters):
  if hyperparameters["debugTracking"]:
    frame2 = cv2.cvtColor(frame2,cv2.COLOR_GRAY2RGB)
    for k in range(0, hyperparameters["nbAnimalsPerWell"]):
      for j in range(0, nbTailPoints):
        x = int(output[k, i-firstFrame][j][0])
        y = int(output[k, i-firstFrame][j][1])
        cv2.circle(frame2, (x, y), 1, (0, 255, 0),   -1)
      x = int(output[k, i-firstFrame][nbTailPoints-1][0]) # it used to be 10 instead of 9 here, not sure why
      y = int(output[k, i-firstFrame][nbTailPoints-1][1]) # it used to be 10 instead of 9 here, not sure why
      cv2.circle(frame2, (x, y), 2, (0, 0, 255),   -1)
      
      x = output[k, i-firstFrame][0][0]
      y = output[k, i-firstFrame][0][1]
      cv2.line(frame2,(int(x),int(y)),(int(x+20*math.cos(outputHeading[k, i-firstFrame])),int(y+20*math.sin(outputHeading[k, i-firstFrame]))), (255,0,0), 3)
    
    if hyperparameters["debugTrackingPtExtremeLargeVerticals"]: # Put this to True for large resolution videos (to be able to see on your screen what's happening)
      frame2 = frame2[int(y-200):len(frame2), :]
    
    cv2.imshow('Frame', frame2)
    cv2.waitKey(0)