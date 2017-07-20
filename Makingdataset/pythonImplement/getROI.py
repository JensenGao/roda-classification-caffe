# -*- coding: utf-8 -*-

import numpy as np
import cv2

frameCount=0#帧计数
ROIWidth=150#数据的宽
ROIHeight=150#数据的高
gap=100#每隔gap个像素进行采集
i=0#命名用的
j=0

videoCapture=cv2.VideoCapture("C:/Users/lenovo/Desktop/Road Classification/[]Bayes Technology's Video/DJI_0019.MOV")
if videoCapture.isOpened()==0:
    print "Failed to open video!"

while True:
    ret,frame=videoCapture.read()#读取视频帧
       
    frameWidth=int(videoCapture.get(3))#帧的宽
    frameHeight=int(videoCapture.get(4))#帧的高
    print "Video's Width :{0}\nVideo's Height:{1}".format(frameWidth,frameHeight)
    
    resultWidth=frameWidth-ROIWidth+1#列的循环
    resultHeight=frameHeight-ROIHeight+1#行的循环
    
    if frameCount%30==0:#每隔30帧采集一次
        for row in xrange(0,resultHeight,gap):#行循环
            for col in xrange(0,resultWidth,gap):#列循环
                
                ROIImage=frame[col:col+ROIWidth,row:row+ROIHeight]#ROI抠图
                imageName="%s%d%s%d%s%d%s"%(
                "C:/Users/lenovo/Desktop/raod/1/",
                 frameCount,'_',i,'_',j,'.jpg')#将后面的路径写到变量里
                
                cv2.imwrite(imageName,ROIImage)#保存图像
    
            i+=1
        j+=1
                
    cv2.namedWindow('videoFrame')
    cv2.imshow('videoFrame',frame)
    
    frameCount+=1#保存下一帧
    print "Frames:{0}\n\n".format(frameCount)
    
    k=cv2.waitKey(33)
    if k==27 or k==ord('Q') or k==ord('q'):#退出播放视频
        break

videoCapture.release()#释放
cv2.destoryAllWindows()#回收窗口
