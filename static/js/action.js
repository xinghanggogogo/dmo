var EventUtil = {
	addHandler: function(element, type, handler) {
		if (element.addEventListener) {
			element.addEventListener(type, handler, false);
		} else if (element.attachEvent) {
			element.attachEvent('on' + type, handler);
		} else {
			element['on' + type] = handler;
		}
	},
	removerHandler: function(element, type, handler) {
		if (element.removeEventListener) {
			element.removeEventListener(type, handler, false);
		} else if (element.detachEvent) {
			element.detachEvent('on' + type, handler);
		} else {
			element['on' + type] = null;
		}
	}
}
$(function() {
	var clickable = true;
	var arr = ["", "", ""];
	var submit = document.getElementById('sub');
	var change = document.getElementById('change');
	var input1 = document.getElementById('password1');
	var input2 = document.getElementById('password2');
	var forget_password = document.getElementById('forget_password');
	var password_change_submit = document.getElementById('password_change_submit');
	var identify_code_resend = document.getElementById('identify_code_send');
	var source = $('#source').val()
	var userInfor = "";

	check_empty($('.login_password')[0]);
	if (getCookie('userAndPwd')) {
		arr = getCookie("userAndPwd").split("&&");
		$('.username').val(arr[0]);
		$('.login .login_password').val(arr[1].substring(parseInt(arr[2])))
	}
	EventUtil.addHandler(submit, 'click', login);
	EventUtil.addHandler(change, 'click', new_pwd)
	EventUtil.addHandler(password_change_submit, 'click', identify_code);
	EventUtil.addHandler(identify_code_resend, 'click', identify_code);
	EventUtil.addHandler(forget_password, 'click', function() {
		$('.item').hide();
		$('.find_password').show();
		$('.pointOutWord').text("");
		pushHistory();
	});
	document.onkeydown = function(event) {
		var e = event || window.event || arguments.callee.caller.arguments[0];
		if (e && e.keyCode == 13) { // enter 键
			if ($('.login').css('display') == 'block') {
				login();
			} else if ($('.new_password').css('display') == 'block') {
				new_pwd();
			} else if ($('.find_password').css('display') == 'block' && $('.identify_code_number').val()) {
				identify_code();
			}
		}
	}

	function login() {
		var telReg = (/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/).test($('.login .username').val());
		var log_Pwd = $('.login .login_password').val();
		if (telReg) {
			if (log_Pwd.length != 0 && log_Pwd.length != 0) {
				if ((log_Pwd).length == 6) {
					arr[1] = $('.login .login_password').val()
				} else {
					if (getCookie('userAndPwd')) {
						arr = getCookie("userAndPwd").split("&&");
						if ($('.login_password').val() != arr[1].substring(parseInt(arr[2]))) {
							arr[1] = hex_md5($('.login_password').val())
							arr[2] = $('.login_password').val().length;
						}
					} else {
						arr[1] = hex_md5($('.login_password').val())
						arr[2] = $('.login_password').val().length;
					}
				}
				$.ajax({
					type: "post",
					url: "/login",
					dataType: 'json',
					data: {
						"username": $('.login .username').val(),
						"password": arr[1]
					},
					success: function(msg) {
						if (msg['type'] == 0) {
							pointWord("账号或密码错误!")
						} else if (msg['type'] == 1) {
							$('.item').hide();
							pointWord("")
							$('.new_password').show();
							userInfor = $('.login .username').val();
						  $('input').val();
						} else if (msg['type'] == 2) {
							if ($('.remember_pwd')[0].checked) {
								setCookie('userAndPwd', $('.login .username').val() + "&&" + arr[1] + "&&" + arr[2], 'd7')
							} else {
								clearCookie('userAndPwd')
							}
							if (source == 'mobile') {
								window.location.href = "/ktv_fin_curdata"
							} else {
								window.location.href = '/bill/stat'
							}
						  $('input').val();
						} else {
							pointWord('帐号密码错误!')
							$.get("http://log.ktvsky.com/mobile_erp/error?login=" + msg['type']);
						}
					}
				});
			} else {
				pointWord("请输入账号和密码!")
			}
		} else {
			pointWord('请输入正确的手机号！')
		}
	}

	function new_pwd() {
		var password1 = $('.password1').val();
		var password2 = $('.password2').val();
		if (password1.length == 0 && password2 == 0) {
			return;
		}
		if (password1.length >= 8 && password1.length <= 12) {
			if (password1.length == password2.length) {
				$.ajax({
					url: 'login_set',
					type: 'post',
					data: {
						"password1": hex_md5(password1),
						"password2": hex_md5(password2)
					},
					success: function(msg) {
						if (msg['type'] == 0) {
							pointWord("两次密码不一致！")
						} else if (msg['type'] == 1) {
							if (userInfor && $('.remember_pwd')[0].checked) {
								setCookie('userAndPwd', userInfor + "&&" + hex_md5(password1) + "&&" + password1.length, 'd7')
							} else {
								clearCookie('userAndPwd')
							}
							if (source == 'mobile') {
								window.location.href = "/ktv_fin_curdata"
							} else {
								window.location.href = '/bill/stat'
							}
						  $('input').val();
						} else {
							pointWord('密码修改错误!')
							$.get("http://log.ktvsky.com/mobile_erp/error?change_pwd=" + meg['type']);
						}
					}
				})
			} else {
				pointWord('输入两次密码长度不一致!')
			}
		} else {
			pointWord('请输入8至12位密码!')
		}
		pushHistory();
	}

	function check_empty(obj) {
		obj.oninput = function() {
			obj.value = obj.value.replace(/\s+/g, "");
		}
	}
	check_empty(input1);
	check_empty(input2);

	function identify_code() {
		if (clickable == true||$('.identify_code_number').val().length==6) {
			var username_1 = $('.username_forget').val();
			var pwd = $('.find_password .identify_code_number').val();
			var telReg_1 = (/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/).test(username_1);
			if (telReg_1) {
				$.ajax({
					type: "post",
					url: "/login_for",
					data: {
						"username": username_1,
						"password_org": pwd
					},
					dataType: 'json',
					success: function(data) {
						if (data['type'] == 0) {
							pointWord('手机号没有注册!')
						} else if (data['type'] == 1) {
							$('.item').hide();
							$('.find_password').show()
							pointWord('验证码发送成功!')
							clickable = false;
							time_running();
						} else if (data['type'] == 2) {
							pointWord('发送验证码有误，请重新获取!')
						} else if (data['type'] == 3) {
							$('.item').hide();
							$('.new_password').show();
							userInfor = username_1;
							pointWord('');
						  $('input').val();
						} else if (data['type'] == 4) {
							pointWord('输入验证码错误!')
						} else {
							pointWord('验证码错误!')
							$.get("http://log.ktvsky.com/mobile_erp/error?identify_code=" + msg['type']);
						}
					}
				});
			} else {
				pointWord('请输入正确手机号!')
			}
		}
	}

	function time_running() {
		var timer = null;
		var number = 120;
		if (timer) {
			clearInterval(timer);
		}
		timer = setInterval(function() {
			number--;
			$('.time_running').html(number);
			$('.identify_code_resend').show();
			$('.identify_code_send').hide();
			if (number <= 0) {
				clickable = true;
				$('.identify_code_resend').hide();
				$('.identify_code_send').show();
				clearInterval(timer);
			}
		}, 1200)
	}

	if (!placeholderSupport()) { // 判断浏览器是否支持 placeholder
		$('[placeholder]').focus(function() {
			var input = $(this);
			if (input.val() == input.attr('placeholder')) {
				input.val('');
				if (input.attr("data-type") == "password") {
					input.attr("type", "password");
				}
				input.removeClass('placeholder');
			}
		}).blur(function() {
			var input = $(this);
			if (input.val() == '' || input.val() == input.attr('placeholder')) {
				input.addClass('placeholder');
				if (input.attr("data-type") == "password") {
					input.attr("type", "text");
				}
				input.val(input.attr('placeholder'));
			}
		}).blur();
	}
});

function placeholderSupport() {
	return 'placeholder' in document.createElement('input');
}

if ((navigator.userAgent.indexOf('MSIE') >= 0)) {
	function pushHistory() {}
} else {
	function pushHistory() {
		var state = {
			title: 'title',
			url: '#'
		};
		window.history.pushState(state, 'title', '#');
	}
}

function pointWord(text) {
	if ($('.pointOutWord').text() == "") {
		$('.pointOutWord').text(text)
		clearInterval(timer_1)
		var timer_1 = setTimeout(function() {
			$('.pointOutWord').text("")
		}, 5000)
	}
}

function clearCookie(c_name) {
	var exp = new Date();
	exp.setTime(exp.getTime() + (-1 * 24 * 60 * 60 * 1000));
	var cval = getCookie(c_name);
	document.cookie = c_name + "=" + cval + "; expires=" + exp.toGMTString();
}

function getCookie(c_name) {
	if (document.cookie.length > 0) {
		c_start = document.cookie.indexOf(c_name + "=")
		if (c_start != -1) {
			c_start = c_start + c_name.length + 1
			c_end = document.cookie.indexOf(";", c_start);
			if (c_end == -1) c_end = document.cookie.length
			return unescape(document.cookie.substring(c_start, c_end))
		}
	}
	return ""
}

function setCookie(c_name, value, time) {
	var strsec = getsec(time);
	var exdate = new Date()
	exdate.setTime(exdate.getTime() + strsec * 1)
	document.cookie = c_name + "=" + escape(value) + ((time == null) ? "" : "; expires=" + exdate.toGMTString())

}
/*过期时间*/
function getsec(str) {
	var str1 = str.substring(1, str.length) * 1;
	var str2 = str.substring(0, 1);
	if (str2 == 's') {
		return str1 * 1000;
	} else if (str2 == 'h') {
		return str1 * 60 * 60 * 1000;
	} else if (str2 == 'd') {
		return str1 * 24 * 60 * 60 * 1000;
	}
}
