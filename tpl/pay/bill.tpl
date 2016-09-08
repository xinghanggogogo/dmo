{% extends 'base.tpl' %} {% block title %}-营业流水{% end %} {% block head %}
<link rel="stylesheet" href="{{ static_url('css/pay_bill_style.css') }}" media="screen" title="no title" charset="utf-8">
<link rel="stylesheet" type="text/css" href="{{ static_url('css/pay_calander.css') }}" /> {% end %} {% block content %}
<header>
	<p class="clear"><span class="left">{{ktv['name']}}进出帐流水<span>(元)</span></span><span class="right">筛选<span>（全部）</span></span>
	</p>
</header>
<div class="mask"></div>
<div class="container" data-ktv="{{ ktv['store_id'] }}">
	<div class="main">
		{% if income_list %} {% for income in income_list %}
		<div class="box" data-orderid={{income[ "order_id"]}} data-paytype={{income[ "pay_type"]}} />
		<h2 class="money">{{income['total_fee']/100}}元</h2>
		<p class="return">手续费返还：{{income['rt_rate_fee']}}</p>
		<p class="time">创建时间：{{income['create_time']}} </p>
		<p class="way">{% if income['pay_type'] == 'wechat' %} 支付方式：微信支付 {% elif income['pay_type'] == 'alipay' %} 支付方式：支付宝支付 {% else %} 支付方式：pos机支付 {% end %}</p>
		<p class="odd_number">线下订单号：{{income['erp_id']}}</p>
	</div>
	{% end %} {% else %}
	<div class='box'>
		<h2 class="no_money show">暂无流水记录</h2>
	</div>
	{% end %}
</div>
<div class="choose_details">
	<div class="choose_dif">
		<div class="content">
			<section>
				<ul class="clear">
					<li class="active" data-i="wechat">微信</li>
					<li data-i="alipay">支付宝</li>
					<li data-i='pos'>POS机</li>
				</ul>
			</section>
			<div class="calender">
				<p style="">开始日期：<input type="text" id="date" value="" readonly="readonly" /></p>
				<p style="">结束日期：<input type="text" id="date2" value="" readonly="readonly" /></p>
				<div>
					<button type="button" name="button">查询</button>
				</div>
			</div>
		</div>
	</div>
	<div class="details" id="details">
		<div class="details_con">
			<h2><span class="total_money"></span></h2>
			<p>订单费用（元）</p>
			<div class="status">
				<p>订单状态：<span class="handling active_word"></span></p>
				<p>创建时间：<span class="detail_time"></span></p>
				<p>支付方式：<span class="detail_way"></span></p>
				<p>手续费用：<span class="detail_poundage"></span></p>
				<p>手续费返还：<span class="detail_return"></span></p>
			</div>
			<div class="order">
				<p>线下订单号：<span class="line_out"></span></p>
				<p>商户订单号：<span class="commercial_tenant"></span></p>
				<p>网络单号：<span class="net"></span></p>
				<p>订单详情：
					<div class="goods"></div>
				</p>
			</div>
		</div>
	</div>
</div>
</div>
{% end %} {% block script %}
<script type="text/javascript" src="static/js/bill.js"></script>
<script type="text/javascript" src="static/js/calander.js"></script>
<script type="text/javascript">
	var date = document.getElementById("date");
	var data2 = document.getElementById('date2')
	date.onfocus = function() {
		clander(date)
	}
	data2.onfocus = function() {
		clander(data2);
	}
</script>
{% end %}