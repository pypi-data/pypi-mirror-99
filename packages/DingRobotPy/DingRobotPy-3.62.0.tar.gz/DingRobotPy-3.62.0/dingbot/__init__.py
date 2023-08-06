# coding=utf-8

__all__     = ['Card', 'DingAPI', 'DingError', 'DingLimit', 'DingManage', 'DingRaise']
__doc__     = 'A SDK for group robots of Dingtalk ( copyright )\nWu Junkai wrote it by python 3.7.7 , run in python 2.7.14, 3.8.1 and 3.8.7\nmore information please view github.com/WuJunkai2004/Dingbot'
__version__ = '3.62.0'

try:
    import urllib2 as _u
    from urllib import quote_plus
except ImportError:
    import urllib.request as _u
    from urllib.parse import quote_plus

import base64
import hashlib
import hmac

import json
import sys
import time

urlopen = _u.urlopen
request = _u.Request
Card = dict

def _http_manage(url, data, headers):
    'Responsible for network access'
    text = urlopen(request(url, data, headers)).read()
    text = text.decode('utf-8') if(sys.version_info.major == 3)else text
    return text

def _http_get(url, headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url, None, headers)

def _http_post(url, data, headers):
    'Inherited from _http_manage and responsible for network get'
    return _http_manage(url, data, headers)

def _signature(webhook, secret, var = sys.version_info.major):
    timestamp          = long(round(time.time() * 1000))        if(var==2)else str(round(time.time() * 1000))
    secret_enc         = bytes(secret).encode('utf-8')          if(var==2)else secret.encode('utf-8')
    string_to_sign     = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign).encode('utf-8')  if(var==2)else string_to_sign.encode('utf-8')
    hmac_code          = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign               = quote_plus(base64.b64encode(hmac_code))
    return '{}&timestamp={}&sign={}'.format(webhook, timestamp, sign)

class _configure_manage:
    'Configuration file read and manage'
    def __init__(self, path = r'.\config.json'):
        self.path = path
        self.load()

    def load(self):
        try:
            with open(self.path, 'r') as fin:
                self.data = json.load(fin)
        except IOError:
            self.data = {}

    def save(self):
        with open(self.path, 'w') as fout:
            json.dump(self.data, fout)

class _dingtalk_robot_manage:
    'dingtalk robot manage , inherited from _dingbot_robot_signature'
    __all__ = ['conf', 'delete', 'login', 'name', 'remember', 'secret', 'webhook']
    def __init__(self, name = None):
        self.conf     = _configure_manage()
        self.name     = name
        if(self.name in self.conf.data.keys()):
            self.login()

    def login(self, webhook = None, secret = None):
        self.webhook  = webhook
        self.secret   = secret
        if(self.name in self.conf.data.keys()):
            self.webhook = self.conf.data[self.name][u'webhook']
            self.secret  = self.conf.data[self.name][u'secret']
        elif(not webhook):
            raise DingError('The robot need a webhook.')

    def remember(self):
        data = {u'webhook':self.webhook, u'secret':self.secret}
        self.conf.data[self.name] = data
        self.conf.save()

    def delete(self):
        if(self.name not in self.conf.data.keys()):
            raise DingError('{} is not a robot\'s name'.format(self.name))
        del self.conf.data[self.name]
        self.conf.save()
        self.__init__()

    def url(self):
        if(self.secret):
            return _signature(self.webhook, self.secret)
        return self.webhook

    def __getattr__(self, item):
        if('ding{}'.format(item.lower()) in [i.lower() for i in __all__] and self.webhook):
            index = [i.lower() for i in __all__].index('ding{}'.format(item.lower()))
            return eval(__all__[index])(self)
        raise AttributeError("'_dingtalk_robot_manage' object has no attribute '{}'.".format(item))

class _dingtalk_robot_api:
    'dingtalk robot api for sending messages'
    __all__ = ['actionCard', 'at', 'feedCard', 'link', 'markdown', 'text', 'send']
    def __init__(self, robot):
        self.__robot__ = robot
        self.__api__   = None
        self.__at__    = None

    def __getattr__(self, mothed):
        self.__api__ = mothed
        return self.send

    def send(self, **kwattr):
        url     = self.__robot__.url()
        headers = {'Content-Type': 'application/json'}
        data    = json.dumps({'at': self.__at__, 'msgtype': self.__api__, self.__api__: kwattr}).encode("utf-8")
        self.__init__(self.__robot__)
        return eval( _http_post( url, data, headers ) )

    def at(self,**kwattr):
        self.__at__ = kwattr

class DingError(RuntimeError):
    'the Error for dingbot and inherited from RuntimeError'

class DingManage(_dingtalk_robot_manage):
    'inherited from _dingtalk_robot_manage'

class DingAPI(_dingtalk_robot_api):
    'inherited from _dingtalk_robot_api for sending messages'

class DingRaise(_dingtalk_robot_api):
    'inherited from _dingtalk_robot_api and raise error while sending messages wrong'
    def send(self, **kwattr):
        remsg=_dingtalk_robot_api.send(self, **kwattr)
        if(remsg['errcode']):
            raise DingError('[Error {}]: {}'.format(remsg['errcode'], remsg['errmsg']))
        return remsg

class DingLimit(_dingtalk_robot_api):
    'inherited from _dingtalk_robot_api for sending while you are in the time limited'
    __his__={}
    def __contains__(self,value):
        if(self.__robot__.webhook not in self.__his__.keys()):
            self.__his__[self.__robot__.webhook] = [0] * 20
        return (value - self.__his__[self.__robot__.webhook][0] <= 60 )

    def send(self,**kwattr):
        if(time.time() not in self):
            self.__his__[self.__robot__.webhook] = self.__his__[self.__robot__.webhook][1:] + [ time.time() ]
            return _dingtalk_robot_api.send(self, **kwattr)
