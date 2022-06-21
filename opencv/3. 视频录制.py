from typing import Tuple
import cv2 

#创建videoWritewei为写入多媒体文件
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
vw = cv2.VideoWriter('./out.mp4',fourcc,25,(1280,720),True)
# 创建窗口
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', 640, 480)
#! 获取到视频设备
cap = cv2.VideoCapture(0)

#读取视频帧, 判断摄像头是否是打开的
while cap.isOpened():
    # 从摄像头读视频帧
    ret, frame = cap.read() 
    if ret == True:
        # 将视频帧在窗口显示，没读一帧就在相同窗口video中显示 
        cv2.imshow('video', frame)
        cv2.resizeWindow('video', 640, 480) #重新设置窗口大小这里是个bug ，会被内容撑大，需妖重新设置一下

        # 写入多媒体文件
        vw.write(frame)
        
        key = cv2.waitKey(30) # 10ms  也就是1000 / 帧 = ？
        if key & 0xFF == ord('q'):
            break
    else:
        break

# 释放 videoCapture
cap.release()
vw.release() #视频videoWrite()
cv2.destroyAllWindows()