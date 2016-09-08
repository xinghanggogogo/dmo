{% extends 'base.tpl' %}

{% block title %}实时数据{% end %}

{% block head %}
    <link rel="stylesheet" href="{{ static_url('css/pay_realData.css')}} " />
    <script type="text/javascript" src="http://cdn.hcharts.cn/jquery/jquery-1.8.3.min.js"></script>
	<script type="text/javascript" src="http://cdn.hcharts.cn/highcharts/highcharts.js"></script>
	<script type="text/javascript" src="{{ static_url('lib/jquery.circliful.min.js') }}" ></script>
{% end %}

{% block content %}
    <input type="hidden" value="{{ user['ktv_id'] }}" id="ktvId"/>
	<div class="warpAll">
		<header>
			<p >今日营收总金额(元)</p>
			<h1 class="nowMoney">{{ float(today_revenue['TotalAmount']) }}</h1>
			<div class="compare">
			    <p>开房率:<span {% if (float(today_revenue['OpenCount'])/float(today_revenue['RoomCount']))<0 %}
                class="down" {% else %} class="up" {% end %}>{{ '%.02f' % ((float(today_revenue['OpenCount'])/float(today_revenue['RoomCount']))*100) }}%</span><i></i></p>
				<p>预定率:<span {% if (float(today_revenue['BookCount'])/float(today_revenue['RoomCount']))<0 %}
                class="down" {% else %} class="up" {% end %}>{{ '%.02f' % ((float(today_revenue['BookCount'])/float(today_revenue['RoomCount']))*100) }}%</span><i></i></p>
			</div>
			<p class="rose">同比昨日涨幅（流水:{{ float(yesterday_revenue['TotalAmount']) }}）</p>
			<div class="compare">
				{% if float(yesterday_revenue['TotalAmount']) != 0 %}
				<p>营收:<span {% if (float(today_revenue['TotalAmount'])-float(yesterday_revenue['TotalAmount']))<0 %}
                class="down" {% else %} class="up" {%end%}>{{ '%.02f' % ((float(today_revenue['TotalAmount'])-float(yesterday_revenue['TotalAmount']))/float(yesterday_revenue['TotalAmount'])*100) }}%</span><i></i></p>
				{% else %}
				<p><span>昨日营收为空</span></p>
				{% end %}
                <p>开房率:<span {% if (float(today_revenue['OpenCount'])-float(yesterday_revenue['OpenCount']))<0 %}
                class="down" {% else %} class="up" {% end %}>{{ '%.02f' % (((float(today_revenue['OpenCount'])/float(today_revenue['RoomCount']))*100)-(float(yesterday_revenue['OpenCount'])/float(yesterday_revenue['RoomCount'])*100)) }}%</span><i></i></p>
                <p>预定量:<span {% if (float(today_revenue['BookCount'])-float(yesterday_revenue['BookCount']))<0 %}
                class="down" {% else %} class="up" {% end %}>{{ '%.02f' % (((float(today_revenue['BookCount'])/float(today_revenue['RoomCount']))*100)-(float(yesterday_revenue['BookCount'])/float(yesterday_revenue['RoomCount'])*100)) }}%</span><i></i></p>
			</div>
		</header>
		<article>
			<div class="graphs">
				<div class="charts">
					<h1 class="time">今日流水</h1>
					<p class="totalMoney">共计：</p>
					<div id="dayAocc" class="chart"></div>
				</div>
				<div class="charts">
					<h1 class="time">月流水</h1>
					<p class="totalMoney">共计：</p>
					<p class="date"></p>
					<div id="monthAocc" class="chart"></div>
				</div>
				<div class="charts">
					<h1 class="time">年流水</h1>
					<p class="totalMoney">共计：</span></p>
					<p class="date"></p>
					<div id="yearAocc" class="chart"></div>
				</div>
			</div>
			<div class="pieChart">
				<p>营收分布占比</p>
				<div id="pieChart" class="chart"></div>
			</div>
			<div class="ringChart">
				<p>支付方式占比</p>
				<div class="ringList"></div>
			</div>
		</article>
	</div>
{% end %}

{% block script %}
    <script type="text/javascript" src="{{ static_url('js/realData.js') }}"></script>
{% end %}
