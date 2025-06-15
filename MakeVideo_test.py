import cv2
import os

# 设置参数
image_folder = '\Pull'  # 图片文件夹路径
output_video = '\Make\output.mp4'  # 输出视频文件名
frame_size = (825, 739)  # 视频分辨率
fps = 60  # 帧率
frames_per_image = 2  # 每张图使用的帧数

# 获取并排序图片列表
images = [img for img in os.listdir(image_folder)
           if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
images.sort()  # 可根据需要自定义排序规则

# 创建视频写入对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, frame_size)

# 逐张图片写入视频
for image_name in images:
    img_path = os.path.join(image_folder, image_name)
    img = cv2.imread(img_path)
    if img is None:
        print(f"跳过无法读取的图片: {image_name}")
        continue

    resized_img = cv2.resize(img, frame_size)
    for _ in range(frames_per_image):
        out.write(resized_img)

out.release()
print(f"视频已保存为 {output_video}")
