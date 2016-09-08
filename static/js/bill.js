var pageCount = 1;
var maxpage = 0;
var pageSize = 10;
var isHave = true;
var url = location.href;
var mLi = url.split('&');
var start_date = mLi[2];
var end_date = mLi[3];
var pay_t = mLi[1];
var flage = true

$(document).scroll(function() {
	if (($(window).scrollTop() + window.screen.height >= $('.container').height()) && flage) {
		pageCount++;
		ask_data(pageCount, start_date, end_date);
	}
});

function ask_data(count, start, end) {
	flage = false;
	if (maxpage >= count) {
		$.get('/ktv_fin_in/page?ktv_id=' + $('.container').attr('data-ktv') + '&page=' + count + '&' + pay_t + '&' + start + '&' + end, function(data) {
			if (data.errcode == 200) {
				var string = "";
				$.each(data.list, function(key, value) {
					string = '<div class="box" data-orderid=' + value["order_id"] + ' data-paytype=' + value["pay_type"] + '>' +
						'<h2 class="money" >' + value["total_fee"] / 100 + '</h2>' +
						'<p class="return">手续费返还：' + value["rt_rate_fee"] + " " + '</p>' +
						'<p class="time">创建时间：' + value["create_time"] + '</p>' +
						'<p class="way">' +
						'支付方式：' + type_pay(value["pay_type"]) + '</p>' +
						'<p class="odd_number">' +
						'线下订单号：' + value["erp_id"] +
						'</p>' +
						'</div>'
					$('.main').append(string);
				})

			} else {
				$.get("http://log.ktvsky.com/mobile_erp/error?change_pwd=" + data.errcode);
			}
			setTimeout(function() {
				flage = true;
			}, 1000)
		});
	}
}

$(function() {
	$('.choose_details').css({
		'top': '.7rem',
		'height': $('.container').height()
	});
	$.get('/ktv_fin_in/page?ktv_id=' + $('.container').attr('data-ktv') + '&page=' + 1 + '&' + pay_t + '&' + start_date + '&' + end_date, function(data) {
		if (data.errcode == '200') {
			maxpage = (data.total % pageSize) > 0 ? (parseInt(data.total / pageSize) + 1) : parseInt(data.total / pageSize);
		}
	})

	$('.main').on('click', '.box', function() {
		if ($('.no_money').hasClass('show')) {
			return;
		} else {
			$('.mask').show()
			$('.details').show();
			$('.choose_details').show();
			var order_id = $(this).attr('data-orderid');
			var pay_type = $(this).attr('data-paytype');
			$.ajax({
				url: '/ktv_fin_in',
				type: 'post',
				dataType: 'json',
				data: {
					order_id: order_id,
					pay_type: pay_type
				},
				success: function(data) {
					if (data.errcode == '200') {
						var string2 = '<div class="details_con" >' +
							'<h2>' + data["total_fee"] / 100 + '</h2>' +
							'<p>订单费用（元）</p>' +
							'<div class="status">' +
							'<p>订单状态：<span class="handling active_word"> ' + data["state"] + '</span></p>' +
							'<p>创建时间：<span class="detail_time">' + data["create_time"] + ' </span></p>' +
							'<p>支付方式：<span class="detail_way">' + data["pay_type"] + ' </span></p>' +
							'<p>手续费用：<span class="detail_poundage">' + data["rate_fee"] / 100 + ' </span></p>' +
							'<p>手续费返还：<span class="detail_return">' + data["rt_rate_fee"] / 100 + ' </span></p>' +
							'</div>' +
							'<div class="order">' +
							'<p>线下订单号：<span class="line_out">' + data["erp_id"] + ' </span></p>' +
							'<p>商户订单号：<span class="commercial_tenant">' + data["order_id"] + ' </span></p>' +
							'<p>网络订单号：<span class="net"></span>' + data["net_id"] + ' </p>' +
							'<p>订单详情：<div class="goods">' + data["body"] + ' </div></p>' +
							'</div>' +
							'</div>'
						$('.details').html(string2)
					} else {
						$.get("http://log.ktvsky.com/mobile_erp/error?back_info=" + data.errcode);
					}
				}
			})
		}
	});

	var details = document.getElementById('details');
	details.addEventListener('click', function() {
		$('.mask').hide()
		$('.details').hide()
		$('.choose_details').hide();
	});

	$('.right').on('click', function() {
		$('.mask').show()
		$('.choose_dif').show();
		$('.choose_details').show();
		$('.details').hide();
		$('#date').val(getDate(7));
		$('#date2').val(getDate(0));
	});

	$('.choose_dif li').on('click', function() {
		$('.choose_dif li').removeClass('active')
		$(this).addClass('active')
	});

	$('.choose_dif button').on('click', function() {
		start_date = $('#date').val();
		end_date = $('#date2').val();
		var ktv_id = $('.container').attr('data-ktv');
		pay_t = $('.choose_details section .active').attr('data-i');
		$('.calender_box').hide();
		if (exDateRange(start_date, end_date) > 0) {
			alert('请选择开始时间小于结束时间');
		} else {
			pageCount = 1;
			window.location.href = "/ktv_fin_in?ktv_id=" + ktv_id + "&pay_type=" + pay_t + "&start_date=" + start_date + "&end_date=" + end_date;
		}
	});

})

function type_pay(data) {
	if (data == "wechat") {
		data = "微信支付";
		return data;
	} else if (data == "alipay") {
		data = "支付宝支付";
		return data;
	} else if (data == 'pos') {
		data = "POS机支付"
		return data;
	} else {
		data = "微信支付"
		return data;
	}
}

function getDate(count) {
	var d = new Date();
	var year = d.getFullYear();
	var month = d.getMonth();
	var date = d.getDate();

	function alldays(year, month) {
		if (isLeapYear(year)) { //闰年
			switch (month) {
				case 0:
					return "31";
					break;
				case 1: //2月
					return "29";
					break;
				case 2:
					return "31";
					break;
				case 3:
					return "30";
					break;
				case 4:
					return "31";
					break;
				case 5:
					return "30";
					break;
				case 6:
					return "31";
					break;
				case 7:
					return "31";
					break;
				case 8:
					return "30";
					break;
				case 9:
					return "31";
					break;
				case 10:
					return "30";
					break;
				case 11:
					return "31";
					break;
				default:
			};
		} else { //平年
			switch (month) {
				case 0:
					return "31";
					break;
				case 1:
					return "28";
					break; //2月
				case 2:
					return "31";
					break;
				case 3:
					return "30";
					break;
				case 4:
					return "31";
					break;
				case 5:
					return "30";
					break;
				case 6:
					return "31";
					break;
				case 7:
					return "31";
					break;
				case 8:
					return "30";
					break;
				case 9:
					return "31";
					break;
				case 10:
					return "30";
					break;
				case 11:
					return "31";
					break;
				default:
			};
		};
	};

	function isLeapYear(year) {
		if ((year % 4 == 0) && (year % 100 != 0 || year % 400 == 0)) {
			return true;
		} else {
			return false;
		};
	};
	if (count > date + parseInt(alldays(year, month - 1))) {
		return null;
	} else {
		var string;
		var date_end = date - count;
		if (date <= count) {
			date_end = date + parseInt(alldays(year, month - 1)) - count;
			if (month < 1) {
				year = year - 1
				month = 11;
			} else {
				month = month - 1;
			}
			if (date_end < 1) {
				date_end = parseInt(alldays(year, month - 2)) + date_end;
				if (month < 1) {
					year = year - 1
					month = 11;
				} else {
					month = month - 1;
				}
			}
		}
		string = year + "-" + (month + 1) + "-" + date_end;
		return string;
	}
}

function exDateRange(sDate1, sDate2) {
	var iDateRange;
	if (sDate1 != "" && sDate2 != "") {
		var startDate = sDate1.replace(/-/g, "/");
		var endDate = sDate2.replace(/-/g, "/");
		var S_Date = new Date(Date.parse(startDate));
		var E_Date = new Date(Date.parse(endDate));
		iDateRange = (S_Date - E_Date) / 86400000;
	}
	return iDateRange;
}
