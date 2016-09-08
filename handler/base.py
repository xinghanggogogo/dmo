#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback

from tornado import web
from control import ctrl
from lib import uimethods, utils
from settings import ERR_MSG
from raven.contrib.tornado import SentryMixin
from tornado.options import options


class BaseHandler(web.RequestHandler, SentryMixin):

    def dict_args(self):
        _rq_args = self.request.arguments
        rq_args = dict([(k, _rq_args[k][0].decode()) for k in _rq_args])
        logging.info(rq_args)
        return rq_args

    def initialize(self):
        ctrl.pdb.close()

    def on_finish(self):
        ctrl.pdb.close()

    def send_json(self, data={}, errcode=200, status_code=200):
        res = {
            'errcode': errcode,
            'errmsg': ERR_MSG[errcode]
        }
        res.update(data)
        self.set_header('Content-Type', 'application/json')
        self.set_status(status_code)
        json_str = uimethods.json_format(self, res)
        self.write(json_str)

    def write_error(self, status_code=200, **kwargs):
        if 'exc_info' in kwargs:
            err_object = kwargs['exc_info'][1]
            traceback.format_exception(*kwargs['exc_info'])

            if isinstance(err_object, utils.APIError):
                err_info = err_object.kwargs
                self.send_json(**err_info)
                return

        self.send_json(status_code=500, errcode=50001)
        if not options.debug:
            self.captureException(**kwargs)

    def get_secure_cookie(self, name, **kwargs):
        cookie = super(BaseHandler, self).get_secure_cookie(name, **kwargs)
        logging.info(cookie)
        return cookie

    def get_current_user(self):
        username = self.get_secure_cookie('erp_ktvsky_com')
        if not username:
            self._logout()
            return
        return username.decode()

    def _login(self, username):
        username = str(username)
        self.set_secure_cookie('erp_ktvsky_com', username, expires_days=1)

    def _logout(self):
        self.clear_cookie('erp_ktvsky_com')
        self.current_user = None
