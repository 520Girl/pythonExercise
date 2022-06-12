import cv2

#! 第一次测试,对模板进行模糊定位
def test_one():
    # 底图地址
    img_path = r"H:\slideVerify\2.jpg"
    img_path4 = r"H:\slideVerify\2n.jpg"
    # 移动块地址
    tm_path = r"H:\slideVerify\2d.png"
    #导入图片
    img_rgb = cv2.imread(img_path, 1)
    template_rgb = cv2.imread(tm_path, 1)
    # 图片灰度化 ,进行图像阀值处理变为黑色背景
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    tm_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)
    tm_gray = cv2.GaussianBlur(tm_gray, (3, 3), 0)
    img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 20)
    tm_thresh = cv2.adaptiveThreshold(tm_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 20)
    # cv2.imshow('ping', img_thresh)
    # cv2.waitKey(0)
    # 进行边缘检查，范围调到较大保留更多的边缘，检测图像的边缘，比如缺口边缘等，返回图片

    img_canny  = cv2.Canny(img_thresh, 100, 500)
    tm_canny = cv2.Canny(tm_thresh, 100, 500)
    cv2.imshow('ping', tm_canny)
    cv2.waitKey(0)
    # 模板匹配一化系数匹配法 TM_CCOEFF_NORMED在用minMaxLoc方法求出最大值，和最小值，以及他们的坐标
    # 将图片和缺口图片进行匹配, 用最小min_loc[0] 减去 max_loc[0] 就是缺口图间距
    res = cv2.matchTemplate(img_canny, tm_canny, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 计算矩形坐标
    h, w = tm_gray.shape[:2]
    w_start_index, h_start_index = 0, 0
    w_end_index, h_end_index = w, h
    # print(w_start_index, w_end_index)
    # print(h_start_index,h_end_index)
    # print(min_val, max_val, min_loc, max_loc)
    # print(f"({w_start_index},{w_end_index})")

    # 画正方形 ,right_bottom计算右下角坐标，画绿色正方形，保存图片地址img_path4， 被画的图片img_rgb
    # cv2.rectangle(img_rgb, f"({int(w_start_index)},{int(w_end_index)})", f"({int(h_start_index)},{int(h_end_index)})", (0, 255, 0), 2)
    right_bottom = (max_loc[0] + w, max_loc[1] + h)
    img_transparent_space = min_loc[0] - max_loc[0]
    cv2.rectangle(img_rgb, min_loc, (right_bottom[0]-img_transparent_space,right_bottom[1]-img_transparent_space,), (0, 255, 0), 2)
    cv2.imwrite(img_path4, img_rgb)

    #查看灰度化后的图片
    # cv2.imshow('ping', img_canny)
    # cv2.waitKey(0)

#! 加强经度，去除缺口图片的背景
def template_matching(img_path,tm_path):
    # 导入图片，灰度化
    img_rgb = cv2.imread(img_path)
    template_rgb = cv2.imread(tm_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    tm_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
    # 缺口图去除背景
    h, w = tm_gray.shape #  缺口图片的宽高
    print(h,w)
    
    w_start_index, h_start_index = 0, 0
    w_end_index, h_end_index = w, h
    # 缺口图去除背景
    # 算出高起始位置

    for i in range(h):
        if not any(tm_gray[i, :]):
            h_start_index = i
        else:
            break
	# 算出高的结束位置
    for i in range(h - 1, 0, -1):
        if not any(tm_gray[i, :]):
            h_end_index = i
        else:
            break
	# 算出宽的起始位置
    for i in range(w):
        if not any(tm_gray[:, i]):
            w_start_index = i
        else:
            break
	# 算出宽的起始位置
    for i in range(w - 1, 0, -1):
        if not any(tm_gray[:, i]):
            w_end_index = i
        else:
            break
    # 取出完整的缺口图
    tm_gray= tm_gray[h_start_index:h_end_index - 21, w_start_index:w_end_index - 21]

    # 自适应阈值话
    img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 20)
    tm_thresh = cv2.adaptiveThreshold(tm_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 20)

    # 边缘检测
    img_canny = cv2.Canny(img_thresh, 0, 500)
    tm_canny = cv2.Canny(tm_thresh, 0, 500)
    # cv2.imshow("img_canny", img_canny)
    # cv2.imshow("tm_canny", tm_canny)
    h, w = tm_gray.shape[:2]
    print(tm_gray.shape)
    print(h, w)
    # 模板匹配
    res = cv2.matchTemplate(img_canny, tm_canny, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_loc)
    print(min_val, max_val, min_loc, max_loc)
    right_bottom = (max_loc[0] + w, max_loc[1] + h)   # 右下角
	# 圈出矩形坐标
    cv2.rectangle(img_rgb, (499,115), right_bottom, (0, 0, 255), 2)

    # 保存处理后的图片
    cv2.imwrite(r"H:\slideVerify\5.jpg", img_rgb)

#! 最后版本，
def get_template_distance(img_path, tm_path): #img_path 为图片地址， tm_path 为缺口图片地址
    #todo 1. 导入图片，进行灰度化处理，高斯模糊去燥点，设置阀值将背景加上黑色底色
    #? 1.1导入图片
    img_rgb = cv2.imread(img_path)
    template_rgb = fix_img(tm_path)

    #? 1.2 灰度化处理
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    tm_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
    

    #? 1.3 高斯模糊去燥点
    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)
    tm_gray = cv2.GaussianBlur(tm_gray, (3, 3), 0)
    

    #? 1.4 设置阀值将背景加上黑色底色
    img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0)
    tm_thresh = cv2.adaptiveThreshold(tm_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0)

    #todo 2. 使用cany算法进行边缘化检查，
    img_canny  = cv2.Canny(img_thresh, 100, 500)
    tm_canny = cv2.Canny(tm_thresh, 100, 500)


    #todo 3. 模板匹配一化系数匹配法，将图片和缺口图进行匹配 TM_CCOEFF_NORMED在用minMaxLoc方法求出最大值，和最小值，以及他们的坐标
    #todo 3. 将图片和缺口图片进行匹配, 用最小min_loc[0] 减去 max_loc[0] 就是缺口图间距
    res = cv2.matchTemplate(img_canny, tm_canny, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_loc, max_loc)

    #todo 4. 计算矩形的宽高 将元祖转int
    h, w = tm_gray.shape[:2]
    w_start_index, h_start_index = 0, 0
    w_end_index, h_end_index = w, h

    #todo 5. 画正方形 最小值得第一源 -  减去最大值得第一个元素得到的就是 缺口图片的透明间距
    right_bottom = (max_loc[0] + w, max_loc[1] + h)
    img_transparent_space = max_loc[1] - max_loc[1]
    cv2.rectangle(img_rgb, max_loc, right_bottom, (0, 255, 0), 2)
    cv2.imwrite(r"H:\slideVerify\9.jpg", img_rgb)

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

def main():
    # template_matching(r"H:\slideVerify\1.jpg",r"H:\slideVerify\1d.png")
    # test_one()
    get_template_distance(r"H:\slideVerify\1.jpg",r"H:\slideVerify\1d.png")

if __name__ == "__main__":
    main()