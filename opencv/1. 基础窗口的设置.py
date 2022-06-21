import cv2

cv2.namedWindow('news', cv2.WINDOW_AUTOSIZE)
img = cv2.imread(r'H:\slideVerify\1.jpg',)
cv2.resizeWindow('news',640,680)

while True: # 解决 按其他键会自动停止
    cv2.imshow('news', img)
    key = cv2.waitKey(0)

    if(key & 0xFF == ord('q')):
        # exit()
        break
    elif key == ord('q'):
        cv2.imwrite(r'H:\slideVerify\11.jpg', img)
    else:
        print(key)
cv2.destroyAllWindows()