import os
from uuid import uuid4
from aip import AipSpeech
from aip import AipNlp
import settings

APP_ID = '20419334'
API_KEY = 'S3bDjNXGxDNpsOeMkcxmimBp'
SECRET_KEY = 'TZyEbYv8lVTd9XR3Lz34w27POd7wwnii'
""" 你的 APPID AK SK """
# APP_ID = '20004294'
# API_KEY = 'gU87iYzV7RzI6DXXgQOb2hXW'
# SECRET_KEY = 'Ace8f3zbRhPZjTfBLoq6STSo87jT5QKB'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 音频转为文本
def audio2text(file_name):
    file_path = os.path.join(settings.AUDIO_PCM_DIR, file_name)
    cmd_str = f'ffmpeg -y -i {file_path} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {file_path}.pcm'
    os.system(cmd_str)
    with open(f'{file_path}.pcm', 'rb') as f:
        audio_context = f.read()
    res = client.asr(audio_context, 'pcm', 16000, {
        "dev_pid": 1537
    })
    print("res",res)
    if res.get('err_no'):
        return res
    return res.get('result')[0]

# 文本转为音频
def text2audio(text):
    file_name = f"{uuid4()}.mp3"
    file_path = os.path.join(settings.AUDIO_PCM_DIR, file_name)
    res = client.synthesis(text, 'zh', 1, {
        "vol": 5,
        'pit': 7,
        "spd": 4,
        "per": 4
    })
    if isinstance(res, dict):
        return res
    with open(file_path, 'wb') as f:
        f.write(res)
    return file_name

# 词法的匹配分析


