

import sys
import os
import time
import Image
from aip import AipOcr
import webbrowser
sys.path.append("libs")

url = 'https://www.baidu.com/s?wd='

# from urllib import request
PATH = lambda p: os.path.abspath(p)

# 以下三个KEY请替换成你自己的
APP_ID = '********'
API_KEY = '********'
SECRET_KEY = '********'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
def screenshot():
    path = PATH(os.getcwd() + "/screenshot")
    timestamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    os.popen("adb wait-for-device")
    os.popen("adb shell screencap -p /data/local/tmp/tmp.jpeg")
    if not os.path.isdir(PATH(os.getcwd() + "/screenshot")):
        os.makedirs(path)
    os.popen("adb pull /data/local/tmp/tmp.jpeg " + PATH(path + "/" + timestamp + ".jpeg"))
    os.popen("adb shell rm /data/local/tmp/tmp.jpeg")
    # print ("success")
    # print(PATH(path + "/" + timestamp + ".png"))
    im = Image.open(PATH(path + "/" + timestamp + ".jpeg"))
    # im = Image.open(PATH(path + "/test" + ".jpg"))
    box = (30, 200, 680, 400)
    im = im.crop(box)
    im.save(PATH(path + "/" + timestamp + "dd.jpeg"), "jpeg")
    image = get_file_content(PATH(path + "/" + timestamp + "dd.jpeg"))
    words_result = client.basicAccurate(image)["words_result"]
    results = ""
    for index,wordstemp in enumerate(words_result):
        if index == 0:
            results = results + wordstemp["words"][2:]
        else:
            results = results + wordstemp["words"]
    webbrowser.open(url + results)
    print results;

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

if __name__ == "__main__":
    screenshot()