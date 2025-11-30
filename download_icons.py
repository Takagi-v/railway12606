import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download_image(url, filename):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

os.makedirs('frontend/src/assets/12306-icons', exist_ok=True)
download_image('https://kyfw.12306.cn/otn/images/center/noticepic.png', 'frontend/src/assets/12306-icons/noticepic.png')
download_image('https://kyfw.12306.cn/otn/index/requestWechatQr?w=mypage', 'frontend/src/assets/12306-icons/wechat-qr.png')
download_image('https://kyfw.12306.cn/otn/index/requestAliQr?w=mypage', 'frontend/src/assets/12306-icons/alipay-qr.png')
