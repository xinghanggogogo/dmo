{% extends 'base.tpl' %}

{% block title %}账户提现流水{% end %}

{% block container %}
<div id="container">
    <ul class="menu cf">
        <li{% if action == 'deposit' %} class="active"{% end %}><a href="/bill/withdraw/deposit">账户提现</a></li>
        <li{% if action == 'flow' %} class="active"{% end %}><a href="/bill/withdraw/flow">提现流水</a></li>
    </ul>
    <div class="flow">
        <table>
            <thead>
                <tr>
                    <th class="index">序号</th>
                    <th>到账金额</th>
                    <th>申请时间</th>
                    <th>提款状态</th>
                    <th>微信金额</th>
                    <th>微信手续费</th>
                    <th>支付宝金额</th>
                    <th>支付宝手续费</th>
                    <th>POS金额</th>
                    <th>POS手续费</th>
                    <th>手续费返还</th>
                    <th>划账日期</th>
                </tr>
            </thead>
            <tbody>
                {% for index, order in enumerate(orders) %}
                <tr>
                    <td>{{ page_size * (page - 1) + index + 1 }}</td>
                    <td>{{ order['account_money'] / 100 }}元</td>
                    <td>{{ order['create_time'] }}</td>
                    <td>{{ order['state'] }}</td>
                    <td>{{ order['withdraw_money'] / 100 }}元</td>
                    <td>{{ order['service_charge'] / 100 }}元</td>
                    <td>{{ order['ali_withdraw_money'] / 100 }}元</td>
                    <td>{{ order['ali_service_charge'] / 100 }}元</td>
                    <td>{{ order['pos_withdraw_money'] / 100 }}元</td>
                    <td>{{ order['pos_service_charge'] / 100 }}元</td>
                    <td>{{ order['return_service_charge'] / 100 }}元</td>
                    <td>{{ order['start_date'] }} 至 {{ order['end_date'] }}</td>
                </tr>
                {% end %}
            </tbody>
        </table>
    </div>
    {% module PageModule(page, page_total) %}
</div>
{% end %}
