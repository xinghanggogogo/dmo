{% extends 'base.tpl' %}

{% block title %}账户提现{% end %}

{% block head %}
    <link rel="stylesheet" href="{{ static_url('css/pay_cash.css') }}" />
{% end %}

{% block content %}
    <input type="hidden" value="{{ ktv['store_id'] }}" id=ktvId />
	<header>
		<p class="naTitle">账户总金额(元)</p>
		<font class="balance" id=withdraw_money>{{withdraw_info['total_money']/100}}</font>
		{% if bank_info_exist %}
            <div class="note">
                {% if ser_info %}
                <p>离服务到期仅剩：&nbsp;{{ser_info['days_left']}}天</p>
                {% end %}
                <p class="seeNote">查看提现记录</p>
            </div>
		{% end %}
	</header>
	<div class="masking"></div>
	{% if bank_info_exist %}
        <div class="warpAll" id="cash">	   <!--提现信息-->
                {% if ser_info %}
                <div class="meals">    <!--套餐信息-->
                    <P>90后服务费</P>
                    <ul>
                        {% if ser_info['contract_left']>=1 and ser_info['contract_left']<=3 %}
                            <li>
                                <div class="mealInfo">
                                    <p class="time"><span class="time_num">1</span>个月</p>
                                </div>
                                <p class="money">￥<span>{{ser_info['month_price']*1}}</span></p>
                            </li>
                        {% elif ser_info['contract_left']>=3 %}
                            <li>
                                <div class="mealInfo">
                                    <p class="time"><span class="time_num">3</span>个月</p>
                                </div>
                                <p class="money">￥<span>{{ser_info['month_price']*3}}</span></p>
                            </li>
                        {% elif ser_info['contract_left']>=6 %}
                            <li>
                                <div class="mealInfo">
                                    <p class="time"><span class="time_num">6</span>个月</p>
                                </div>
                                <p class="money">￥<span>{{ser_info['month_price']*6}}</span></p>
                            </li>
                        {% elif ser_info['contract_left']>=12 %}
                            <li>
                                <div class="mealInfo">
                                    <p class="time"><span class="time_num">12</span>个月</p>
                                </div>
                                <p class="money">￥<span>{{ser_info['month_price']*12}}</span></p>
                            </li>
                        {% end %}
                    </ul>
                </div>
                {% end %}
            <div class="cashInfo">    <!--提现信息-->
                <div
                    <p>可提现金额</p>
                </div>
                <div>
                    <span class="cashMoney" id="cashMoney">{{ withdraw_info['withdraw_money']/100 }}元</span>
                    <p class="type"><span id="wx">{{ withdraw_info['wx_money']/100 }}</span><span id="ali">{{ withdraw_info['ali_money']/100 }}</span><span id="pos">{{ withdraw_info['pos_money']/100 }}</span></p>
                    <p class="xgtc">已选购<span class="tc"></span></p>
                </div>
                <button {% if withdraw_info['withdraw_money']<=0 %} class="btn" {% else %} class="btn isbtn" {% end %} id="cashBtn">提现</button>
                <a href="/ktv_fin_wd_rules" class="ruleBtn">提现规则</a>

            </div>
            <div id="cashInfo">   <!--提现的账户信息-->
                <p>到账银行信息</p>
                <div class="accountInfo">
                    <p>开户名称:{{withdraw_info['account_name']}}</p>
                    <p>开户银行:{{withdraw_info['bank_name']}}</p>
                    <p>开户支行:{{withdraw_info['bank_branch']}}</p>
                    <p>银行卡号:{{withdraw_info['bank_account']}}</p>
                    <p>联系方式:{{withdraw_info['bank_phone']}}</p>
                </div>
                <p class="alter">若变更到账银行信息请与雷石联系<a href="tel:13911219708" id="phone">18601045362</a></p>
            </div>
        </div>
	{% else %}
        <div class="warpAll" id="bankInfo">
            <p>请慎重填写以下到账银行账户信息:</p>
            <div class="bankInfo">
                <p><span class="name">开户名称</span><input name="account_name" placeholder="例:公司/个人" value="{{ktv['account_name']}}"/></p>
                    <span>个人账户请填写开户人姓名；<br/>公司账户请与营业执照登记公司名称一致；</span>
                <p><span class="name">开户银行</span><input name="bank_name" placeholder="例:浦发银行" value="{{ktv['bank_name']}}"/></p>
                <p><span class="name">开户支行</span><input name="bank_branch" placeholder="例:北苑支行" value="{{ktv['bank_branch']}}" /></p>
                    <span>请填写完整的支行信息，避免银行到帐失败</span>
                <p><span class="name">银行卡号</span><input type="tel" name="bank_account" placeholder="请输入银行卡卡号" value="{{ktv['bank_account']}}" maxlength="21"/></p>
                <p><span class="name">联系方式</span><input type="tel" name="bank_phone" placeholder="请输入联系方式" value="{{ktv['bank_phone']}}" maxlength="11"/></p>
            </div>
            <button class="btn isbtn" id="bankBtn">确认提交</button>
        </div>
	{% end %}
	<div class="confirm">     <!--提示信息-->
		<p class="xgtc">已选购<span class="tc">￥-<span class="mealMoney"></span><span class="mealDesc"></span></span></p>
		<p class="esta">确认银行信息填写无误,<br/>一经提交不得更改！</p>
		<div class="isTrue">
			<span name="false">否</span>
			<span name="true">是</span>
		</div>
	</div>
	<div class="warpAll cashNotes">    <!--cash notes-->
		<p>提现记录<span>(元)</span></p>
            <ul class="cashState"></ul>
            <p class="noNote">暂无更多记录</p>
		<div class="detail">
			<div class="ds">
				<font class="dealMoney"></font>
				<p>提现金额（元）</p>
			</div>
			<div class="des">
				<p>提款状态:<span class="state dealTrue"></span></p>
				<p class="rout"></p>
				<p class="wx"><span class="wxM"></span> 手续费 -<span class="wxCost"></span></p>
				<p class="ali"><span class="aliM"></span> 手续费 -<span class="aliCost"></span></p>
				<p class="pos"><span class="posM"></span> 手续费 -<span class="posCost"></span></p>
				<p class="wireDate"></p>
				<p class="applyDate"></p>
			</div>
		</div>
	</div>
	<div class="modul">
		<p></p>
	</div>
{% end %}

{% block script %}
    <script type="text/javascript" src="{{ static_url('js/cash.js') }}"></script>
{% end %}
