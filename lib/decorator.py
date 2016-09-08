#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from urllib.parse import quote
from sqlalchemy.orm import class_mapper
from settings import WX_USERINFO_GRANT_URL, WX_REDIRECT_URL, WX_CONF

def model2dict(model):
    if not model:
        return {}
    fields = class_mapper(model.__class__).columns.keys()
    return dict((col, getattr(model, col)) for col in fields)

def model_to_dict(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return model2dict(ret)
    return wrap

def models_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [model2dict(r) for r in ret]
    return wrap

def tuples_first_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [item[0] for item in ret]
    return wrap

def filter_update_data(func):
    def wrap(*args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            data = dict([(key, value) for key, value in data.items() if value or value == 0])
            kwargs['data'] = data
        return func(*args, **kwargs)
    return wrap

def tuple_to_dict(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [dict(zip(i.keys(), i.values())) for i in ret]
    return wrap

def check_useragent(func):
    def wrap(*args, **kw):
        self = args[0]
        ua = self.request.headers.get('User-Agent', '')
        if 'ThunderErp' not in ua:
            return self.render('error.tpl')
        return func(*args, **kw)
    return wrap

def wx_auth(func):
    def wrap(*args, **kw):
        self = args[0]
        openid = self.get_cookie('openid')
        if openid:
            return func(*args, **kw)
        url = WX_USERINFO_GRANT_URL.format(appid=WX_CONF['appid'], redirect_uri=WX_REDIRECT_URL, state=quote(self.request.path))
        return self.redirect(url)
    return wrap

