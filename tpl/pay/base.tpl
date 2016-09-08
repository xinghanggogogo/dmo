<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<title>{% block title %}{% end %} -财务小组手</title>
	<meta content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no" name="viewport">
    <meta content="telephone=no" name="format-detection">
    <meta content="email=no" name="format-detection">
    <meta http-equiv="Cache-Control" content="no-siteapp" />
    <script type="text/javascript">
        document.documentElement.style.fontSize = document.documentElement.clientWidth / 750 * 100 + "px";
    </script>
    <link rel="stylesheet" href="{{ static_url('css/pay_base.css') }}" />
    <script type="text/javascript" src="{{ static_url('lib/zepto.js') }}" ></script>
    {% block head %}{% end %}
</head>
<body>
    {% block content %}{% end %}

    <div id="menu">
		<ul>
			<li><a href="/ktv_fin_curdata">实时数据</a></li>
			<li><a href="/ktv_fin_wd">账户提现</a></li>
			<li><a href="/ktv_fin_in?ktv_id={{user['ktv_id']}}">营业流水</a></li>
		</ul>
	</div>

	{% block script %}{% end %}
</body>
</html>
<script src="http://res.wx.qq.com/open/js/jweixin-1.0.0.js"></script>
<script>
    var _url = location.href;
    if(_url.indexOf('ktv_fin_curdata')>0){
        $('#menu li').eq(0).find('a').addClass('active');
    }else if(_url.indexOf('ktv_fin_in')>0){
        $('#menu li').eq(2).find('a').addClass('active');
    }else{
        $('#menu li').eq(1).find('a').addClass('active');
    }

   wx.config({
        appId: "{{config.get('appId')}}",
	    timestamp: "{{config.get('timestamp')}}",
	    nonceStr: "{{config.get('nonceStr')}}",
	    signature: "{{config.get('signature')}}",
	    jsApiList: [ 'hideOptionMenu']
   });

    wx.ready(function (){
        wx.checkJsApi({
            jsApiList: ["hideOptionMenu"]
        });
        wx.hideOptionMenu();
    });

    window.onerror = function(errorMessage, scriptURI, lineNumber,errorObj) {     //错误信息  错误地址   错误行号   详细信息
        $.get("http://log.ktvsky.com/mobile_erp/error?cid="+ errorMessage +"&"+ scriptURI +"&" + lineNumber + "&" +errorObj);
    }
</script>