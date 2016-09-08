<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>账户提现</title>
    <link href="{{ static_url('css/base.css') }}" rel="stylesheet" type="text/css" />
    <script type="text/javascript" src="{{ static_url('lib/jquery-1.7.1.min.js') }}"></script>
</head>
<body>
    <input type="hidden" value="{{ ktv_id }}" id="ktvId"/>
    <div class="second-header">
        <ul class="list-ls">
            <li><a id="jcz" class='ls' href="/bill/index/{{ ktv_id }}" data-id='3'>进出账流水</a></li>
            <li><a id="tx" class='ls selectOn' href="/bill/withdraw/{{ ktv_id }}" data-id='4'>账户提现</a></li>
        </ul>
        <img class="logo" src="{{ static_url('images/logo.png') }}" />
    </div>
    <div class="tx">
        <ul class="list-zf">
            <li><a class="zf select-on" href="#">账户提现</a></li>
            <li><a class="zf" href="#">提现流水</a></li>
        </ul>
    </div>
    <div id="cashInfo">
        <div class="cash">    <!--账户提现提现-->
            <div class="center">
                <p class="fontWe">账户总金额<span class="marginLeft" id="totalMoney"></span>元</p>
                <p>请慎重填写以下到账银行账户信息:</p>
                <ul class="userInfo">
                    <li>开户名称<input type="text" placeholder="例:公司/个人" /></li><br/>
                    <p class="expl">个人账户请填写开户人姓名;<br/><br/>公司账户请与营业执照登记公司名称一致</p>
                    <li>开户银行<input type="text" placeholder="例:浦发银行"/></li><br/>
                    <li>开户支行<input type="text" placeholder="例:北京北苑支行"/></li><br/>
                    <p class="expl">完整的支行信息,避免银行转账失败</p>
                    <li>银行卡号<input type="text" placeholder="请输入银行卡卡号"/></li><br/>
                    <li>联系方式<input type="text" placeholder="请输入联系方式" maxlength="11" class="phone"/></li><br/>
                    <li><input type="button" value="确认保存" id="saveInfo" onclick="saveInfo()"/></li>
                </ul>
                <p class="fontWe">可提现金额<span class="marginLeft" id="withMoney"></span>元</p>
                <p><span id="wx"></span><span id="ali"></span><span id="pos">0.00</span></p>
            </div>
            <div style="text-align: center;margin-bottom: 20px;">
                <input type="button" id="txButton" value="提现" onclick="postal()"/>
            </div>
            <p class="gz">到账时间根据到账银行办理时间为准</p>
        </div>
    </div>
    <div id="cashNotes">   <!--提现流水-->
        <table>
            <thead>
                <tr>
                    <th>序号</th>
                    <th>微信提取金额</th>
                    <th>微信手续费用</th>
                    <th>支付宝提现金额</th>
                    <th>支付宝手续费用</th>
                    <th>到账金额</th>
                    <th>订单状态</th>
                    <th>结账订单开始时间</th>
                    <th>结账订单结束时间</th>
                    <th>提现申请时间</th>
                    <th>财务操作完成时间</th>
                    <th>更新时间</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
        <p class="noOrder" style="display: none;">你暂时没有订单！</p>
    </div>
</body>
</html>
<script type="text/javascript" src="{{ static_url('js/cash.js') }}"></script>
