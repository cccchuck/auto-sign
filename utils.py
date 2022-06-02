from urllib.parse import urlencode
from typing import Dict

import time
import requests
import json
import hashlib


def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def sendMsg(content: str):
    URL = 'https://open.feishu.cn/open-apis/bot/v2/hook/935f3e40-9063-42c7-b4b6-0378a8ac3341'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    requests.post(URL, headers=headers, data=json.dumps(data))


class Log:
    def __init__(self, filePath="log/log.log"):
        self.filePath = filePath
        self.content = ''

    def log(self, content):
        res = f'[{ getTime() }] | { content }\n'
        self.content += res
        print(res)

    def save(self):
        with open(self.filePath, 'a') as f:
            f.write(self.content)
            self.content = ''


class InSchool:
    def __init__(self, account: Dict, log: Log):
        self.session = requests.session()

        self.headers = {
            'Host': 'gw.wozaixiaoyuan.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }

        self.log = log

        self.account = account

        self.username = account.get('username')

        self.password = account.get('password')

        self.JWSESSION = account.get('JWSESSION')

        if not self.JWSESSION:
            self.login()
        else:
            self.work()

        return

    def getJwsession(self):
        return self.JWSESSION

    def getUsername(self):
        return self.username[:3] + '****' + self.username[-4:]

    def login(self):
        self.log.log(f'username: { self.getUsername() } logging in...')
        self.headers['Host'] = 'gw.wozaixiaoyuan.com'

        URL = f'https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username?username={ self.username }&password={ self.password }'
        res = self.session.post(URL, headers=self.headers)
        if res.status_code == 200:
            if json.loads(res.text).get('code') == 0:
                self.log.log(f'username: { self.getUsername() } login success')
                self.JWSESSION = res.headers['JWSESSION']
                self.work()
            else:
                self.log.log(f'username: { self.getUsername() } login failed')
        else:
            self.log.log(f'username: { self.getUsername() } request failed')

    def signIn(self):
        self.headers['Content-Type'] = 'application/json'
        self.headers['JWSESSION'] = self.JWSESSION
        self.headers['Host'] = 'student.wozaixiaoyuan.com'

        URL = 'https://student.wozaixiaoyuan.com/sign/doSign.json'

        data = {
            'id': self.account.get('id'),
            'signId': self.account.get('signId'),
            'latitude': self.account.get('latitude'),
            'longitude': self.account.get('longitude'),
            'country': self.account.get('country'),
            'province': self.account.get('province'),
            'city': self.account.get('city'),
            'district': self.account.get('district'),
            'township': self.account.get('township'),
        }

        res = self.session.post(URL, headers=self.headers, json=data)

        self.handle(res, 'Sign In')

        return None

    def signHealth(self):
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['JWSESSION'] = self.JWSESSION
        self.headers['Host'] = 'student.wozaixiaoyuan.com'

        URL = 'https://student.wozaixiaoyuan.com/health/save.json'

        timestamp = int(round(time.time() * 1000))

        data = {
            "answers": self.account.get('answers'),
            "latitude": self.account.get('latitude'),
            "longitude": self.account.get('longitude'),
            "country": self.account.get('country'),
            "province": self.account.get('province'),
            "city": self.account.get('city'),
            "district": self.account.get('district'),
            "township": self.account.get('township'),
            "street": self.account.get('street'),
            "areacode": self.account.get('areacode'),
            "towncode": self.account.get('towncode'),
            "citycode": self.account.get('citycode'),
            "timestampHeader": timestamp,
            "signatureHeader": hashlib.sha256(f'{ self.account.get("province") }_{ timestamp }_{ self.account.get("city") }'.encode('utf-8')).hexdigest()
        }

        data = urlencode(data)

        res = self.session.post(URL, headers=self.headers, data=data)

        self.handle(res, 'Sign Health')

        return None

    def handle(self, res, type):
        if res.status_code == 200:
            code = json.loads(res.text).get('code')
            if code == 0:
                self.log.log(
                    f'username: { self.getUsername() } { type } Success')
                sendMsg(f'username: { self.getUsername() } { type } Success')
            else:
                if code == -10:
                    self.log.log('Log in expired')
                    if type == 'Sign In':
                        self.signIn()
                    elif type == 'Sign Health':
                        self.signHealth()
                elif code == 1:
                    self.log.log(f'{ type } end')
                else:
                    raise Exception(
                        f'username: { self.getUsername() } { type } failed')
        else:
            raise Exception(f'username: { self.getUsername() } request failed')
        return None

    def work(self):
        self.log.log(f'username: { self.getUsername() } working...')
        try:
            self.signIn()
            self.signHealth()
        except Exception as e:
            self.log.log(e.args[0])
        return None


def invoke(accounts):
    for account in accounts:
        inschool = InSchool(account)
        JWSESSION = inschool.getJwsession()
        if JWSESSION:
            account['JWSESSION'] = JWSESSION

    return accounts
