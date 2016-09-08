#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.sql.expression import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TINYINT, DATETIME

from settings import DB_
from mysql.base import NotNullColumn, Base
from lib.decorator import model_to_dict, filter_update_data, models_to_list


class Cashier(Base):
    __tablename__ = 'cashier'

    cashier_id = Column(INTEGER(11), primary_key=True)
    nickname = NotNullColumn(VARCHAR(64), default='')
    headimgurl = NotNullColumn(VARCHAR(512), default='')
    ktv_id = NotNullColumn(INTEGER(11))
    client_id = NotNullColumn(INTEGER(11))
    openid = NotNullColumn(VARCHAR(64), default='')
    total_cash = NotNullColumn(INTEGER(11), default=0)
    score = NotNullColumn(INTEGER(11), default=0)
    ac_task = NotNullColumn(VARCHAR(64), default='0, 0')
    sp_task = NotNullColumn(VARCHAR(64), default='0, 0')
    info = NotNullColumn(VARCHAR(64), default='')


class CashierWithdraw(Base):
    __tablename__ = 'cashier_withdraw'

    withdraw_id = Column(INTEGER(11), primary_key=True)
    openid = NotNullColumn(VARCHAR(64))
    withdraw_money = NotNullColumn(INTEGER(11))


class KtvFinanceAccount(Base):
    __tablename__ = 'ktv_finance_account'

    id = Column(INTEGER(11), primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11),default=0)
    username = NotNullColumn(INTEGER(11),default=0)
    password_org = NotNullColumn(VARCHAR(11), default='')
    password = NotNullColumn(VARCHAR(32), default='')


class ServiceInfo(Base):
    __tablename__ = 'ktv_service_info'

    id = Column(INTEGER(11),primary_key=True)
    ktv_id = NotNullColumn(INTEGER(11),default=0)
    ser_fee = NotNullColumn(INTEGER(11))
    ser_period = NotNullColumn(INTEGER(11))
    invoice = NotNullColumn(TINYINT(1),default=0)
    phone_num = NotNullColumn(VARCHAR(11),default='')
    contract_period= NotNullColumn(INTEGER(5), default=0)
    pay_cycle = NotNullColumn(INTEGER(5), default=0)
    month_price = NotNullColumn(INTEGER(5), default=0)
    auth_endtime = NotNullColumn(DATETIME, default=func.now())
    pay_mode = NotNullColumn(TINYINT(1), default=0)
    room_count = NotNullColumn(INTEGER(5), default=0)


class APIModel(object):

    def __init__(self, pdb):
        self.pdb = pdb
        self.master = pdb.get_session(DB_KTV, master=True)
        self.slave = pdb.get_session(DB_KTV)

    @model_to_dict
    def get_cashier(self, ktv_id=None, client_id=None, openid=None):
        q = self.slave.query(Cashier)
        if ktv_id and client_id:
            q = q.filter_by(ktv_id=ktv_id).filter_by(client_id=client_id)
            q = q.order_by(Cashier.update_time.desc()).limit(1)
        if openid:
            q = q.filter_by(openid=openid)
        return q.scalar()

    @filter_update_data
    def update_cashier(self, openid, data):
        self.master.query(Cashier).filter_by(openid=openid).update(data)
        self.master.commit()

    @model_to_dict
    def add_cashier(self, **data):
        cashier = Cashier(**data)
        self.master.add(cashier)
        self.master.commit()
        return cashier

    def cal_withdraw_sum(self, openid):
        q = self.slave.query(func.sum(CashierWithdraw.withdraw_money).label('withdraw_money')).filter_by(openid=openid)
        return q.scalar() or 0

    @model_to_dict
    def add_cashier_withdraw(self, **data):
        cashier_withdraw = CashierWithdraw(**data)
        self.master.add(cashier_withdraw)
        self.master.commit()
        return cashier_withdraw

    @model_to_dict
    def get_ktv_fin_account(self, username):
        return self.slave.query(KtvFinanceAccount).filter_by(username=username).scalar()

    @model_to_dict
    def get_ktv_fin_account_from_ktv_id(self, ktv_id):
        return self.slave.query(KtvFinanceAccount).filter_by(ktv_id=ktv_id).scalar()

    def update_ktv_fin_account(self, **data):
        q = self.master.query(KtvFinanceAccount).filter_by(username=data['username'])
        if q.scalar():
            q.update(data)
        else:
            self.master.add(KtvFinanceAccount(data))
        self.master.commit()

    @model_to_dict
    def insert_ser_info(self, **params):
        self.master.add(ServiceInfo(**params))
        self.master.commit()
        return ServiceInfo(**params)

    @model_to_dict
    def get_ktv_ser_order(self, tradeno):
        return self.slave.query(ServiceInfo).filter_by(id=tradeno).scalar()

