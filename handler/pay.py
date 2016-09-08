#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import logging
import datetime
import json
import xml2json
import optparse

from control import ctrl
from lib import utils
from tornado import web
from handler.base import BaseHandler
from settings import OrderStateString, PayType, QRCODE_TICKET


class PayBaseHandler(BaseHandler):

    def check_xsrf_cookie(self):
        super(BaseHandler, self).check_xsrf_cookie()

    def get_current_user(self):
        if self.get_argument('demo', ''):
            username = '13419664597'
            self._login(username)
            return username

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


class LoginForgetHandler(PayBaseHandler):

    def random_code(self):
        '''
        忘记密码
        '''
        n = random.randint(99999,1000000)
        return n

    async def post(self):
        try:
            username = self.get_argument('username')
            password_org = self.get_argument('password_org')
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        msg = {}
        user = ctrl.pay.get_ktv_fin_account(username)

        if not user:
            msg.update({
                'type': 0
            })
            return self.send_json(msg)

        if not password_org:
            username = int(username)
            password_org = self.random_code()
            content = '密码重置验证：%s（5分钟内有效），请您尽快完成登陆密码的重置。如有问题请电询：010-51667307' % password_org
            msg = await ctrl.pay.send_message_ctl(username=username, password_org=password_org, ktv_id=user['ktv_id'], content=content)
            return self.send_json(msg)

        if password_org == user['password_org']:
            # 匹配初始密码,让用户重置密码
            self._login(username)
            msg['type']= 3
            return self.send_json(msg)
        else:
            # 验证码输入错误
            msg['type'] = 4
            return self.send_json(msg)

    def get(self):
        username = self.get_argument('username', '')
        self.render('pay/login.tpl', username=username)


class LoginSetHandler(PayBaseHandler):

    @web.authenticated
    def get(self):
        '''
        密码重置
        '''
        self.render('pay/login.tpl')

    @web.authenticated
    def post(self):
        try:
            password1 = self.get_argument('password1')
            password2 = self.get_argument('password2')
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        username = self.current_user
        user = ctrl.pay.get_ktv_fin_account(username)
        msg = {}

        if password1 != password2:
            msg['type'] = 0
            self.send_json(msg)
        else:
            ctrl.pay.update_ktv_fin_account(username=username, password=password1)
            msg.update({
                'type': 1,
                'user': user
            })
            self.send_json(msg)


class KtvFinCDHandler(PayBaseHandler):

    @web.authenticated
    async def get(self):
        username = self.current_user
        user = ctrl.pay.get_ktv_fin_account(username)
        ktv = await ctrl.pay.get_ktv_ctl(user['ktv_id'])

        revenue = await ctrl.pay.get_day_data_ctl(ktv_id=user['ktv_id'])
        try:
            yesterday_revenue = revenue['data'][0]
            today_revenue = revenue['data'][1]
        except:
            return self.render('error.tpl')
        config = await utils.async_common_api('/wx/share/config', dict(url=self.request.full_url()))

        self.render('pay/realData.tpl',
                    ktv=ktv,
                    config=config,
                    today_revenue=today_revenue,
                    yesterday_revenue=yesterday_revenue,
                    active_type='current_data',
                    user=user)


class KtvFinRevenueHandler(PayBaseHandler):

    async def get(self, data_type):
        try:
            ktv_id = self.get_argument('ktv_id')
        except:
            raise utils.APIError(errcode=10001)

        if data_type == 'hour':
            revenue = await ctrl.pay.get_hour_data_ctl(ktv_id)
            times = [rev['Time'][11:] for rev in revenue.get('data', [])]
        elif data_type == 'month':
            revenue = await ctrl.pay.get_month_data_ctl(ktv_id)
            times = [rev['Time'][6:] for rev in revenue.get('data', [])]
        else:
            revenue = await ctrl.pay.get_year_data_ctl(ktv_id)
            times = [rev['Time'] for rev in revenue.get('data', [])]

        values = [float(rev['Value']) for rev in revenue.get('data', [])]
        total = '%.02f' % sum(values)

        self.send_json({
            'times': times,
            'values': values,
            'total': total
        })


class KtvFinPropHandler(PayBaseHandler):

    @web.authenticated
    async def get(self, data_type):
        username = self.current_user
        user = ctrl.pay.get_ktv_fin_account(username)
        ktv_id = user['ktv_id']

        if data_type == 'revenue':
            revenue_data = await ctrl.pay.get_revenue_data_ctl(ktv_id)
            revenue_data = revenue_data.get('data', [])
            data = [[item['Name'] + ' ' + item['Value'], float(item['ValueRate'][:-1])] for item in revenue_data]
        else:
            prop = await ctrl.pay.get_per_data_ctl(ktv_id)
            data = prop.get('data', [])
            for item in data:
                item['ValueRate'] = item['ValueRate'][:-1]

        self.send_json({
            'data': data
        })


class KtvFinanceWithdrawHandler(PayBaseHandler):

    @web.authenticated
    async def get(self):
        '''
        提现服务页面和详情页
        '''
        username = self.current_user
        user = ctrl.pay.get_ktv_fin_account(username)

        self.set_secure_cookie('is_login', str(user['ktv_id']), expires_days=1)

        ktv = await ctrl.pay.get_ktv_ctl(user['ktv_id'])
        bank_info_exist_flag = ktv['bank_account'] != '' and ktv['bank_name'] != '' and ktv['bank_branch'] != '' and \
                         ktv['bank_phone'] != '' and ktv['account_name'] != ''

        ser_info = await ctrl.pay.get_ser_info_ctl(12)

        if ser_info:
            ser_info['contract_left'] = ser_info['contract_period'] - ser_info['pay_cycle']
            ser_info['days_left'] = (datetime.datetime.strptime(ser_info['auth_endtime'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()).days

        config = await utils.async_common_api('/wx/share/config', dict(url=self.request.full_url()))

        withdraw_info = await ctrl.erp.get_bank_info_ctl(user['ktv_id'])
        withdraw_info['bank_account'] = withdraw_info['bank_name'] + ' 尾号 ' + withdraw_info['bank_account'][-4:]

        if not withdraw_info.get('total_fee'):
            withdraw_info.update({
                'total_fee': 0
            })

        self.render('pay/cash.tpl',
            config=config,
            user=user,
            bank_info_exist=bank_info_exist_flag,
            withdraw_info=withdraw_info,
            ktv=ktv,
            active_type='withdraw_list',
            ser_info=ser_info
        )


class KtvFinWithdrawPageHandler(PayBaseHandler):

    async def get(self):
        try:
            ktv_id = self.get_argument('ktv_id')
            page = int(self.get_argument('page', 1))
            from_date = self.get_argument('form_date', '2015-1-1')
            to_date = self.get_argument('to_date', datetime.datetime.now().strftime('%Y-%m-%d'))
        except:
            raise utils.APIError(errcode=10001)

        wd_list = await utils.async_common_api('/wx/withdraw/%s' % ktv_id, params=dict(from_date=from_date, to_date=to_date, page=page))
        logging.error(wd_list)

        for item in wd_list['list']:
            item['start_date'] = item['start_date'][:-8]
            item['end_date'] = item['end_date'][:-8]

        self.send_json(dict(list=wd_list['list'], total=wd_list['total']))


class WithdrawHandler(PayBaseHandler):

    @web.authenticated
    async def post(self):
        '''
        提现按钮
        '''
        ser_fee = self.get_argument('ser_fee', 0)
        ser_period = self.get_argument('ser_period', 0)
        invoice = self.get_argument('invoice', 0)
        phone_num = self.get_argument('phone_num', '')

        username = self.current_user
        user = ctrl.pay.get_ktv_fin_account(username)

        if ser_fee:
            params = {}
            ser_info = await ctrl.pay.get_ser_info_ctl(12)
            params.update({
                'ktv_id': user['ktv_id'],
                'ser_fee': ser_fee,
                'ser_period': ser_period,
                'invoice': invoice,
                'phone_num': phone_num,
                'contract_period': ser_info['contract_period'],
                'pay_cycle': ser_info['pay_cycle'],
                'month_price': ser_info['month_price'],
                'auth_endtime': ser_info['auth_endtime'],
                'pay_mode': ser_info['pay_mode'],
                'room_count': ser_info['room_count']})
            await ctrl.pay.insert_ser_info_ctl(**params)

        response = await ctrl.erp.withdraw_money_ctl(user['ktv_id'])
        self.send_json(response)


class KtvServiceOrderHandler(PayBaseHandler):

    def get(self):
        '''
        商户服务订单反查询接口
        '''
        try:
            tradeno = int(self.get_argument('tradeno'))
        except:
            raise utils.APIError(errcode=10001)

        ktv_ser_order = ctrl.pay.get_ktv_ser_order_ctl(tradeno)

        self.send_json(ktv_ser_order)


class WithdrawRulesHandler(PayBaseHandler):

    @web.authenticated
    async def get(self):
        '''
        提现规则说明页
        '''
        username = self.current_user
        user = ctrl.pay.get_ktv_fin_account(username)
        ktv = await ctrl.pay.get_ktv_ctl(user['ktv_id'])

        config = await utils.async_common_api('/wx/share/config', dict(url=self.request.full_url()))

        self.render('pay/cashRule.tpl',
            ktv=ktv,
            user=user,
            config=config
        )


class KtvFinIncomePageHandler(PayBaseHandler):

    @web.authenticated
    async def get(self):
        '''
        营业流水分页
        '''
        try:
            ktv_id = int(self.get_argument('ktv_id'))
            pay_type = self.get_argument('pay_type', 'wechat')
            start_date = self.get_argument('start_date', '2015-01-01')
            end_date = self.get_argument('end_date', datetime.datetime.now().strftime('%Y-%m-%d'))
            page = int(self.get_argument('page', 1))
        except Exception as e:
            raise utils.APIError(errcode=10001)

        params = {
            'ktv_id': ktv_id,
            'start_date': start_date,
            'end_date': end_date,
            'pay_type': pay_type,
            'page_size': 10,
            'page': page,
            'has_pn': True
        }

        income_list = await ctrl.erp.get_pay_orders_ctl(**params)
        income_list, total = income_list['list'], income_list['total']
        if pay_type == 'pos':
            for item in income_list:
                item.update({
                    'total_fee': item['amount'],
                    'erp_id': '空'
                })

        for item in income_list:
            item.update({
                'pay_type': pay_type
            })

        self.send_json(dict(list=income_list, total=total))


class KtvFinanceIncomeHandler(PayBaseHandler):

    @web.authenticated
    async def get(self):
        '''
        营业流水/筛选条件
        '''
        try:
            ktv_id = self.get_argument('ktv_id')
            pay_type = self.get_argument('pay_type', 'wechat')
            start_date = self.get_argument('start_date', '')
            end_date = self.get_argument('end_date', datetime.datetime.now().strftime('%Y-%m-%d'))
            page_size = self.get_argument('page_size', 10)
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        if not start_date:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

        username = self.current_user
        user = ctrl.pay.get_ktv_fin_account(username)
        ktv = await ctrl.pay.get_ktv_ctl(ktv_id)

        config = await utils.async_common_api('/wx/share/config', dict(url=self.request.full_url()))

        params = {
            'ktv_id': ktv_id,
            'pay_type': pay_type,
            'start_date':start_date,
            'end_date':end_date,
            'page_size':page_size
        }

        income_list = await ctrl.erp.get_pay_orders_ctl(**params)

        for i in range(0,len(income_list['list'])):
            print (income_list['list'][i])

        if pay_type == 'pos':
            [item.update({'total_fee': item['amount'], 'erp_id': '空'}) for item in income_list['list']]

        for item in income_list['list']:
            item.update({
                'pay_type': pay_type
            })

        self.render('pay/bill.tpl',
             config=config,
             user=user,
             pay_type=pay_type,
             ktv=ktv,
             income_list=income_list['list'],
             active_type='income_list'
        )

    async def post(self):
        '''
        营业订单详情
        '''
        try:
            pay_type = self.get_argument('pay_type')
            order_id = self.get_argument('order_id')
        except:
            raise utils.APIError(errcode=10001)

        print (pay_type)
        print (order_id)

        order = await ctrl.pay.get_order_by_orderid_ctl(pay_type=pay_type, order_id=order_id)

        order.update({
            'pay_type': PayType[pay_type]
        })

        if pay_type in ('wechat', 'alipay'):
            order['state'] = OrderStateString[order['state']]
            order['net_id'] = order['wx_pay_id'] if pay_type == 'wechat' else order['ali_pay_id']
        else:
            state_dict = { 1: '成功', 0: '失败' }
            order.update(dict(total_fee=order['amount'], erp_id='空', net_id=order['order_no'], state=state_dict[order['state']]))

        self.send_json(order)


class KtvFinEventCallBackHandler(PayBaseHandler):

    def get(self):
        self.write(self.get_argument('echostr'))

    async def post(self):
        msg = self.request.body
        msg_dict = json.loads(xml2json.xml2json(msg.decode(), optparse.Values({'pretty': True})))
        logging.error(msg_dict)

        msg_dict = msg_dict.get('xml', {})
        event = msg_dict.get('Event', '')
        openid = msg_dict.get('FromUserName', '')
        username_and_ktv_id = msg_dict.get('EventKey', '')
        username, ktv_id = list(map(int, username_and_ktv_id.split(',')))

        if event not in ('subscribe', 'SCAN') or not username or not ktv_id: #action
            return

        user = ctrl.pay.get_ktv_fin_account(username)
        if not user:
            username = int(username)
            password_org = random.randint(99999,1000000)
            content = "【雷石KTV】欢迎登陆财务管理账号，账户名为：%s，初始密码：%s。" % (username, password_org)
            msg = await ctrl.pay.send_message_ctl(username=username, password_org=password_org, ktv_id=ktv_id, content=content)
            if msg['type'] == 2:
                return

        await utils.async_common_api('/wx/custom/send', dict(openid=openid, text='https://erp.ktvsky.com/ktv_fin_curdata', msgtype='text', gzh=''))

