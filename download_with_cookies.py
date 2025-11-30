import requests
import os

cookies = {
    'JSESSIONID': '0C4B412A8F9441B90A4AD4EABC976ADB',
    'tk': '1UdKhYQ0sWN_S3LKGwiGQYDl2-Pfjin0YnBFPgqrw1w0',
    '_jc_save_fromStation': '%u5317%u4EAC%2CBJP',
    '_jc_save_toStation': '%u4E0A%u6D77%2CSHH',
    '_jc_save_fromDate': '2025-11-02',
    '_jc_save_toDate': '2025-11-02',
    '_jc_save_wfdc_flag': 'dc',
    'guidesStatus': 'off',
    'BIGipServerotn': '1708720394.64545.0000',
    'BIGipServerpassport': '937951498.50215.0000',
    'highContrastMode': 'defaltMode',
    'cursorStatus': 'off',
    'route': '495c805987d0f5c8c84b14f60212447d',
    'uKey': '9a0f9d9b52df881d6884dace0f2f233e6f4b6606c106c55323fd7e4fd4cebc24'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download_image(url, filename):
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename} ({len(response.content)} bytes)")
        else:
            print(f"Failed to download {filename}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

os.makedirs('frontend/src/assets/12306-icons', exist_ok=True)

# Download noticepic.png (just in case)
download_image('https://kyfw.12306.cn/otn/images/center/noticepic.png', 'frontend/src/assets/12306-icons/noticepic.png')

# Download QR codes
download_image('https://kyfw.12306.cn/otn/index/requestWechatQr?w=mypage', 'frontend/src/assets/12306-icons/wechat-qr.png')
download_image('https://kyfw.12306.cn/otn/index/requestAliQr?w=mypage', 'frontend/src/assets/12306-icons/alipay-qr.png')
