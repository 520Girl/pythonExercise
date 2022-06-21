import cv2
from cv2 import waitKey
# 创建窗口
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', 640, 480)
#! 获取到视频设备
# cap = cv2.VideoCapture(0)

#! 通过多媒体文件中读取视频帧
cap = cv2.VideoCapture(r"C:\Users\Gratefuls\Desktop\天府绿道\VID_20220203_154953.mp4")
#读取视频帧
while True:
    # 从摄像头读视频帧
    ret, frame = cap.read() 
    # 将视频帧在窗口显示，没读一帧就在相同窗口video中显示 
    cv2.imshow('video', frame)

    key = cv2.waitKey(30) # 10ms  也就是1000 / 帧 = ？
    if key & 0xFF == ord('q'):
        break

# 释放 videoCapture
cap.release()
cv2.destroyAllWindows()