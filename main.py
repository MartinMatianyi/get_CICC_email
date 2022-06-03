from time import strftime, gmtime, sleep
import pytesseract
import re
from PIL import Image
import os
import socket
import socks
import requests
import random
from urllib.request import urlretrieve
from os.path import exists

# 所有的请求都走 tor
socks.set_default_proxy(proxy_type=socks.SOCKS5, addr="127.0.0.1", port=9050)
socket.socket = socks.socksocket
IMAGE_URL_Start = "https://secure.college-ic.ca/default/search/generate-email-image?nocache="
IMAGE_URL_Mid = "&lang=en&form_id="
IMAGE_URL_End = "&token="
log = open(r".\report\log.txt", "r")
start = 0
end = 0


def img_download(start, end):
    os.makedirs('./image/', exist_ok=True)
    for x in range(start, end + 1):
        if not exists('./image/img' + str(x) + '.png'):
            urlretrieve(IMAGE_URL_Start + str(random.randint(1, 999)) + IMAGE_URL_Mid + str(x) + IMAGE_URL_End,
                        './image/img' + str(x) + '.png')
            print("Downloading img:" + str(x - start + 1) + "/" + str(end - start + 1))
            sleep(1)
            if x % 10 == 0:
                resp = requests.get('http://api.ipify.org/').text
                print("Current IP: " + resp)


def img_translate(start, end, log):
    f = open(r".\report\\" + str(start) + "-" + str(end) + ".txt", "w")
    pytesseract.pytesseract.tesseract_cmd = r'E:\ORC\tesseract.exe'
    string = ''
    emails = []
    i = 0
    empty = True
    for x in range(start, end + 1):
        im = Image.open('.\\image\\img' + str(x) + '.png')
        string = pytesseract.image_to_string(im)
        for email in re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+)", string):
            emails.append(email)
            print("Reading img:" + str(x - start + 1) + "/" + str(end - start + 1))
            empty = False
    if empty:
        print("No email in range " + str(start) + " to " + str(end))
    for mail in emails:
        f.write(mail + "\n")
    log.close()
    new_log = open(r".\report\log.txt", "w")
    new_log.write("You end at " + str(end) + " on " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) +
                  ".\nYou can start from " + str(end + 1) + " if you want to continue.")
    new_log.close()
    f.close()


def print_info():
    print(log.read())
    global start
    global end
    start = int(input("Start:"))
    end = int(input("End:"))
    print("Getting email from website, id from " + str(start) + " to " + str(end) + ". Out put file: " + str(
        start) + "-" + str(end) + ".txt")


print_info()
img_download(start, end)
img_translate(start, end, log)
