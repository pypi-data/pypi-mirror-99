# coding=utf-8
import json
import os
import sys
import time

from pydub import AudioSegment

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

global API_KEY
global SECRET_KEY

API_KEY = '4E1BG9lTnlSeIf1NQFlrSq6h'
SECRET_KEY = '544ca4657ba8002e3dea3ac2f5fdd241'


def setup(api_key, secret_key):
    global API_KEY
    global SECRET_KEY
    API_KEY = api_key
    SECRET_KEY = secret_key


# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
global PER
PER = 5
# 语速，取值0-15，默认为5中语速
global SPD
SPD = 5
# 音调，取值0-15，默认为5中语调
global PIT
PIT = 5
# 音量，取值0-9，默认为5中音量
global VOL
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 3

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

# TTS_URL = 'http://tsn.baidu.com/text2audio'
TTS_URL = 'http://tsn.baidu.com/text2audio'  # baidu精品语音


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    print("fetch token begin")
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """

"""
    单例获取
"""


def aiGet(text, result_name='result'):
    token = fetch_token()

    # design
    print(text)
    TEXT = text

    tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
    print(tex)
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)
    print('test on Web Browser' + TTS_URL + '?' + data)

    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else result_name + '.' + FORMAT
    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        if (IS_PY3):
            result_str = str(result_str, 'utf-8')
        print("tts api  error:" + result_str)

    print("result saved as :" + save_file)


"""
    获取语音文件
    @param TEXT {String}
    @return sound {.mp3}
"""


def getOne(text, result_name='out/result'):
    aiGet(text=text, result_name=result_name)


def getByList(text_list):
    i = 0
    for item in text_list:
        aiGet(text=item, result_name='out/autoSave' + str(i))
        i += 1
        time.sleep(0.5)


def getByObj(obj_list):
    for (text, path) in obj_list:
        if path[0, 3] != 'out/':
            aiGet(text=text, result_name='out/' + path)
        else:
            aiGet(text=text, result_name=path)


"""
    音频处理
"""


def mixSound(file1, file2):
    music1 = AudioSegment.from_mp3(file1 + '.mp3')
    music2 = AudioSegment.from_mp3(file2 + '.mp3')
    output = music1.overlay(music2)
    print('mixed : ' + file1 + ' + ' + file2)
    return output


def createBaseFile():
    aiGet(text='', result_name='out/base')


def createInList(fileList):
    if not os.path.exists('out/base.mp3'):
        createBaseFile()
    output_music = AudioSegment.from_mp3('out/base.mp3')
    for item in fileList:
        output_music += AudioSegment.from_mp3('out/' + item + '.mp3')
        print(item + '.mp3 has been added.')
    return output_music


def makeExportFile(musicFile, out_name="default"):
    musicFile.export("export/" + out_name + ".mp3", format="mp3")
    print('make package is success! please check in fold export/' + out_name + '.mp3')


def dirMake(dir_name):
    if dir_name(len(dir_name)-1) != '/':
        dir_name += ''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def autoMake(text_list, out_name='export_default', who_read='auto'):
    # 获取转义音频文件
    getByList(text_list=text_list)
    music_file = []
    # dirMake('out')
    # 谁来读
    who_in_list = False
    global PER
    # 检测传入 为 auto 或 list
    if type(who_read) == str:
        if who_read != 'auto':
            PER = int(who_read)
    elif type(who_read) == list:
        who_in_list = True
        # 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
        # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
        # 补全未定义
        # for i in range(len(text_list) - len(who_read)):
        #     who_read += '0'
    for i in range(len(text_list)):
        if who_in_list:
            PER = who_read[i]
        _c = 'autoSave' + str(i)
        music_file.insert(i, _c)
    print(music_file)
    export_file = createInList(music_file)
    makeExportFile(export_file, out_name=out_name)
