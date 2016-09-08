#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pickle
import logging
import time

from lib import utils
from tornado.httputil import url_concat
from settings import APIS, A_MINUTE, A_HOUR, A_DAY


class PayCtrl(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.api = ctrl.pdb.api

    def __getattr__(self, name):
        return getattr(self.api, name)

    def get_day_summary_key(self, ktv_id, stm='', etm=''):
        return 's_day_summary_%s_%s_%s' % (ktv_id, stm, etm)

    def get_hour_turnover_key(self, ktv_id, stm='', etm=''):
        return 's_hour_turnover_%s_%s_%s' % (ktv_id, stm, etm)

    def get_month_turnover_key(self, ktv_id, stm='', etm=''):
        return 's_month_turnover_%s_%s_%s' % (ktv_id, stm, etm)

    def get_year_turnover_key(self, ktv_id, stm='', etm=''):
        return 's_year_turnover_%s_%s_%s' % (ktv_id, stm, etm)

    def get_revenue_prop_key(self, ktv_id, stm='', etm=''):
        return 's_revenue_%s_%s_%s' % (ktv_id, stm, etm)

    def get_pay_prop_key(self, ktv_id, stm='', etm=''):
        return 's_pay_prop_%s_%s_%s' % (ktv_id, stm, etm)

    async def get_ktv(self, ktv_id):
        ktv = await utils.async_common_api('/kinfo/%s' % ktv_id)
        return ktv

    async def send_message(self, username, password_org, ktv_id, content):
        msg = {}
        result = await utils.async_common_api('/verify/code/send', params=dict(phone_num=username, content=content))
        logging.info(result)

        if result.get('errmsg') == '请求成功' and result.get('msg') == 'OK':
            self.api.update_ktv_fin_account(username=username, password_org=password_org, ktv_id=ktv_id, password='')
            msg['type'] = 1
        else:
            msg['type'] = 2

        return msg

    async def get_order_by_orderid(self, pay_type, order_id):
        http_client = utils.get_async_client()
        params = {
            'order_id': order_id
        }
        request = utils.http_request(url_concat(APIS['order'].format(pay_type=pay_type), params))
        response = await http_client.fetch(request)
        order_info = json.loads(response.body.decode())
        return order_info['order']

    def gen_request(self, data_type, ktv_id, params):
        req_url = url_concat(APIS['ktv_fin_curdata'].format(data_type=data_type, ktv_id=ktv_id), params)
        logging.info('ngrok request: %s' % req_url)
        http_request = utils.http_request(req_url, auth_username='ktvsky', auth_password='ktvsky5166')
        return http_request

    async def get_ser_info(self, ktv_id):
        params = {
            'ktvid': ktv_id,
            'op': 'getktvpayinfo'
        }
        http_client = utils.get_async_client()
        http_request = utils.http_request(url_concat(APIS['ktv_service_info'], params))
        response = await http_client.fetch(http_request)
        response = json.loads(response.body.decode())
        return response['result']

    async def insert_ser_info(self, **params):
        ktv_ser_info = self.api.insert_ser_info(**params)
        tradeno = ktv_ser_info['id']
        params_api = {
            'op': 'savektvpayinfo',
            'tradeno': tradeno
        }
        http_client = utils.get_async_client()
        http_request = utils.http_request(url_concat(APIS['sub_ktv_service_info'], params_api))
        res = await http_client.fetch(http_request)

    async def get_day_data(self, ktv_id, stm='', etm=''):
        params = {
            'stm': stm,
            'etm': etm
        }
        http_client = utils.get_async_client()
        http_request = self.gen_request_ctl('getDaySummaryInfo', ktv_id, params)

        key = self.get_day_summary_key_ctl(ktv_id, stm, etm)
        data = self.ctrl.rs.get(key)

        if data:
            return pickle.loads(data)

        try:
            response = await http_client.fetch(http_request)
            data = json.loads(response.body.decode())
            assert int(data['code']) == 1
            self.ctrl.rs.set(key, pickle.dumps(data), A_MINUTE)
            return data
        except:
            return {}

    async def get_hour_data(self, ktv_id, stm='', etm=''):
        params = {
            'stm': stm,
            'etm': etm
        }
        http_client = utils.get_async_client()
        http_request = self.gen_request_ctl('getHourTurnoverInfo', ktv_id, params)

        key = self.get_hour_turnover_key_ctl(ktv_id, stm, etm)
        data = self.ctrl.rs.get(key)

        if data:
            return pickle.loads(data)

        try:
            response = await http_client.fetch(http_request)
            data = json.loads(response.body.decode())
            assert int(data['code']) == 1
            self.ctrl.rs.set(key, pickle.dumps(data), A_MINUTE * 10)
            return data
        except:
            return {}

    async def get_month_data(self, ktv_id, stm='', etm=''):
        params = {
            'stm': stm,
            'etm': etm
        }
        http_client = utils.get_async_client()
        http_request = self.gen_request_ctl('getMonthTurnoverInfo', ktv_id, params)

        key = self.get_month_turnover_key_ctl(ktv_id, stm, etm)
        data = self.ctrl.rs.get(key)

        if data:
            return pickle.loads(data)

        try:
            response = await http_client.fetch(http_request)
            data = json.loads(response.body.decode())
            assert int(data['code']) == 1
            self.ctrl.rs.set(key, pickle.dumps(data), A_HOUR * 12)
            return data
        except:
            return {}

    async def get_year_data(self, ktv_id, stm='', etm=''):
        params = {
            'stm': stm,
            'etm': etm
        }
        http_client = utils.get_async_client()
        http_request = self.gen_request_ctl('getYearTurnoverInfo', ktv_id, params)

        key = self.get_year_turnover_key_ctl(ktv_id, stm, etm)
        data = self.ctrl.rs.get(key)

        if data:
            return pickle.loads(data)

        try:
            response = await http_client.fetch(http_request)
            data = json.loads(response.body.decode())
            assert int(data['code']) == 1
            self.ctrl.rs.set(key, pickle.dumps(data), A_DAY * 7)
            return data
        except:
            return {}

    async def get_revenue_data(self, ktv_id, stm='', etm=''):
        params = {
            'stm': stm,
            'etm': etm
        }
        http_client = utils.get_async_client()
        http_request = self.gen_request_ctl('getRevenueInfo', ktv_id, params)

        key = self.get_revenue_prop_key_ctl(ktv_id, stm, etm)
        data = self.ctrl.rs.get(key)

        if data:
            return pickle.loads(data)

        try:
            response = await http_client.fetch(http_request)
            data = json.loads(response.body.decode())
            assert int(data['code']) == 1
            self.ctrl.rs.set(key, pickle.dumps(data), A_MINUTE)
            return data
        except:
            return {}

    async def get_per_data(self, ktv_id, stm= '', etm= ''):
        params = {
            'stm': stm,
            'etm': etm
        }
        http_client = utils.get_async_client()
        http_request = self.gen_request_ctl('getPayWayInfo', ktv_id, params)

        key = self.get_pay_prop_key_ctl(ktv_id, stm, etm)
        data = self.ctrl.rs.get(key)

        if data:
            return pickle.loads(data)

        try:
            response = await http_client.fetch(http_request)
            data = json.loads(response.body.decode())
            assert int(data['code']) == 1
            self.ctrl.rs.set(key, pickle.dumps(data), A_MINUTE)
            return data
        except:
            return {}

    def get_ktv_ser_order(self, tradeno):
        ktv_ser_order_info = self.api.get_ktv_ser_order(tradeno=tradeno)
        extra_info = dict(contract_period= ktv_ser_order_info['contract_period'],
                          month_price= ktv_ser_order_info['month_price'],
                          pay_cycle= ktv_ser_order_info['pay_cycle'],
                          auth_endtime= ktv_ser_order_info['auth_endtime'],
                          pay_mode= ktv_ser_order_info['pay_mode'],
                          room_count= ktv_ser_order_info['room_count']
                          )
        order_info = dict(id= ktv_ser_order_info['id'],
                          ktv_id= ktv_ser_order_info['ktv_id'],
                          ser_fee= ktv_ser_order_info['ser_fee'],
                          ser_period= ktv_ser_order_info['ser_period'],
                          create_time= ktv_ser_order_info['create_time'],
                          invoice= ktv_ser_order_info['invoice'],
                          phone_num= ktv_ser_order_info['phone_num']
                          )
        order_info['extra'] = extra_info
        return order_info
