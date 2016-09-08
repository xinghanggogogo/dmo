#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import base64

from tornado import web
from tornado.options import options
from lib import uimodules, uimethods
from tornado.httpserver import HTTPServer
from raven.contrib.tornado import AsyncSentryClient


URLS = [
    (r'erp\.ktvsky\.com',

        (r'/','handler.erp.IndexPageHandler'),
        (r'/bill/ktv/(\d+)/(\d+)/(.*)', 'handler.erp.BillPageHandler'),
        (r'/bill/stat', 'handler.erp.BillStatPageHandler'),
        (r'/bill/search/(wechat|alipay|pos)', 'handler.erp.BillSearchPageHandler'),
        (r'/bill/order/(wechat|alipay|pos)', 'handler.erp.BillOrderPageHandler'),
        (r'/bill/withdraw/(deposit|flow|bank)', 'handler.erp.WithdrawPageHandler'),
        (r'/bank', 'handler.erp.BankHandler'),
        (r'/withdraw', 'handler.erp.WithdrawHandler'),
        (r'/account/order', 'handler.erp.AliOrderHandler'),
        (r'/revenue/(hour|month|year|prop|pay_prop)', 'handler.erp.RevenueHandler'),
        (r'/prop/(revenue|pay)', 'handler.erp.PropHandler'),

        (r'/wx', 'handler.cashier.WxCallBackHandler'),
        (r'/wx/event', 'handler.cashier.EventCallBackHandler'),
        (r'/fetch/qrcode', 'handler.cashier.FetchQrcodeHandler'),
        (r'/openid/(\d+)/(\d+)', 'handler.cashier.CashierOpenidHandler'),
        (r'/cashier/grade', 'handler.cashier.CashierGradeHandler'),
        (r'/cashier/home', 'handler.cashier.CashierHomeHandler'),
        (r'/cashier/version', 'handler.cashier.CashierVersionHandler'),
        (r'/cashier/afterpay', 'handler.cashier.AfterPayHandler'),
        (r'/cashier/withdraw', 'handler.cashier.WithdrawHandler'),

        (r'/login', 'handler.erp.IndexPageHandler'),
        (r'/login_for', 'handler.pay.LoginForgetHandler'),
        (r'/login_set', 'handler.pay.LoginSetHandler'),
        (r'/ktvfinrevenue/(hour|month|year)', 'handler.pay.KtvFinRevenueHandler'),
        (r'/ktvfinprop/(revenue|pay)', 'handler.pay.KtvFinPropHandler'),
        (r'/ktv_fin_wd', 'handler.pay.KtvFinanceWithdrawHandler'),
        (r'/ktv_fin_wd/page', 'handler.pay.KtvFinWithdrawPageHandler'),
        (r'/ktv_fin_in', 'handler.pay.KtvFinanceIncomeHandler'),
        (r'/ktv_fin_in/page', 'handler.pay.KtvFinIncomePageHandler'),
        (r'/ktv_withdraw', 'handler.pay.WithdrawHandler'),
        (r'/ktv_fin_wd_rules', 'handler.pay.WithdrawRulesHandler'),
        (r'/ktv_fin_curdata', 'handler.pay.KtvFinCDHandler'),
        (r'/service/order', 'handler.pay.KtvServiceOrderHandler'),
        (r'/wx/ktv_fin_event', 'handler.pay.KtvFinEventCallBackHandler')
    )
]


class Application(web.Application):

    def __init__(self):
        settings = {
            'login_url': '/login',
            'xsrf_cookies': False,
            'compress_response': True,
            'debug': options.debug,
            'ui_modules': uimodules,
            'ui_methods': uimethods,
            'static_path': os.path.join(sys.path[0], 'static'),
            'template_path': os.path.join(sys.path[0], 'tpl'),
            'cookie_secret': base64.b64encode(uuid.uuid3(uuid.NAMESPACE_DNS, 'myktv').bytes),
            'sentry_url': 'https://d11a209bf6b44d108e21a1e4bf0a8c64:e8d0d661b78e48df81fa6f0e54248ae3@sentry.ktvsky.com/6'
        }
        web.Application.__init__(self, **settings)
        for spec in URLS:
            host = spec[0] if not options.debug else '.*$'
            handlers = spec[1:]
            self.add_handlers(host, handlers)


def run():
    app = Application()
    app.sentry_client = AsyncSentryClient(app.settings['sentry_url'])
    http_server = HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    print('Running on port %d' % options.port)
