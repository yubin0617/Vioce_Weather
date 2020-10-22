import os
import json
from uuid import uuid4
import time

from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket
from gevent.pywsgi import WSGIServer
from flask import Flask,request,render_template,send_file,g
import baidu_aip
import settings
from Weather import *
app = Flask(__name__)  # type:Flask

# asr_str = ""
@app.route('/getfile/<filename>')
def getfile(filename):
    file_path = os.path.join(settings.AUDIO_PCM_DIR,filename)
    return send_file(file_path)

@app.route('/upload')
def upload():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return '请使用websocket连接'

    while True:
        message = ws.receive()
        if isinstance(message,bytearray):
        # if message:
            print("成功接收音频！")
            print(message)
            file_name = f"{uuid4()}.wav"
            file_path = os.path.join(settings.AUDIO_PCM_DIR,file_name)
            with open(file_path,'wb') as f:
                f.write(message)
            #asr_str==郑州市
            #global  asr_str
            asr_str = baidu_aip.audio2text(file_name)
            # print(asr_str)
            asr_str = Weather(asr_str)

            file_mp3_name = baidu_aip.text2audio(asr_str)
            print(file_mp3_name)
            send_dic = json.dumps({
                "filename":file_mp3_name,
                "play_type":'audio',
                "sendtime":111
            })
            ws.send(send_dic)
        else:
            ws.close()

@app.route('/index')
def index():
    t=time.gmtime()
    #upload()
    #seter = g.asr_str.split("\n")
    return render_template('index.html',data=time.strftime("%Y-%m-%d",t))

@app.route('/info')
def info():
  return tempjson.jsonweather


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1',5000),app,handler_class=WebSocketHandler)
    http_server.serve_forever()
    print(settings.AUDIO_PCM_DIR)
