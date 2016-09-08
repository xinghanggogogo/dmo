#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import datetime
import xml2json
import optparse

from lib import utils
from lib.decorator import wx_auth
from handler.base import BaseHandler
from control import ctrl
from urllib.parse import quote, unquote
from tornado.httputil import url_concat
from settings import CUR_AC_TASK_DST, WX_CONF, WX_USERINFO_GRANT_URL, WX_REDIRECT_URL, FETCH_OPENID_URL,\
                                     AC_TASK_REWARD, SP_TASK_REWARD, FETCH_USERINFO_URL, QRCODE_TICKET, FETCH_USERINFO_URL_V2,\
                                     RED_PACK_TEMPLATE_ID, TEMPLATE_MSG_URL


class FetchQrcodeHandler(BaseHandler):

    async def get(self):
        try:
            ktv_id = int(self.get_argument('ktv_id'))
            client_id = int(self.get_argument('client_id'))
        except Exception as e:
            logging.error(e)
            return self.send_json(errcode=10001)

        try:
            response = await utils.async_common_api('/wx/arged/qrcode', dict(flag=1, arg='%s,%s'%(ktv_id, client_id)))
            return self.send_json({'url': response['url']})
        except Exception as e:
            logging.error(e)
            return self.send_json(errcode=50001)


class CashierHomeHandler(BaseHandler):

    @wx_auth
    async def get(self):
        openid = self.get_cookie('openid')
        if not openid:
            openid = self.get_argument('openid', '')
        if not openid:
            return self.render('go to cashier home page error')
        cashier = ctrl.erp.get_cashier_ctl(openid)
        if not cashier:
            return self.render('cashier.home.tpl', cashier={}, config=dict(appId='', timestamp='', nonceStr='', signature=''), withdrawed=0)

        level_list = []
        ac_task = list(map(int, cashier['ac_task'].split(',')))
        cur_ac_task_dst = CUR_AC_TASK_DST if ac_task[1]==0 else 1000
        level_list.append(dict(type='ac_task', title='每累计%d元' % cur_ac_task_dst, level=ac_task[1], cur=ac_task[0], dst=cur_ac_task_dst, reward=AC_TASK_REWARD))
        sp_task = list(map(int, cashier['sp_task'].split(',')))
        level_list.append(dict(type='sp_task', title='每笔满1000元', level=sp_task[1], cur=0, dst=sp_task[0], reward=SP_TASK_REWARD))
        cashier.update({'tasks': level_list})

        config = await utils.async_common_api('/wx/share/config', dict(url=self.request.full_url()))
        ktv = await utils.async_common_api('/kinfo/%s' % cashier['ktv_id'])
        cashier.update({'ktv': ktv.get('name')})

        withdrawed = ctrl.erp.cal_withdraw_sum(openid)
        return self.render('cashier.home.tpl', cashier=cashier, config=config, withdrawed=withdrawed)


class WxCallBackHandler(BaseHandler):

    async def _get_openid(self, code):
        key = 'code_%s' % code
        v = ctrl.rs.get(key)
        if v:
            return v.decode()
        url = FETCH_OPENID_URL.format(appid=WX_CONF['appid'], secret=WX_CONF['appsecret'], code=code)
        http_client = utils.get_async_client()
        request = utils.http_request(url)
        response = await http_client.fetch(request)
        response = json.loads(response.body.decode())
        logging.info(response)
        ctrl.rs.set(key, response['openid'], 10*60)
        return response['openid']

    async def get(self):
        state = self.get_argument('state', '/cashier/home')
        code = self.get_argument('code', '')
        if code:  # 有code, 是已经授权跳转回来的, 则获取openid
            openid = await self._get_openid(code)
            self.set_cookie('openid', openid)
            return self.redirect(unquote(state))

        url = WX_USERINFO_GRANT_URL.format(
            appid=WX_CONF['appid'],
            redirect_uri=quote(WX_REDIRECT_URL),
            state=state
        )
        # 跳转去授权
        return self.redirect(url)


class EventCallBackHandler(BaseHandler):

    def get(self):
        '''用于绑定消息推送地址'''
        self.write(self.get_argument('echostr'))

    async def update_cashier(self, ktv_id, client_id, openid):
        cashier = ctrl.erp.get_cashier_ctl(openid)
        if not cashier:
            await self.insert_cashier(openid, ktv_id, client_id)
            return

        if cashier['ktv_id'] != ktv_id or cashier['client_id'] != client_id:
            data = dict(ktv_id=ktv_id, client_id=client_id)
            ctrl.erp.update_cashier_ctl(openid, data)

    async def get_user_info(self, openid):
        try:
            access_token = await utils.async_common_api('/wx/token', dict(flag=1))
        except Exception as e:
            logging.error(e)
            raise

        url = FETCH_USERINFO_URL_V2.format(access_token=access_token['accec_token'], openid=openid)
        http_client = utils.get_async_client()
        request = utils.http_request(url)
        response = await http_client.fetch(request)
        response = json.loads(response.body.decode())
        return response

    async def insert_cashier(self, openid, ktv_id, client_id):
        try:
            userinfo = await self.get_user_info(openid)
        except Exception as e:
            logging.error(e)
            raise
        ctrl.erp.add_cashier_ctl(ktv_id, client_id, openid, userinfo['headimgurl'], userinfo['nickname'])

    async def post(self):
        msg = self.request.body
        msg_dict = json.loads(xml2json.xml2json(msg.decode(), optparse.Values({'pretty': True})))
        logging.error(msg_dict)

        msg_dict = msg_dict.get('xml', {})
        event = msg_dict.get('Event', '')
        openid = msg_dict.get('FromUserName', '')
        ktvid_and_clientid = msg_dict.get('EventKey', '')
        if event not in ('subscribe', 'SCAN') or not ktvid_and_clientid or not openid:
            return

        if event == 'SCAN':
            ktvid_clientid_list = list(map(int, ktvid_and_clientid.split(',')))
        else:
            ktvid_clientid_list = list(map(int, ktvid_and_clientid.split('_')[1].split(',')))
            # 关注发送消息
            await utils.async_common_api('/wx/custom/send', dict(openid=openid, text='欢迎进入收银员等级认证系统', msgtype='text', gzh='lsfwh'))
        await self.update_cashier(ktvid_clientid_list[0], ktvid_clientid_list[1], openid)


class CashierGradeHandler(BaseHandler):

    async def get(self):
        try:
            openid = self.get_argument('openid')
        except Exception as e:
            logging.error(e)
            return self.send_json(errcode=10001)

        cashier = ctrl.erp.get_cashier_ctl(openid)
        if not cashier:
            return self.send_json(errcode=40004)

        level_list = []
        ac_task = list(map(int, cashier['ac_task'].split(',')))
        cur_ac_task_dst = CUR_AC_TASK_DST if ac_task[1]==0 else 1000
        level_list.append(dict(type='ac_task', title='每累计%s元'%cur_ac_task_dst, level=ac_task[1], cur=ac_task[0], dst=cur_ac_task_dst))
        sp_task = list(map(int, cashier['sp_task'].split(',')))
        level_list.append(dict(type='sp_task', title='每笔满1000元', level=sp_task[1], cur=0, dst=sp_task[0]))

        bg_img_url = ctrl.erp.get_cashier_grade_bg_img_url_ctl()
        res = dict(list=level_list, pic=bg_img_url)
        self.send_json(res)


class CashierOpenidHandler(BaseHandler):

    def get(self, ktv_id, client_id):
        info = self.get_argument('info', '')
        cashier = ctrl.erp.get_cashier(ktv_id, client_id)
        openid = '' if not cashier else cashier['openid']
        if openid and info:
            ctrl.erp.update_cashier(openid, dict(info=info))

        return self.send_json({'openid': openid})


class CashierVersionHandler(BaseHandler):

    def get(self):
        cashier_version = ctrl.erp.get_cashier_version_ctl()
        return self.send_json(cashier_version)


class AfterPayHandler(BaseHandler):

    def post(self):
        try:
            openid = self.get_argument('openid')
            fee = int(self.get_argument('fee'))
        except Exception as e:
            logging.error(e)
            return self.send_json(errcode=10001)

        fee = fee // 100
        cashier = ctrl.erp.get_cashier_ctl(openid)
        if not cashier:
            return self.send_json({})

        total_cash = cashier['total_cash']
        data = dict()
        ac_task = list(map(int, cashier['ac_task'].split(',')))
        ac_task[0] += fee
        if ac_task[1] == 0:
            if ac_task[0] >= 500:
                ac_task[0] -= 500
                total_cash += AC_TASK_REWARD
                ac_task[1] += 1
        ac_task[1] += ac_task[0] // 1000
        total_cash += AC_TASK_REWARD * ac_task[0] // 1000
        ac_task[0] %= 1000
        data.update({'ac_task': ','.join(list(map(str, ac_task)))})

        if fee >= 1000:
            sp_task = list(map(int, cashier['sp_task'].split(',')))
            sp = fee // 1000
            sp_task[1] += sp
            total_cash += SP_TASK_REWARD * sp
            data.update({'sp_task': ','.join(list(map(str, sp_task)))})
        data.update({'total_cash': total_cash})
        ctrl.erp.update_cashier_ctl(openid, data)
        self.send_json({})

    def get(self):
        # 用于别人测试方便
        self.post()


class WithdrawHandler(BaseHandler):

    async def post(self):
        try:
            openid = self.get_argument('openid')
            lock_key = 'cash_withdraw_%s'%openid
            assert ctrl.rs.setnx(lock_key, 1)
            ctrl.rs.expire(lock_key, 60*10)
        except Exception as e:
            logging.error(e)
            return self.send_json(errcode=10001)

        cashier = ctrl.erp.get_cashier_ctl(openid)
        withdrawed = ctrl.erp.cal_withdraw_sum(openid)
        total_amount = cashier['total_cash'] - withdrawed
        if total_amount < 10:
            logging.info('openid: %s, money less than 10, but still call this api' % openid)
            return self.send_json({'errmsg': 'money less than 10, cannot withdraw'})
        withdraw_money = 200 if total_amount > 200 else total_amount

        response = await utils.async_common_api('/wx/redpack', dict(flag=1, openid=openid, total_amount=withdraw_money * 100, gzh='lsfwh'))
        logging.error('openid: %s, cashier withdraw result: %s' % (openid, response))
        result, errmsg = 0, ''
        if response.get('result_code') == 'SUCCESS':
            result = 1
            errmsg = response.get('return_msg')
            ctrl.erp.add_cashier_withdraw(openid=openid, withdraw_money=withdraw_money)
        self.send_json({'sum': total_amount, 'result': result, 'errmsg': errmsg})
        ctrl.rs.delete(lock_key)

