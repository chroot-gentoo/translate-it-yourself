import requests
import json

URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
KEY = 'trnsl.1.1.20180821T114816Z.2608105dfedb4a3b.f1e2c459514e629e989ea72141c0054ccb4d60bb'


def translate(text, orig_lang='en', target_lang='ru'):
    _request = {'key': KEY, 'text': text, 'lang': f'{orig_lang}-{target_lang}'}
    try:
        translated = requests.post(URL, data=_request)
    except requests.exceptions.ConnectionError:
        res = 'error', 'no connection', 'нет интернет соединения'
    else:
        translation = json.loads(translated.text)
        res = 'info', 'перевод', translation['text'][0]
    return res
