<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf8"/>
        <title>{% block title %}{% end %} - 财务小组手</title>
        <link href="{{ static_url('css/erp.css') }}" rel="stylesheet" type="text/css" />
        <script type="text/javascript" src="{{ static_url('lib/jquery-1.7.1.min.js') }}"></script>
        {% block head %}{% end %}
    </head>
    <body>
        <div id="top-header" class="cf">
            <ul>
                <li{% if top_cate == 'stat' %} class="active"{% end %}><a href="/bill/stat">营收统计</a></li>
                <li{% if top_cate == 'order' %} class="active"{% end %}><a href="/bill/order/wechat">进出账流水</a></li>
                <li{% if top_cate == 'withdraw' %} class="active"{% end %}><a href="/bill/withdraw/deposit">账户提现</a></li>
            </ul>
            <p>
                <a href="javascript: location.reload(true)" class="refresh">页面刷新</a>
                <img class="logo" src="{{ static_url('images/logo.png') }}" />
            </p>
        </div>
        {% block container %}{% end %}
        {% block foot %}{% end %}
    </body>
</html>
