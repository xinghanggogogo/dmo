#!/usr/bin/env python
# -*- coding: utf-8 -*-

#redis mysql API ERR_MSG TIME  WEIXIN_API

# redis
REDIS = {
    'host': '10.10.155.122',
    'port': 6379
}

# mysql
DB_KTV = 'myktv'
MYSQL = {
    DB:{
        'master': {
            'host': '10.10.146.167',
            'user': 'ktvsky',
            'pass': '098f6bcd4621d373cade4e832627b4f6',
            'port': 3306
        },
        'slaves': [
            {
                'host': '10.10.18.204',
                'user': 'ktvsky',
                'pass': '098f6bcd4621d373cade4e832627b4f6',
                'port': 3308
            }
        ],
    },
}

ERR_MSG = {
    200: '服务正常',
    10001: '请求参数错误',
    40004: '无数据',
    50001: '系统错误',
}

# time
A_MINUTE = 60
A_HOUR = 3600
A_DAY = 24 * A_HOUR


APIS = {
    #接口
}

SECURET = 'LSKDFJA9LS5LKJO980DSJWL2NL234B03'

WX_CONF = {
    'appid': 'wx790c59cfd383eb60',
    'appsecret': '0086acb983365eb952fc37cd52ef4e83'
}

WX_USERINFO_GRANT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo&state={state}&connect_redirect=1#wechat_redirect'
FETCH_OPENID_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
FETCH_USERINFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN'
FETCH_USERINFO_URL_V2 = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN'
WX_REDIRECT_URL = 'https://erp.ktvsky.com/wx'
QRCODE_TICKET = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}'
TEMPLATE_MSG_URL = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'

# try to load debug settings
# try:
#     from tornado.options import options
#     if options.debug:
#         exec(compile(open('settings.debug.py')
#              .read(), 'settings.debug.py', 'exec'))
# except:
#     pass
