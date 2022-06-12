import numpy as np
import cv2
import matplotlib.pyplot as plt


def crop_image_from_gray(img, boundary=7):
    # 转为灰度图
    # 注意, cv2.imread读取的是bgr格式, 而不是rgb

    height, width, channel = img.shape
    for h in range(height):
        for w in range(width):
            color = img[h, w]
            if (color == np.array([71, 112, 76, 0])).all():
                img[h, w] = [255, 255, 255, 255]
                print(1)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray_img)
    gray_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0)
    cv2.imshow('ffff',gray_img)
    cv2.waitKey(0)
    print(gray_img)
    mask = gray_img > boundary
    img1 = img[:, :, 0][np.ix_(mask.any(1), mask.any(0))]
    img2 = img[:, :, 1][np.ix_(mask.any(1), mask.any(0))]
    img3 = img[:, :, 2][np.ix_(mask.any(1), mask.any(0))]
    img = cv2.merge((img1, img2, img3))
    return img


img = cv2.imread(r"H:\slideVerify\1d.png", -1)
cv2.imshow('12',img)
cv2.waitKey(0)
img = crop_image_from_gray(img, 7)
cv2.imwrite(r"H:\slideVerify\10.png", img)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.figure()
plt.imshow(img_rgb)
plt.show()



def fix_img(filename):
    #  1.为了更高的准确率，使用二值图像
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # COLOR_BGR2GRAY:BGR和灰度图的转换
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # 2.将轮廓提取出来【对于二值化图片的物体找轮廓真的挺好用的】
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 轮廓图：用绿色线(0, 255, 0)来画出最小的矩形框架
    contour_img = cv2.drawContours(img, contours, 0, (0, 255, 0), 1)
    cv2.imshow("contour_img.png", contour_img)  # 裁剪出滑块的区域
    cv2.waitKey(0)
    x, y, w, h = cv2.boundingRect(contours[0])  # 以方框标出轮廓的位置
    mixintu = contour_img[y:y + h, x:x + w]  # 截取部分区域图片
    cv2.imshow("mixintu.png", mixintu)  # 裁剪出滑块的区域
    cv2.imwrite(r"H:\slideVerify\500.png", mixintu)
    cv2.waitKey(0)
    return mixintu

print(fix_img(r"H:\slideVerify\10.png"))
