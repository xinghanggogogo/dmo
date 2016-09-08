#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime

from lib import utils
from settings import APIS, COMMON_URL
from urllib.parse import urlencode
from tornado.httputil import url_concat


class ErpCtrl(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.api = ctrl.pdb.api

    def __getattr__(self, name):
        return getattr(self.api, name)

    def get_cashier_key(self, openid):
        return 'cashier_%s' % openid

    def get_cashier(self, openid):
        key = self.get_cashier_key_ctl(openid)
        cashier = self.ctrl.rs.get(key)
        if cashier:
            return eval(cashier)

        cashier = self.api.get_cashier(openid=openid)
        self.ctrl.rs.set(key, cashier)
        return cashier

    def add_cashier(self, ktv_id, client_id, openid, headimgurl, nickname):
        cashier = self.api.add_cashier(ktv_id=ktv_id, client_id=client_id, openid=openid, total_cash=0, score=0,
                                       ac_task='0,0', sp_task='1000, 0', headimgurl=headimgurl, nickname=nickname)
        if cashier:
            self.ctrl.rs.set(self.get_cashier_key_ctl(openid), cashier)

    def update_cashier(self, openid, data):
        self.api.update_cashier(openid, data)
        self.ctrl.rs.delete(self.get_cashier_key_ctl(openid))

    def get_cashier_version(self):
        key = 'cashier_version'
        cashier_version = self.ctrl.rs.get(key)
        if cashier_version:
            return eval(cashier_version)
        return {}

    def set_cashier_version(self, cashier_version):
        assert isinstance(cashier_version, dict)
        key = 'cashier_version'
        self.ctrl.rs.set(key, cashier_version)

    def get_cashier_grade_bg_img_url(self):
        key = 'cashier_grade_bg_img_url'
        return self.ctrl.rs.get(key).decode()

    async def _request_orders(self, ktv_id, term_id, pay_type, start_date, end_date, page, page_size, has_pn=None):
        if pay_type == 'wechat':
            url = APIS['account_order'].format(ktv_id=ktv_id)
        elif pay_type == 'alipay':
            url = APIS['ali_account_order'].format(ktv_id=ktv_id)
        elif pay_type == 'pos':
            url = APIS['pos_account_order'].format(ktv_id=ktv_id)
        elif pay_type == 'deposit':
            url = APIS['withdraw_history'].format(ktv_id=ktv_id)
        else:
            raise utils.APIError(errcode=10001)

        http_client = utils.get_async_client()

        params = {
            'term_id': term_id,
            'start_date': start_date,
            'end_date': end_date
        }

        if has_pn:
            params.update({
                'pn': page,
                'size': page_size,
                'has_pn': True
            })

        request = utils.http_request(url_concat(url, params))
        response = await http_client.fetch(request)
        orders = json.loads(response.body.decode())
        return orders

    async def update_ktv(self, ktv_id, args):
        http_client = utils.get_async_client()
        req_url = '{url}/kinfo/{ktv_id}'.format(url=COMMON_URL, ktv_id=ktv_id)
        params = json.dumps(args)
        request = utils.http_request(req_url, method='PUT', body=params)
        response = await http_client.fetch(request)
        response = json.loads(response.body.decode())
        return response

    async def get_ktv_pos(self, ktv_id):
        req_url = APIS['ktv_pos'].format(ktv_id=ktv_id)
        http_client = utils.get_async_client()
        request = utils.http_request(req_url)
        response = await http_client.fetch(request)
        pos_list = json.loads(response.body.decode())
        return pos_list

    async def get_pay_orders(self, ktv_id, term_id='', pay_type='wechat', start_date=None, end_date=None, page=1, page_size=30, has_pn=True):
        orders = await self._request_orders_ctl(ktv_id, term_id, pay_type, start_date + ' 00:00:00', end_date + ' 00:00:00',  page, page_size, has_pn)
        return orders

    async def get_bank_info(self, ktv_id):
        http_client = utils.get_async_client()
        request = utils.http_request(APIS['withdraw_account'].format(ktv_id=ktv_id))
        response = await http_client.fetch(request)
        bank_info = json.loads(response.body.decode())
        return bank_info

    async def update_bank_info(self, ktv_id, args):
        http_client = utils.get_async_client()
        params = urlencode(args)
        request = utils.http_request(APIS['bank'].format(ktv_id=ktv_id), method='POST', body=params)
        response = await http_client.fetch(request)
        response = json.loads(response.body.decode())
        return response

    async def withdraw_money(self, ktv_id, is_extra=0):
        http_client = utils.get_async_client()
        params = urlencode({
            'is_extra': is_extra
        })
        http_request = utils.http_request(APIS['withdraw'].format(ktv_id=ktv_id), method='POST', body=params)
        response = await http_client.fetch(http_request)
        response = json.loads(response.body.decode())
        return response
