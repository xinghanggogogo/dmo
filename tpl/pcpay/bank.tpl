{% extends 'base.tpl' %}

{% block title %}添加银行卡{% end %}

{% block container %}
<div id="container">
    <ul class="menu cf">
        <li{% if action == 'deposit' %} class="active"{% end %}><a href="/bill/withdraw/deposit">账户提现</a></li>
        <li{% if action == 'flow' %} class="active"{% end %}><a href="/bill/withdraw/flow">提现流水</a></li>
    </ul>
    <div class="bank-edit">
        <p class="total">账户金额<span>{{ int(bank_info['total_money']) / 100 }}</span>元</p>
        <p class="tip">请慎重填写以下到账银行账户信息:</p>
        <form method="POST">
            <input type="hidden" name="is_extra" value="{{ is_extra }}" />
            <ul>
                <li><label>开户名称</label><input class="text" type="text" name="account_name" placeholder="例:公司/个人" /></li>
                <li class="exp">个人账户请填写开户人姓名;<br/>公司账户请与营业执照登记公司名称一致</li>
                <li><label>开户银行</label><input class="text" type="text" name="bank_name" placeholder="例:浦发银行" /></li>
                <li><label>开户支行</label><input class="text" type="text" name="bank_branch" placeholder="例:北京北苑支行" /></li>
                <li class="exp">完整的支行信息,避免银行转账失败</li>
                <li><label>银行卡号</label><input class="text" type="text" name="bank_account" placeholder="请输入银行卡卡号" /></li>
                <li><label>联系方式</label><input class="text" type="text" name="bank_phone" placeholder="请输入您的手机号" maxlength="11" /></li>
                <li><input type="submit" value="提交" class="btn submit" /></li>
            </ul>
        </form>
    </div>
</div>
{% end %}

{% block foot %}
<script>
(function() {
    $('form').submit(function(evt) {
        var form_data = $(this).serializeArray(),
            flag = true,
            phone_reg = /^1([38]\d|4[57]|5[0-35-9]|7[06-8]|8[89])\d{8}$/;
            account_reg = /\d{6,}/,
            json_data = {};
        for (var i = 0, len = form_data.length; i < len; i++) {
            var name = form_data[i].name,
                value = form_data[i].value;
            if (name == 'bank_phone' && !phone_reg.test(value)) {
                flag = false
                break
            }
            if (name == 'bank_account' && !account_reg.test(value)) {
                flag = false
                break
            }
            if (value == '') {
                flag = false
                break
            }
            json_data[name] = value
        }
        if (flag == false) {
            alert('银行信息为空或联系方式不是手机号！')
            evt.preventDefault()
            return
        }
        var state = confirm('为了保障您的账户安全，请确认银行信息填写无误！')
        if (state == true) {
            $.ajax({
                type: 'POST',
                url: '/bank',
                data: json_data,
                dataType: 'json',
                success: function(response) {
                    if (response.errcode == 200) {
                        alert('恭喜您，银行信息保存成功，马上就可以提现了。')
                        location.href = '/bill/withdraw/deposit'
                    } else {
                        alert(response.errmsg)
                    }
                }
            })
        }
        evt.preventDefault()
    })
})()
</script>
{% end %}
