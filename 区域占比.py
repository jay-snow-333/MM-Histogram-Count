import cv2
import numpy as np


# 定义鼠标点击事件的回调函数
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        # 获取指定像素点的颜色值
        bgr_color = image[y, x]
        # 转换为HSV颜色空间
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)
        # 打印颜色值
        print(f"点击位置({x}, {y})的颜色值：{hsv_color[0][0]}")
        # 根据点击位置获取颜色范围
        lower_blue = np.array([hsv_color[0][0][0] - 10, hsv_color[0][0][1] - 50, hsv_color[0][0][2] - 50])
        upper_blue = np.array([hsv_color[0][0][0] + 10, hsv_color[0][0][1] + 50, hsv_color[0][0][2] + 50])

        # 根据颜色范围提取蓝色区域
        blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

        # 计算蓝色像素占整张图的比例
        total_pixels = blue_mask.shape[0] * blue_mask.shape[1]
        blue_pixels = np.count_nonzero(blue_mask)
        blue_ratio = blue_pixels / total_pixels

        # 提取蓝色区域的颜色值
        blue_masked_image = cv2.bitwise_and(image, image, mask=blue_mask)
        blue_mean_color = cv2.mean(blue_masked_image, mask=blue_mask)[:3]

        print(f"蓝色像素占整张图的比例：{blue_ratio:.4f}")
        print(f"蓝色颜色值：{blue_mean_color}")

        # 根据颜色范围提取蓝色区域
        blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

        # 取反蓝色区域的掩码，得到背景区域的掩码
        background_mask = cv2.bitwise_not(blue_mask)

        # 将蓝色区域的像素替换成红色
        result = image.copy()
        result[np.where(blue_mask)] = [0, 0, 255]

        # 将背景区域与原始图像进行按位与操作，保持背景不变
        background = cv2.bitwise_and(image, image, mask=background_mask)

        # 将替换后的图像和背景区域进行按位或操作，得到最终结果
        result = cv2.bitwise_or(result, background)

        # 显示图像
        cv2.imshow("result", result)

# 读取彩色图像
image = cv2.imread("26-2.tif")

# 将图像转换为HSV颜色空间
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 显示图像并设置鼠标点击事件的回调函数
cv2.imshow("image", image)
cv2.setMouseCallback("image", mouse_callback)

# 等待按下任意键退出程序
cv2.waitKey(0)
cv2.destroyAllWindows()
