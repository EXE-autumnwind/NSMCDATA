import os
import imageio.v2 as imageio
import numpy as np
from PIL import Image
from tqdm import tqdm

root_folder = r'D:\气象云图' #图片文件夹
output_video = r'D:\气象云图\视频输出\output.mp4'#输出文件夹
frame_size = (825, 739) #分辨率
fps = 60 #帧率
frames_per_image = 2

os.makedirs(os.path.dirname(output_video), exist_ok=True)

def get_all_images_with_timestamp(root):
    image_list = []
    for root_dir, dirs, files in os.walk(root):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename = os.path.splitext(file)[0]
                timestamp = ''.join(filter(str.isdigit, filename))
                if len(timestamp) == 4:
                    full_path = os.path.join(root_dir, file)
                    image_list.append((timestamp, full_path))
    return image_list

def sort_images(image_list):
    def parse_date_from_path(path):
        parts = path.split(os.sep)
        year = 0
        month = 0
        day = 0
        for part in parts:
            if part.endswith('年') and part[:-1].isdigit():
                year = int(part[:-1])
            elif part.endswith('月') and part[:-1].isdigit():
                month = int(part[:-1])
            elif part.endswith('日') and part[:-1].isdigit():
                day = int(part[:-1])
        hhmm = int([t for t, p in image_list if p == path][0]) if any(p == path for t, p in image_list) else 0
        return (year, month, day, hhmm)
    return sorted(image_list, key=lambda x: parse_date_from_path(x[1]))

image_list = get_all_images_with_timestamp(root_folder)
if not image_list:
    print("未找到任何有效图片文件！")
    exit()

sorted_images = [img_path for (timestamp, img_path) in sort_images(image_list)]
total_frames = len(sorted_images) * frames_per_image

try:
    writer = imageio.get_writer(
        output_video,
        fps=fps,
        format='mp4',
        codec='libx264'
    )

    with tqdm(total=len(sorted_images), desc="处理图片") as pbar_img:
        with tqdm(total=total_frames, desc="生成视频帧") as pbar_frame:
            for img_path in sorted_images:
                try:
                    with Image.open(img_path) as img:
                        img_resized = img.resize(frame_size, Image.Resampling.LANCZOS)
                        img_np = np.array(img_resized)
                        for _ in range(frames_per_image):
                            writer.append_data(img_np)
                            pbar_frame.update(1)
                    pbar_img.update(1)
                except Exception as e:
                    print(f"\n处理 {os.path.basename(img_path)} 失败: {e}")
                    pbar_img.update(1)
                    continue

    writer.close()
    print(f"\n视频已成功保存至: {output_video}")

except Exception as e:
    print(f"\n视频生成失败: {e}")
    print("请确保已安装依赖：pip install imageio[ffmpeg] pillow numpy tqdm")
