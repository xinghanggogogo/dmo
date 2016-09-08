<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>学员奖励</title>
    <meta content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no" name="viewport">
    <meta content="telephone=no" name="format-detection">
    <meta content="email=no" name="format-detection">
    <meta http-equiv="Cache-Control" content="no-siteapp" />
    <link rel="stylesheet" href="{{ static_url('css/index.css') }}" />
    <script type="text/javascript" src="{{ static_url('lib/jquery-1.7.1.min.js') }}"></script>
</head>
<body>
    {% if not cashier %}
        <div class="pleaseOpen">
            <img src="{{static_url('images/points.png')}}"/>
            <p>请登录收银系统，使用微信扫码二维码，参与活动</p>
        </div>
    {% else %}
        <div class="warpAll">
            <input value="{{ cashier.get('openid') }}" type="hidden" id="openId"/>
            <div class="reward">   <!--领取奖励-->
                <span class="user">
                    <img alt="" src="{{ cashier.get('headimgurl') }}"/>
                </span>
                <div class="grades">
                    <div>{{ cashier.get('nickname', '') }}</div>
                    <p>{{ cashier.get('ktv', 'ktv不详') }}</p>
                </div>
                <div class="rewardInfo">
                    <span class="totalRe">总奖励金额</span>
                    <div class="userRE">
                        <p class="moneyInfo"><span class="money">{{ cashier.get('total_cash') - withdrawed }}</span>元</p>
                        <div class="pageCen">
                            {% if cashier.get('total_cash') - withdrawed >= 10 %}
                                <a href="#" onclick="" id="dole" class="dole">立即领取</a>
                            {% else %}
                                 <a href="#" onclick="" id="doleNo" class="dole">立即领取</a>
                            {% end %}
                        </div>
                        <span class="tj">满10元可领取</span>
                    </div>
                </div>
            </div>
            <!--<div class="yestTask">
                <span class="taskTitle">昨日完成任务:</span>
                <ul class="info">
                    <li>累积奖励<span>×1</span>次</li>
                    <li>单笔1000元以上<span>×2</span>次</li>
                </ul>
            </div>-->
            <div class="present">    <!--当前任务-->
                <span class="taskTitle">当前任务进度:</span>
                {% for key in cashier.get('tasks', []) %}
                    <div class="info">
                        <div class="preTj"><span>{{ key.get('title') }}</span><span class="finMore">已完成×{{ key.get('level') }}次</span></div>
                        <div class="setbacks">
                        {% if key.get('cur')/key.get('dst') == 0 %}
                            <span class="vader" style="width:{{ key.get('cur') * 100 // key.get('dst') }}%;"></span>
                            <em style="margin-left:{{ key.get('cur') * 100 // key.get('dst') }}%; background: none">{{ key.get('cur') * 100 // key.get('dst') }}%</em>
                        {% else %}
                            <span class="vader" style="width:{{ key.get('cur') * 100 // key.get('dst') }}%;min-width:2%;"></span>
                            <em style="margin-left:{{ 2 if key.get('cur') * 100 // key.get('dst') < 2 else key.get('cur') * 100 // key.get('dst') }}%;">{{ key.get('cur') * 100 // key.get('dst') }}%</em>
                        {% end %}
                        </div>
                        <div class="preTj"><span>0</span><span class="maxtj">{{ key.get('dst') }}</span></div>
                        {% if key.get('type') == 'ac_task' %}
                            <p class="infoTj">当日消费每累计增加{{ key.get('dst') }}元—奖励{{ key.get('reward') }}元</p>
                        {% else %}
                            <p class="infoTj">单笔消费满{{ key.get('dst') }}元—奖励{{ key.get('reward') }}元</p>
                        {% end %}
                    </div>
                 {% end %}
            </div>
        </div>
    {% end %}
</body>
</html>
<script src="https://res.wx.qq.com/open/js/jweixin-1.0.0.js"></script>
<script>
    wx.config({
        appId: '{{config['appId']}}',
        timestamp: {{config['timestamp']}},
        nonceStr: '{{config['nonceStr']}}',
        signature: '{{config['signature']}}',
        jsApiList: ['hideOptionMenu','closeWindow']
    });

var isSub = true;
$(function(){
    $("#dole").on("touchstart",function(event){
        event.preventDefault();
        if(isSub = true){
            isSub = false;
            $(this).css({'background':"{{ static_url('images/doleClick.png') }}",'background-size':'100% 100%'});
            $.ajax({
                async:true,
                cache : false,
                type:"post",
                url:'/cashier/withdraw',
                data:{openid:$("#openId").val()},
                dataType:'json',
                success:function(data){
                    if(data['result'] == 1){
                        wx.closeWindow();
                    }else{
                        alert(data.errmsg);
                    }
                }
            });
            isSub = true;
        }
    });
});

wx.ready(function (){
    wx.checkJsApi({
        jsApiList: ["hideOptionMenu", "closeWindow"]
    });
    wx.hideOptionMenu();
});
</script>
