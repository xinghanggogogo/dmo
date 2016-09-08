{% extends 'base.tpl' %}

{% block title %}提现规则{% end %}

{% block head %}
<style>
    .title{text-align:center;font-size:.4rem;padding:.4rem}p,strong,table{margin:0 .24rem;font-size: .18rem;}strong{margin:.24rem;display:inline-block}.tx{font-size:.3rem}p{line-height:22px;text-indent:20px}table{border-collapse:collapse;text-align:center;width:90%;margin-left:5%;color:#353535;font-size:.26rem}table td,table tr{border:solid 1px #454545}table tr td{padding:8px 4px;width:25%}table tr:first-child{font-weight:700;color:#454545}
</style>
{% end %}

{% block content %}
	<h1 class="title">雷石支付平台政策通知</h1>
	<p class="zw">为了满足客户需求，方便客户使用，雷石公司特推出雷石支付平台。雷石支付平台包含：微信支付、支付宝支付、雷石智能移动POS机支付。</p>
	<strong class="tx">雷石支付平台提现及手续费模式：</strong>
	<table>
		<tr>
			<td>支付方式</td>
			<td>提现周期</td>
			<td>支付手续费</td>
			<td nowrap="nowrap">提现汇款手续费</td>
		</tr>
		<tr>
			<td rowspan="2">微信支付</td>
			<td>T+1</td>
			<td>0.69%</td>
			<td>商家付</td>
		</tr>
		<tr>
			<td>每周二（法定节假日除外）</td>
			<td>0.39%</td>
			<td>雷石付</td>
		</tr>
		<tr>
			<td>支付宝支付</td>
			<td>每周二（法定节假日除外）</td>
			<td>0.7%</td>
			<td>商家付</td>
		</tr>
		<tr>
			<td rowspan="2">POS机支付</td>
			<td>T+1</td>
			<td>0.69%</td>
			<td>商家付</td>
		</tr>
		<tr>
			<td>每周二（法定节假日除外</td>
			<td>0.39%</td>
			<td>雷石付</td>
		</tr>
	</table>
	<strong style="margin-bottom: 2rem;">依据国家政策规定手续费如有调整，以书面通知为准。</strong>
{% end %}
