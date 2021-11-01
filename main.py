import sys
import json
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
import requests
import urllib.request

form_class = uic.loadUiType('uiTest.ui')[0]

def checking_lan(txt):
    client_id = "uhE6Ud51JTtzOTdFUFic"
    client_secret = "GgVrJGawWH"
    encQuery = urllib.parse.quote(txt)  # 문자 입력
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        send_data = response.read()
        dict = json.loads(send_data)
        return dict['langCode']

    else:
        print("Error Code:" + rescode)

def get_translate(text, fromlang):
    tolang='ko'
    if(fromlang=='ko'):
        tolang='en'
    client_id = "uhE6Ud51JTtzOTdFUFic" # <-- client_id 기입
    client_secret = "GgVrJGawWH" # <-- client_secret 기입

    data = {'text': text,
            'source': fromlang,
            'target': tolang}

    url = "https://openapi.naver.com/v1/papago/n2mt"

    header = {"X-Naver-Client-Id":client_id,
              "X-Naver-Client-Secret":client_secret}

    response = requests.post(url, headers=header, data=data)
    rescode = response.status_code

    if(rescode==200):
        send_data = response.json()
        trans_data = (send_data['message']['result']['translatedText'])
        return trans_data
    else:
        print("Error Code:" , rescode)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Btn.clicked.connect(self.btn_clicked)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def btn_clicked(self):
        txt = self.inP.toPlainText()
        lang=checking_lan(txt)

        self.outP.setText(get_translate(txt, lang))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
