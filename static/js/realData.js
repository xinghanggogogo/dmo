var ktv_id = $('#ktvId').val(),
    colorType = ['#99dd40','#58c0f5','#8374e8','#f36a6a','#f39534', '#f45534'];

$.get('/ktvfinrevenue/hour?ktv_id='+ktv_id,function(data){
    if(data.errcode == '200'){
        addChartInfo($('#dayAocc'),data.times,data.values,'时间(H)');
        $('.totalMoney').eq(0).text('共计：'+ data.total +'元');
    }
});

$.get('/ktvfinrevenue/month?ktv_id='+ktv_id,function(data){
    if(data.errcode == '200'){
        addChartInfo($('#monthAocc'),data.times,data.values,'时间(日)');
        $('.totalMoney').eq(1).text('共计：'+ data.total +'元');
        $('.date').eq(0).text('('+ data.times[0] +'至'+ data.times[data.times.length-1] +')');
    }
});

$.get('/ktvfinrevenue/year?ktv_id='+ktv_id,function(data){
    if(data.errcode == '200'){
        addChartInfo($('#yearAocc'),data.times,data.values,'时间(月)');
        $('.totalMoney').eq(2).text('共计：'+ data.total +'元');
        $('.date').eq(1).text('('+ data.times[0] +'至'+ data.times[data.times.length-1] +')');
    }
});

$.get('/ktvfinprop/revenue?ktv_id='+ktv_id,function(data){
    if(data.errcode == '200'){
        addPieInfo($('#pieChart'),data.data);
    }
});

$.get('/ktvfinprop/pay?ktv_id='+ktv_id,function(data){
    if(data.errcode == '200'){
        $.each(data.data,function(key,value){
            $('.ringList').append(
                '<div class="stat"  data-text="'+ value['Name'] +' '+ value['ValueRate'] +'%" data-info="'+ value['Value'] +'元" data-percent="'+ value['ValueRate'] +'" data-fgcolor="'+ colorType[key] +'" data-bgcolor="#f0eae6"></div>'
            );
        });
        $('.stat').circliful();
        $('.circliful').css('margin-left',($('body').width()-3*$('.circliful').width())/4);
    }
});

/*曲线图*/
var addChartInfo = function(id,xA,yA,Xnit){
	var xA=xA;     //指定X轴刻度值
	var yA=yA;                //指定数据
	var xData=0,yData=0;
    id.highcharts({
        chart: {
            type: 'areaspline',
        },
        title: {
            text: '曲线图',          
            style:{
            	 opacity:'0',
            }
        },
        legend:{
        	enabled:false,
        },
        xAxis: { 
            labels: {  
            	formatter:function(){
            		return xA[this.value]
            	},
           	},
           	title: {
                align: 'high',
                offset: 50,
                text: Xnit,
                rotation: 0,
                x: -10
            },          	
            tickInterval:1,          
            tickmarkPlacement:'on',
            tickWidth:0,
        },
        yAxis: {
        	title: {
                align: 'high',
                offset: 0,
                text: '金额(元)',
                rotation: 0,
                y: -20,
           },
           labels:{
          		format: '{value} 元'
           },
           gridLineColor: '#f3f4f5',
           lineColor: '#edeff0',
           lineWidth: 1,
        },
        plotOptions: {
            areaspline: {
            	lineWidth: 0,  
                fillOpacity: 0.5,
            },
            series: {
                marker: {
                    enabled: false
                },  
            },
            allowPointSelect: true,
            area: {
                marker: {
                    enabled: false,
                    radius: 12,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            },
        },
        series: [{
        	allowPointSelect: true,
            data: yA,
            color:'#f88147',
            dataLabels: {
            	enabled: false,
            },
            marker: {
            	radius:0,
            }
        }],
        tooltip: {
        	shared: true,
        	backgroundColor: '#4c5e70',
        	borderColor:'none',
        	crosshairs: [{
        		width:1,
        		color:'#4c5e70',
        		dashStyle:'Dash',
        	}],       	
        	style: {
                padding: 10,
                fontWeight: 'bold',               
                color: '#fff',               
          	},
            formatter:function(){     
            	return '<small>'+ xA[this.x] +'</small><br/><small>'+ this.y +'元</small>'
            }
        },
        credits:{
     		enabled:false // 禁用版权信息
		},
		colors:'#f88147',
    });
}

    /*饼状图*/
    var addPieInfo = function (id,data) {
        id.highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: null,
            },
            tooltip: {
                pointFormat: '',
            },
            plotOptions: {
                pie: {
                    allowPointSelect: false,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        },
                        connectorColor: 'silver'
                    }
                }
            },
            series: [{
                type: 'pie',
                data: data
            }],
            colors:['#f88147', '#ffbd95', '#ffd0b3', '#ffdfcc', '#ffa169'],
            credits:{
                enabled:false // 禁用版权信息
            },
        });
    }

