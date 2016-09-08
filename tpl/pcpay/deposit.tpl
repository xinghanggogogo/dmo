{% extends 'base.tpl' %}

{% block title %}账户提现{% end %}

{% block container %}
<div id="container">
    <ul class="menu cf">
        <li{% if action == 'deposit' %} class="active"{% end %}><a href="/bill/withdraw/deposit">账户提现</a></li>
        <li{% if action == 'flow' %} class="active"{% end %}><a href="/bill/withdraw/flow">提现流水</a></li>
    </ul>
    <div class="deposit">
        <ul class="cf">
            <li class="f14"><label>账面总金额：</label><span class="b">{{ int(bank_info['total_money']) / 100 }}元</span></li>
            <li>
                <label class="f14">可提现金额：</label><span class="b f14">{{ int(bank_info['withdraw_money']) / 100 }}元</span>
                <div class="detail"><span class="wx">{{ int(bank_info['wx_money']) / 100 }}</span><span class="ali">{{ int(bank_info['ali_money']) / 100 }}</span><span class="pos">{{ int(bank_info['pos_money']) / 100 }}</span></div>
            </li>
            <li class="card-list">
                <label class="f14">选择到账银行：</label>
                <dl class="active" data-extra="0" title="{{ bank_info['bank_account'] }}">
                    <dt>{{ bank_info['bank_name'] }}</dt>
                    <dd>
                        <em>开户名称</em><span>{{ bank_info['account_name'] }}</span>
                    </dd>
                    <dd>
                        <em>开户支行</em><span>{{ trim(bank_info['bank_branch'], 12) }}</span>
                    </dd>
                    <dd>
                        <em>银行卡号</em><span>{{ trim(bank_info['bank_account'], 12) }}</span>
                    </dd>
                    <dd>
                        <em>联系方式</em><span>{% if bank_info['bank_phone'] %}{{ bank_info['bank_phone'] }}{% else %}<input type="text" name="bank_phone" placeholder="请输入您的手机号" maxlength="11" />{% end %}</span>
                    </dd>
                </dl>
                {% if bank_info['extra_bank'] %}
                <dl data-extra="1" title="{{ bank_info['extra_bank']['bank_account'] }}">
                    <dt>{{ bank_info['extra_bank']['bank_name'] }}</dt>
                    <dd>
                        <em>开户名称</em><span>{{ bank_info['extra_bank']['account_name'] }}</span>
                    </dd>
                    <dd>
                        <em>开户支行</em><span>{{ trim(bank_info['extra_bank']['bank_branch'], 12) }}</span>
                    </dd>
                    <dd>
                        <em>银行卡号</em><span>{{ trim(bank_info['extra_bank']['bank_account'], 12) }}</span>
                    </dd>
                    <dd>
                        <em>联系方式</em><span>{{ bank_info['extra_bank']['bank_phone'] }}</span>
                    </dd>
                </dl>
                {% else %}
                <a href="/bill/withdraw/bank?is_extra=1" class="add-card">添加银行卡</a>
                {% end %}
                <div class="cf"></div>
                <div class="save-tip">
                    <p class="yellow">* 为了您的账户安全，若需要变更到账银行信息请与雷石联系，联系电话：010-51660862-830</p>
                    <p class="yellow">* 到账时间根据到账银行办理时间为准</p>
                </div>
            </li>
            <li class="line">
                <label class="f14">点击进行提现：</label>
                <div class="withdraw">
                    <input type="button" value="提现" id="withdraw" class="btn" />
                </div>
            </li>
        </ul>
    </div>
</div>
{% end %}

{% block foot %}
<script>
(function() {
    $('#withdraw').on('click', function(evt) {
        var active_card_dom = $('.card-list dl.active'),
            is_extra = active_card_dom.attr('data-extra'),
            bank_phone_dom = active_card_dom.find('input[name=bank_phone]'),
            bank_phone = bank_phone_dom.length > 0 ? bank_phone_dom.val() : '',
            phone_reg = /^1([38]\d|4[57]|5[0-35-9]|7[06-8]|8[89])\d{8}$/;
        if (bank_phone_dom.length > 0 && (bank_phone == '' || !phone_reg.test(bank_phone))) {
            alert('联系方式为空或联系方式不是手机号！')
            return
        }
        var state = confirm('尊敬的客户您好，确认提现吗？');
        if (state == true) {
            $.ajax({
                type: 'POST',
                url: '/withdraw',
                data: {
                    is_extra: is_extra,
                    bank_phone: bank_phone
                },
                dataType: 'json',
                success: function(response) {
                    if (response.errcode == 200) {
                        alert('提现成功，雷石会第一时间安排人员给您打款。')
                    } else {
                        alert(response.errmsg)
                    }
                    location.reload(true)
                }
            })
        }
    })
    $('.card-list dl').on('click', function(evt) {
        $('.card-list dl').removeClass('active')
        $(this).addClass('active')
    })
})()
</script>
{% end %}
