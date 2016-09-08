{% extends 'base.tpl' %}

{% block title %}进出账流水{% end %}

{% block head %}
<link href="{{ static_url('lib/pickerdate.min.css') }}" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="{{ static_url('lib/moment.min.js') }}"></script>
<script type="text/javascript" src="{{ static_url('lib/pickerdate.min.js') }}"></script>
{% end %}

{% block container %}
<div id="container" class="cf">
    <ul class="menu cf">
        <li{% if pay_type == 'wechat' %} class="active"{% end %}><a href="/bill/order/wechat">微信支付</a></li>
        <li{% if pay_type == 'alipay' %} class="active"{% end %}><a href="/bill/order/alipay">支付宝</a></li>
        <li{% if pay_type == 'pos' %} class="active"{% end %}><a href="/bill/order/pos">POS机</a></li>
    </ul>
    <div id="left-container">
        <div class="table">
            {% if pay_type in ('wechat', 'alipay') %}
            <table border="0">
                <thead>
                    <tr>
                        <th class="index">序号</th>
                        <th>线上订单号</th>
                        <th>订单金额</th>
                        <th>手续费/电影版权费</th>
                        <th>净收入</th>
                        <th>手续费返还</th>
                        <th>订单创建时间</th>
                        <th>支付类型</th>
                        <th>订单详情</th>
                    </tr>
                </thead>
                <tbody>
                    {% if orders %}
                    {% for index, order in enumerate(orders) %}
                    <tr>
                        <td>{{ page_size * (page - 1) + index + 1 }}</td>
                        <td>{{ order['order_id'] }}</td>
                        <td>{{ order['total_fee'] / 100 }}元</td>
                        <td>{{ order['rate_fee'] / 100 }}元</td>
                        <td>{{ (order['total_fee'] - order['rate_fee']) / 100 }}元</td>
                        <td>{{ order['coupon_fee'] / 100 }}元</td>
                        <td>{{ order['create_time'] }}</td>
                        <td>{{ order_action_to_text(order['action']) }}</td>
                        <td title="{{ order['body'] }}">{{ trim(order['body'], 6) }}</td>
                    </tr>
                    {% end %}
                    {% else %}
                    <tr><td colspan="9">暂无订单数据</td></tr>
                    {% end %}
                </tbody>
            </table>
            {% else %}
            <table border="0">
                <thead>
                    <tr>
                        <th class="index">序号</th>
                        <th>商户订单号</th>
                        <th>终端号</th>
                        <th>订单金额</th>
                        <th>手续费</th>
                        <th>净收入</th>
                        <th>手续费返还</th>
                        <th>订单创建时间</th>
                        <th>订单状态</th>
                    </tr>
                </thead>
                <tbody>
                    {% if orders %}
                    {% for index, order in enumerate(orders) %}
                    <tr>
                        <td>{{ page_size * (page - 1) + index + 1 }}</td>
                        <td>{{ order['order_no'] }}</td>
                        <td>{{ order['term_id'] }}</td>
                        <td>{{ order['amount'] / 100 }}元</td>
                        <td>{{ order['rate_fee'] / 100 }}元</td>
                        <td>{{ (order['amount'] - order['rate_fee']) / 100 }}元</td>
                        <td>{{ order['coupon_fee'] / 100 }}元</td>
                        <td>{{ order['finish_time'] }}</td>
                        <td>已支付</td>
                    </tr>
                    {% end %}
                    {% else %}
                    <tr><td colspan="9">暂无订单数据</td></tr>
                    {% end %}
                </tbody>
            </table>
            {% end %}
        </div>
        {% if handler.request.path.find('search') > 0 %}
            {% if pay_type == 'pos' and pos_list %}
                {% module PageModule(page, page_total, base_url='/bill/search/' + pay_type + '?start_date=' + start_date + '&end_date=' + end_date + '&term_id=' + term_id) %}
            {% else %}
                {% module PageModule(page, page_total, base_url='/bill/search/' + pay_type + '?start_date=' + start_date + '&end_date=' + end_date) %}
            {% end %}
        {% else %}
            {% module PageModule(page, page_total) %}
        {% end %}
    </div>
    <div id="right-container">
        <form method="GET" action="/bill/search/{{ pay_type }}">
            <ul>
                <li><span>开始时间：</span><input id="start_date" name="start_date" type="text" class="text" value="{{ start_date }}" /></li>
                <li><span>结束时间：</span><input id="end_date" name="end_date" type="text" class="text" value="{{ end_date }}" /></li>
                {% if pay_type == 'pos' and pos_list %}
                <li class="pos">
                    <span>终端号：</span>
                    <select name="term_id">
                        <option value="">所有终端</option>
                        {% for index, pos in enumerate(pos_list) %}
                        <option value="{{ pos['term_id'] }}"{% if term_id == pos['term_id'] %} selected="selected"{% end %}>{{ pos['term_id'] }}</option>
                        {% end %}
                    </select>
                </li>
                {% end %}
                <li><input class="btn" type="submit" value="查询" /></li>
                <li><input id="export" value="导出报表" class="btn" type="button" /></li>
            </ul>
        </form>
    </div>
</div>
{% end %}

{% block foot %}
<script>
(function() {
    var DATA = {
        'pay_type': '{{ pay_type }}'
    }

    var start_date = $('#start_date'),
        end_date = $('#end_date');
    var picker_start = new Pikaday({
        field: start_date[0]
    })
    var picker_end = new Pikaday({
        field: end_date[0]
    })
    function date_check(start, end) {
        start = start.val()
        end = end.val()
        if (start == '' || end == '') {
            alert('请选择时间区间！')
            return false
        }
        if (start > end) {
            alert('开始时间不能大于结束时间！')
            return false
        }
        return true
    }

    function date_range(start, end) {
        var range = 0;
        start = start.val()
        end = end.val()
        if (start != '' && end != '') {
            start = start.replace(/-/g, "/")
            end = end.replace(/-/g, "/")
            start = new Date(Date.parse(start))
            end = new Date(Date.parse(end))
            range = (end - start) / 86400000
        }
        return range
    }

    $('form').submit(function(e) {
        return date_check(start_date, end_date)
    })
    $('#export').on('click', function(e) {
        if (date_check(start_date, end_date) == false) {
            return false
        }
        if (date_range(start_date, end_date) > 31) {
            alert('最多导出一个月的流水报表')
            return false
        }
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/account/order',
            data: {
                start_date: start_date.val(),
                end_date: end_date.val(),
                pay_type: DATA['pay_type']
            },
            success: function(response) {
                if (response.errcode == 200 && response.url) {
                    location.href = response.url
                } else {
                    alert(response.errmsg)
                }
            }
        })
        return false
    })
})()
</script>
{% end %}
