import os
import requests
from datetime import datetime, timedelta, timezone
import time


os.makedirs('/Pull', exist_ok=True)
#------------^^^^^^----------------
#-------在这里修改储存路径----------
while True:
    utc_now = datetime.now(timezone.utc) - timedelta(minutes=18)
    year = utc_now.strftime("%Y")
    month = utc_now.strftime("%m")
    day = utc_now.strftime("%d")
    time_str = utc_now.strftime("%Y%m%d%H%M00")
    url = f"http://image.nmc.cn/product/{year}/{month}/{day}/RDCP/medium/SEVP_AOC_RDCP_SLDAS3_ECREF_ACHN_L88_PI_{time_str}000.PNG"
    local_now = utc_now + timedelta(hours=8)
    print(f"Downloading from URL: {url}")

    response = requests.get(url)
    if response.status_code == 200:
        filename = f"/Pull/{local_now.strftime('%Y%m%d%H%M%S')}.PNG"
#--------------------------^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^------------这里可以改文件名称策略        
        try:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"图片保存成功！文件名: {filename}")
        except Exception as e:
            print(f"保存文件时出错: {e}")
    else:
        print("下载失败，有可能是当前未更新图片，属于正常情况，如果超过10分钟为正常获取图片，请进行进一步检查！状态码:", response.status_code)

    time.sleep(60)
