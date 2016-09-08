#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import when
import math
import logging
import datetime
import hashlib
import random
import qrcode
import base64

from io import BytesIO
from control import ctrl
from handler.base import BaseHandler
from tornado.httputil import url_concat
from settings import APIS, MYKTV_SECRET, SECURET, QRCODE_TICKET
from tornado import web, gen
from lib import utils


class IndexPageHandler(BaseHandler):

    MOBILE_PATTERN = re.compile('(Mobile|iPod|iPhone|Android|Opera Mini|BlackBerry|webOS|UCWEB|Blazer|PSP)', re.I)

    def _d(self):
        if self.MOBILE_PATTERN.search(self.request.headers.get('user-agent', '')):
            return 'mobile'
        else:
            return 'pc'

    def post(self):
        try:
            username = int(self.get_argument('username'))
            password = self.get_argument('password')
        except Exception as e:
            raise utils.APIError(errcode=10001)

        user = ctrl.pay.get_ktv_fin_account(username)
        msg = dict(type=0)
        if not user:
            pass
        elif password == user['password_org'] and not user['password']:
            self._login(username)
            self.set_secure_cookie('is_login', str(user['ktv_id']), expires_days=1)
            msg.update({
                'type': 1
            })
        elif password == user['password']:
            self._login(username)
            self.set_secure_cookie('is_login', str(user['ktv_id']), expires_days=1)
            msg.update({
                'type': 2,
                'user': user
            })

        self.send_json(msg)

    def get(self):
        username = self.get_argument('username', '')
        self.render('pay/login.tpl', username=username, source=self._d())


class BillPageHandler(BaseHandler):

    def get(self, timestamp, ktv_id, sign):

        if not utils.check_sign(timestamp, ktv_id, sign):
            return self.render('error.tpl')

        self.set_secure_cookie('is_login', ktv_id, expires_days=1)
        self.redirect('/bill/stat')


class BillStatPageHandler(BaseHandler):

    async def _get_base64_img(self, ktv_id):
        ktv = await ctrl.pay.get_ktv_ctl(ktv_id)
        if not ktv:
            return
        try:
            response = await utils.async_common_api('/wx/arged/qrcode', dict(flag=2, arg='%s,%s'%(ktv['bank_phone'], ktv_id)))
            print (response)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=8,
                border=0
            )
            img = qr.make(response['url'])
            by = BytesIO()
            img.save(by, format='png')
            base64_img = base64.encodebytes(by.getvalue())
            return base64_img
        except Exception as e:
            logging.error(e)
            return None

    async def get(self):
        is_login = self.get_secure_cookie('is_login')
        print ('ktv_id:' + is_login.decode())
        if not is_login:
            return self.render('error.tpl')

        ktv_id = int(is_login.decode())
        bank_info = await ctrl.erp.get_bank_info_ctl(ktv_id)
        revenue = await ctrl.pay.get_day_data_ctl(ktv_id)
        base64_img = await self._get_base64_img(ktv_id)

        self.render('stat.tpl',
                    ktv_id=ktv_id,
                    top_cate='stat',
                    base64_img=base64_img,
                    bank_info=bank_info,
                    revenue=revenue)


class BillSearchPageHandler(BaseHandler):

    async def get(self, pay_type):
        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return self.render('error.tpl')

        try:
            page = int(self.get_argument('page', 1))
            start_date = self.get_argument('start_date')
            end_date = self.get_argument('end_date')
            term_id = self.get_argument('term_id', '')
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        page_size = 20
        ktv_id = int(is_login.decode())
        order_info = await ctrl.erp.get_pay_orders_ctl(ktv_id, term_id=term_id, pay_type=pay_type, start_date=start_date, end_date=end_date, page=page, page_size=page_size)

        orders = order_info['list']
        total = order_info['total']

        page_total = (total + page_size - 1) // page_size

        if pay_type == 'pos':
            pos_list = (await ctrl.erp.get_ktv_pos_ctl(ktv_id))['list']
        else:
            pos_list = []

        self.render('orders.tpl',
                    ktv_id=ktv_id,
                    top_cate='order',
                    pay_type=pay_type,
                    orders=orders,
                    start_date=start_date,
                    end_date=end_date,
                    pos_list=pos_list,
                    term_id=term_id,
                    page=page,
                    page_size=page_size,
                    page_total=page_total)


class BillOrderPageHandler(BaseHandler):

    async def get(self, pay_type):
        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return self.render('error.tpl')

        try:
            page = int(self.get_argument('page', 1))
        except:
            raise utils.APIError(errcode=10001)

        page_size = 20
        ktv_id = int(is_login.decode())
        today = datetime.datetime.now()
        today_7ago = today - datetime.timedelta(days=7)
        start_date = today_7ago.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

        order_info = await ctrl.erp.get_pay_orders_ctl(ktv_id, pay_type=pay_type, start_date=start_date, end_date=end_date, page=page, page_size=page_size)
        orders = order_info['list']
        total = order_info['total']

        page_total = (total + page_size - 1) // page_size

        if pay_type == 'pos':
            pos_list = (await ctrl.erp.get_ktv_pos_ctl(ktv_id))['list']
        else:
            pos_list = []

        self.render('orders.tpl',
                    ktv_id=ktv_id,
                    top_cate='order',
                    pay_type=pay_type,
                    orders=orders,
                    start_date=start_date,
                    end_date=end_date,
                    term_id='',
                    pos_list=pos_list,
                    page=page,
                    page_size=page_size,
                    page_total=page_total)


class WithdrawPageHandler(BaseHandler):

    async def render_deposit(self, ktv_id):
        bank_info = await ctrl.erp.get_bank_info_ctl(ktv_id)

        if bank_info['bank_is_empty']:
            self.redirect('/bill/withdraw/bank')
            return

        extra_bank = bank_info['extra_bank']
        if extra_bank:
            extra_bank = json.loads(extra_bank)[0]
            bank_info['extra_bank'] = extra_bank
            bank_info['extra_bank']['bank_account'] = '%s 尾号 %s' % (bank_info['extra_bank']['bank_name'], bank_info['extra_bank']['bank_account'][-4:])

        self.render('deposit.tpl',
                    top_cate='withdraw',
                    action='deposit',
                    ktv_id=ktv_id,
                    bank_info=bank_info)

    async def render_flow(self, ktv_id):
        try:
            page = int(self.get_argument('page', 1))
        except:
            raise utils.APIError(errcode=10001)

        page_size = 20
        start_date = '2016-01-01'
        end_date = '2020-01-01'
        order_info = await ctrl.erp.get_pay_orders_ctl(ktv_id, pay_type='deposit', start_date=start_date, end_date=end_date, page=page, page_size=page_size)

        orders = order_info['list']
        total = order_info['total']

        page_total = (total + page_size - 1) // page_size

        self.render('flow.tpl',
                    top_cate='withdraw',
                    action='flow',
                    ktv_id=ktv_id,
                    orders=orders,
                    page=page,
                    page_size=page_size,
                    page_total=page_total)

    async def render_bank(self, ktv_id):
        try:
            is_extra = int(self.get_argument('is_extra', 0))
        except:
            raise utils.APIError(errcode=10001)

        bank_info = await ctrl.erp.get_bank_info_ctl(ktv_id)

        self.render('bank.tpl',
                    top_cate='withdraw',
                    action='deposit',
                    is_extra=is_extra,
                    bank_info=bank_info)

    async def get(self, action):
        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return self.render('error.tpl')

        await getattr(self, 'render_%s' % action)(is_login.decode())


class BankHandler(BaseHandler):

    async def post(self):
        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return

        try:
            bank_account = self.get_argument('bank_account')
            bank_name = self.get_argument('bank_name')
            bank_branch = self.get_argument('bank_branch')
            account_name = self.get_argument('account_name')
            bank_phone = self.get_argument('bank_phone')
            is_extra = int(self.get_argument('is_extra', 0))
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        ktv_id = int(is_login.decode())
        response = await ctrl.erp.update_bank_info_ctl(ktv_id, {
            'bank_account': bank_account,
            'bank_name': bank_name,
            'bank_branch': bank_branch,
            'account_name': account_name,
            'bank_phone': bank_phone,
            'is_extra': is_extra
        })
        self.send_json(data=response)


class WithdrawHandler(BaseHandler):

    async def post(self):
        try:
            is_extra = int(self.get_argument('is_extra', 0))
            bank_phone = self.get_argument('bank_phone', '')
        except:
            raise utils.APIError(errcode=10001)

        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return

        ktv_id = int(is_login.decode())
        ktv = await ctrl.pay.get_ktv_ctl(ktv_id)

        if not ktv:
            return

        if not is_extra and bank_phone and not ktv['bank_phone']:
            await ctrl.erp.update_ktv_ctl(ktv_id, {
                'bank_phone': bank_phone
            })

        response = await ctrl.erp.withdraw_money_ctl(ktv_id, is_extra)
        self.send_json(response)


class AliOrderHandler(BaseHandler):

    def _money_format(self, fee):
        return '%.02f元' % (fee / 100)

    async def export(self, ktv_id):
        try:
            pay_type = self.get_argument('pay_type', 'wechat')
            start_date = self.get_argument('start_date')
            end_date = self.get_argument('end_date')
            assert pay_type in ('wechat', 'alipay', 'pos')
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        data = []
        order_info = await ctrl.erp.get_pay_orders_ctl(ktv_id, pay_type=pay_type, start_date=start_date, end_date=end_date, has_pn=False)
        orders = order_info['list']

        if not orders:
            raise utils.APIError(errcode=40004)

        if pay_type == 'wechat':
            sheet_dict = {
                'sheetname': '微信进出账流水',
                'titles': ['商户订单号', '订单费用', '手续费返还', '手续费用', '支付方式', '订单创建时间', '订单详情', '线下订单号']
            }
            for order in orders:
                sheet_dict.setdefault('data', []).append([order['order_id'], self._money_format(order['total_fee']), self._money_format(order['coupon_fee']),
                     self._money_format(order['rate_fee']), utils.wxorder_action_to_text(order['action']), order['create_time'], order['body'], order['erp_id']])
        elif pay_type == 'alipay':
            sheet_dict = {
                'sheetname': '支付宝进出账流水',
                'titles': ['商户订单号', '订单费用', '手续费返还', '手续费用', '支付方式', '订单创建时间', '订单详情', '线下订单号']
            }
            for order in orders:
                sheet_dict.setdefault('data', []).append([order['order_id'], self._money_format(order['total_fee']), self._money_format(order['coupon_fee']),
                     self._money_format(order['rate_fee']), utils.wxorder_action_to_text(order['action']), order['create_time'], order['body'], order['erp_id']])
        else:
            sheet_dict = {
                'sheetname': 'pos机进出账流水',
                'titles': ['商户订单号', '订单费用', '手续费返还', '手续费用','订单状态', '订单创建时间']
            }
            for order in orders:
                sheet_dict.setdefault('data', []).append([order['order_no'], self._money_format(order['amount']), self._money_format(order['coupon_fee']),
                     self._money_format(order['rate_fee']), '已支付', order['finish_time']])

        data.append(sheet_dict)
        filename = 'static/data/进出账流水_%s~%s.xlsx' % (start_date, end_date)
        filename_with_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
        utils.export_xlsx(data=data, export_filename=filename_with_path)
        self.set_header('Access-Control-Allow-Origin', '*')
        self.send_json(data={'url': '/' + filename})

    async def post(self):
        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return

        ktv_id = int(is_login.decode())
        await self.export(ktv_id)


class RevenueHandler(BaseHandler):

    async def get(self, data_type):
        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return

        ktv_id = int(is_login.decode())

        if data_type == 'hour':
            revenue = await ctrl.pay.get_hour_data_ctl(ktv_id)
        elif data_type == 'month':
            revenue = await ctrl.pay.get_month_data_ctl(ktv_id)
        else:
            revenue = await ctrl.pay.get_year_data_ctl(ktv_id)

        times = [rev['Time'] for rev in revenue.get('data', [])]
        values = [rev['Value'] for rev in revenue.get('data', [])]

        self.send_json({
            'times': times,
            'values': values
        })


class PropHandler(BaseHandler):

    async def get(self, data_type):
        is_login = self.get_secure_cookie('is_login')

        if not is_login:
            return

        ktv_id = int(is_login.decode())

        if data_type == 'revenue':
            prop = await ctrl.pay.get_revenue_data_ctl(ktv_id)
        else:
            prop = await ctrl.pay.get_per_data_ctl(ktv_id)

        self.send_json({
            'data': prop.get('data', [])
        })

