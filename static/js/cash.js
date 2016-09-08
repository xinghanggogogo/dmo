var reg = new RegExp("^[0-9]*$"),
    ktv_id = $('#ktvId').val(),
    isBuy = true,
    withdraw_money = $('#withdraw_money').text(),
    mealNum = 0,
    pageCount = 0,
    pageSize = 10,
    page = 1;


$(function(){

	$('.meals li').eq(0).trigger('touchstart');
	$.get('/ktv_fin_wd/page?ktv_id='+ ktv_id ,function(data){
	    if(data.errcode == '200'){
	        pageCount = (data.total%pageSize)>0?(parseInt(data.total/pageSize)+1):parseInt(data.total/pageSize);
	    }
	});

	$('.seeNote').unbind('click').on('click',function(){
        addNoteInfo(1);
		$('header,#cash').hide();
		$('.cashNotes').show();
		pushHistory();
	});
});

    /*buy meals*/
	$('.meals li').on('touchstart',function(){
		if($(this).hasClass('click')){
			$(this).removeClass('click');
			isBuy = false;
			mealNum = 0;
		}else{
			$('.meals li').removeClass('click');
			$(this).addClass('click');
			isBuy = true;
			mealNum = $(this).find('.time_num').text();
		}
		if(!isBuy){
			$('.xgtc').hide();
			$('.confirm .mealMoney').text('');
			$('.confirm .mealDesc').text('');
			$('#cashMoney').text(withdraw_money);
			$('#cashBtn').addClass('isbtn');
		}else{
			$('.xgtc').show();
			$('.cashInfo .xgtc .tc').text('￥-'+$(this).find('.money span').text()+' '+$(this).find('.time_num').text()+'个月套餐');
			$('.confirm .mealMoney').text($(this).find('.money span').text());
			$('.confirm .mealDesc').text($(this).find('.time_num').text()+'个月套餐');
			//更改显示价格
			var ser_fee = $(this).find('.money span').text();
			$('#cashMoney').text((withdraw_money- ser_fee).toFixed(2));
		}
		if($('#cashMoney').text()>0){
            $('#cashBtn').hasClass('isbtn') ? '': $('#cashBtn').addClass('isbtn');
        }else{
            $('#cashBtn').removeClass('isbtn');
        }
	});

	/*submit bankInfo*/
	$('#bankBtn').on('click',function(e){
		var jsSize = $('.bankInfo>p').size();
		flag = true;
		bankJson = {};
		for(var k=0;k<jsSize;k++){
			if($('.bankInfo>p').eq(k).find('input').val() == ''){
				flag = false;
			}
			bankJson[$('.bankInfo>p').eq(k).find('input').attr('name')] = $('.bankInfo>p').eq(k).find('input').val();
		}
		if(!reg.test($('.phoneNum').val())){
			modul('输入银行卡号有误,请重新输入！');
			e.preventDefault();
			return
		}

		if(!phone($('.phone').val())){
			modul('手机号格式不对,请重新输入！');
			e.preventDefault();
			return
		}

		if (flag == false) {
            modul('银行信息不能为空！');
            e.preventDefault();
            return
        }
		$('.confirm,.masking').show();
		$('.isTrue span').on('click',function(){
			if($(this).attr('name') == 'true'){
                $.ajax({
                    type:"post",
                    url:"/bank",
                    async:true,
                    data:bankJson,
                    dataType :'json',
                    success: function(data){
                        if(data.errcode == '200'){
                            modul('银行信息提交成功,正在为你跳转！');
							setTimeout(function () {
								location.href = '/ktv_fin_wd';
							},2000);
                        }else{
                            modul('银行信息提交失败');
                            $.get("http://log.ktvsky.com/mobile_erp/error?back_info="+ data.errcode); //错误信息汇总
                        }
                    }
                });
			}
			$('.confirm,.masking').hide();
		});
	});

/*绑定事件*/
function bindClick(){

	/*see detail*/
	$('.cashState li').unbind('click').on('click',function(){
		$('.masking,.detail').show();
		$('.detail .dealMoney').text($(this).find('.dealMoney').text());
		$('.detail .state').text($(this).find('.state').text());
		$('.detail .wireDate').text($(this).find('.wireDate').text());
		$('.detail .applyDate').text($(this).find('.applyDate').text());
		$('.detail .wxM').text($(this).find('.data').attr('data-wx'));
		$('.detail .wxCost').text($(this).find('.data').attr('data-wxcost'));
		$('.detail .aliM').text($(this).find('.data').attr('data-ali'));
		$('.detail .aliCost').text($(this).find('.data').attr('data-alicost'));
		$('.detail .posM').text($(this).find('.data').attr('data-pos'));
		$('.detail .posCost').text($(this).find('.data').attr('data-poscost'));
		$(this).find('.rout').length>0?$('.detail .rout').show().text($(this).find('.rout').text()):$('.detail .rout').hide();
	});
}

/*cash*/
$('#cashBtn').on('click',function(){
	if($(this).hasClass('isbtn')){
		$('.masking').show();
		$('.confirm').show().find('.esta').text('确认提现吗？');
		$('.isTrue span').unbind('click').on('click',function(){
			if($(this).attr('name') == 'true'){
				$.ajax({
                    type:"post",
                    url:'/ktv_withdraw',
                    async:true,
                    data:{'ser_fee':$('.mealMoney').text(),'ser_period':mealNum},
                    dataType :'json',
                    success: function(data){
                        if(data.errcode == '200'){
                            modul('提现成功');
                            $('#cashBtn').removeClass('isbtn');
                        }else if(data.errcode == '1001'){
                            modul('上个订单还没处理完成，请先等待');
                        }else if(data.errcode == '500'){
                            modul('订单异常，请稍后处理');
                        }else{
							modul(data.errmsg);
                            $.get("http://log.ktvsky.com/mobile_erp/error?cash="+ data.errcode +':'+data.errmsg);
                        }
                    }
                });
			}
			$('.confirm,.masking').hide();
		});
	}
})

$('.masking').on('click',function(){
	if($('.detail').css('display') == 'block'){
		$('.masking,.detail').hide();
	}
});

/*提交框*/
function modul(obj){
	$('.modul').show().find('p').text(obj);
	$('.modul').css('margin-left',($('body').width()-$('.modul').width())/2);
	setTimeout("$('.modul').hide()",5000);
}

/*安卓物理返回*/
window.addEventListener('popstate', function(evt) {
    if($('.cashNotes').css('display') == 'block'){
    	$('.cashNotes,.masking').hide();
		$('header,#cash').show();
		$('.cashState li').remove();
    }
});


function pushHistory(){
    var state = {
        title: 'title',
        url: '#'
    };
    window.history.pushState(state, 'title', '#');
}


$(document).scroll(function(){
    if(($(window).scrollTop()+ window.screen.height) >= $('.cashState').height() && $('.cashNotes').css('display') == 'block'){
        addNoteInfo(page);
    }
})


function addNoteInfo(count){
    if(pageCount>=count){
        $.get('/ktv_fin_wd/page?ktv_id='+ ktv_id +'&page='+ count ,function(data){
            if(data.errcode == '200'){
                 $('.noNote').hide();
                 $.each(data.list,function(key,value){
                      var str = '<li>'+
                                '<div>'+
                                    '<font class="dealMoney">'+ value['account_money']/100 +'</font>'+
                                    '<p class="wireDate">划账日期：'+ value['start_date'].split(' ')[0] +' 至 '+ value['end_date'].split(' ')[0] +'</p>'+
                                    '<p class="applyDate">申请时间：'+ value['create_time'] +'</p>'+
                                    '<p class="state dealTrue">'+ value['state'] +'</span>'+
                                    '<p class="rout">手续费返还：'+ value['return_service_charge'] +'</p>'+
                                    '<p class="data" data-wx="'+ value['withdraw_money']/100 +'" data-ali="'+ value['ali_withdraw_money']/100 +'" data-pos="'+ value['pos_withdraw_money']/100 +'" data-wxCost="'+ value['service_charge']/100 +'" data-aliCost="'+ value['ali_service_charge']/100 +'" data-posCost="'+ value['pos_service_charge']/100 +'"></p>'+
                                '</div>'+
                            '</li>';

                    $('.cashState').append(str);
                    });
                 bindClick();
                 page++;
            }else{
                 $('.noNote').show();
                 $.get("http://log.ktvsky.com/mobile_erp/error?noteInfo="+ data.errcode +':'+data.errmsg);
            }
        });
    }else{
        $('.noNote').show();
    }
}

function phone(obj){
    var telReg = (/^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/).test(obj);
    return telReg;
}
