<!DOCTYPE html>
<html>

    <head>
        <title>雷石ktv财务账号登陆</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        <meta charset="utf-8">
        <meta content="no-cache,must-revalidate" http-equiv="Cache-Control">
        <meta content="no-cache" http-equiv="pragma">
        <meta content="0" http-equiv="expires">
        <meta content="telephone=no, address=no" name="format-detection">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <script type="text/javascript">
            document.documentElement.style.fontSize = document.documentElement.clientWidth / 750 * 100 + "px";
        </script>
        <link rel="stylesheet" href="{{ static_url('css/pay_reset.min.css') }}" media="screen" title="no title" charset="utf-8">
        <!-- 移动段css -->
        <link rel="stylesheet" id="pcOrPh" href="{{ static_url('css/pay_index_style.css') }}" media="screen" title="no title" charset="utf-8">
        <!-- px端css -->
        <!-- <link rel="stylesheet" href="{{static_url('css/erp.css')}}" media="screen" title="no title"> -->
    </head>
    <style type="text/css">
        * {
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
            -webkit-tap-highlight-color: transparent;
        }
    </style>
    </head>

    <body style="display:none">
        <div class="container">
            <h2>财务管理系统登录</h2>
            <h3>雷石KTV</h3>
            <p class="pointOutWord"></p>
            <div class="item login active ">
                <ul>
                    <li>
                        <label for="">帐&nbsp&nbsp号</label><input type="tel" name="name" value="" class="username" placeholder='请输入手机号' maxlength="11">
                    </li>
                    <li>
                        <label for="">密&nbsp&nbsp码</label><input type="password" name="name" value="" class=" login_password" placeholder="请输入密码">
                    </li>
                    <li id="sub" class="button"><button type="submit" name="button" class="submit">登录</button></li>
                </ul>
                <div class="forget_password clear"><span><input type="checkbox" checked="checked" name="rem" class="remember_pwd"/><label for="rem">&nbsp记住密码</label></span> <span id="forget_password">忘记密码</span></div>
            </div>
            <div class="find_password item">
                <ul>
                    <li>
                        <label for="">帐&nbsp&nbsp号</label><input type="tel" name="name" value="" class="username_forget" placeholder="请输入帐号" maxlength="11" />
                    </li>
                    <li><label for="">验证码</label><input type="text" name="name" value="" class="identify_code_number" placeholder="请输入验证码" maxlength="6">
                        <div class="identify_code_box">
                            <div class="identify_code_send" id="identify_code_send">发送验证码</div>
                            <div class="identify_code_resend"> 重新发送 <span class="time_running">120</span>s</div>
                        </div>
                    </li>
                    <li style="text-align: center;">
                        <button  type="submit" name="button" class="submit" id="password_change_submit">登录</button>
                    </li>
                </ul>
            </div>
            <div class="item new_password">
                <ul>
                    <li>
                        <input type="password" name="name" value="" class="password1" id="password1" placeholder="请输入密码">
                    </li>
                    <li>
                        <input type="password" name="name" value="" class="password2" id="password2" placeholder="请再次输入密码">
                    </li>
                    <li>
                        <div class="prompt">请您输入8~12位新密码</div>
                    </li>
                    <li class="change" id="change" style="text-align: center;"><button type="submit" name="button" class="submit">提交</button></li>
                </ul>
            </div>
        </div>
        <input type='hidden' value={{ source}} id=source />
        <div class="footer" >如有问题请联系：010-51660862</div>
    </body>
    <script id="loadjs" charset="UTF-8"></script>
    <script id="md5" src="/static/js/md5.js" type="text/javascript" charset="utf-8"></script>
    <script id="index" type="text/javascript" charset="utf-8"></script>
    <script type="text/javascript">
        if (getExplorer()) {
            loadjs.src = "/static/lib/zepto.js";
            pcOrPh.href = "{{ static_url('css/pay_index_style.css') }}";
            window.addEventListener('popstate', function(evt) {
                if ($('.forget_password').css("display") == 'block') {
                    $('.item').hide();
                    $('.login').show();
                    $('.pointOutWord').text("");
                } else if ($('.new_password').css("display") == 'block') {
                    $('.item').hide();
                    $('.login').show();
                }
            })
        } else {
            loadjs.src = "/static/lib/jquery-1.7.1.min.js";
            pcOrPh.href = "{{ static_url('css/erp.css') }}";
        }

        function getExplorer() {
            var sUserAgent = navigator.userAgent.toLowerCase();
            var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
            var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
            var bIsMidp = sUserAgent.match(/midp/i) == "midp";
            var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
            var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
            var bIsAndroid = sUserAgent.match(/android/i) == "android";
            var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
            var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
            if (!(bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM)) {
                return false
            } else {
                return true;
            }
        }
    </script>
    <script type="text/javascript">
        setTimeout(function() {
            index.src = "/static/js/action.js";
            $('body').show();
        }, 300);
    </script>

</html>
