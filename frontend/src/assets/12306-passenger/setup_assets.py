import os
import re
import requests

# Base URL for 12306 images
BASE_URL = "https://kyfw.12306.cn/otn/resources/images/center/"

# Files to download
FILES = [
    "not.png",
    "to.png",
    "to4.png",
    "user-check.png",
    "user-check-success.png",
    "user-check-error.png",
    "mobile-check-success.png",
    "mobile-check-error.png",
    "ytb.png",
    "ytp.png",
    "qxps.png",
    "qxzf.png",
    "zfcg.png",
    "ykp.png",
    "dkp.png",
    "to2.png",
    "to3.png",
    "bg01.png"
]

def download_file(filename):
    url = BASE_URL + filename
    print(f"Downloading {filename} from {url}...")
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
            print(f"Saved {filename}")
        else:
            print(f"Failed to download {filename}: {r.status_code}")
            # Try checking if it exists with a different extension or path if needed
            # But for now just report failure
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

def fix_css():
    css_file = "center.css"
    if not os.path.exists(css_file):
        print(f"{css_file} not found!")
        return

    print(f"Fixing {css_file}...")
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace ../images/center/ with ./
    new_content = content.replace('../images/center/', './')
    
    # Also replace @2x references if we don't download them, but let's keep them pointing to ./ just in case
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {css_file}")

if __name__ == "__main__":
    # Download images
    for f in FILES:
        download_file(f)
    
    # Fix CSS
    fix_css()
