{% extends 'base.tpl' %}

{% block title %}营收统计{% end %}

{% block head %}
<script type="text/javascript" src="{{ static_url('lib/echarts.common.min.js') }}"></script>
<script type="text/javascript" src="{{ static_url('lib/underscore-min.js') }}"></script>
{% end %}

{% block container %}
<div id="container" class="stat">
    <div class="yesterday-today">
        <h2>昨日今日营收对比（元）</h2>
        {% if revenue and revenue.get('data', []) and len(revenue['data']) == 2 %}
        <ul>
            <li>
                <em>{{ revenue['data'][1]['Stm'] }} ~ 现在</em>
                <span class="w250">今日营收总金额：{{ revenue['data'][1]['TotalAmount'] }}</span>
                <span class="w150">总包房数：{{ revenue['data'][1]['RoomCount'] }}</span>
                <span class="w150">开房数：{{ revenue['data'][1]['OpenCount'] }}</span>
                <span class="w150">预订数：{{ revenue['data'][1]['BookCount'] }}</span>
            </li>
            <li>
            <em>{{ revenue['data'][0]['Stm'] }} ~ {{ revenue['data'][0]['Etm'] }}</em>
            <span class="w250">昨日营收总金额：{{ revenue['data'][0]['TotalAmount'] }}</span>
            <span class="w150">总包房数：{{ revenue['data'][0]['RoomCount'] }}</span>
            <span class="w150">开房数：{{ revenue['data'][0]['OpenCount'] }}</span>
            <span class="w150">预订数：{{ revenue['data'][0]['BookCount'] }}</span>
            </li>
        </ul>
        {% else %}
        <p class="no-data">暂未获取到数据，请检查中转服务器相关服务或点击右上角页面刷新</p>
        {% end %}
        <div id="echart-today-revenue" class="map"></div>
        <div id="echart-month-revenue" class="map"></div>
        <div id="echart-year-revenue" class="map"></div>
    </div>
    <div class="today-revenue">
        <h2>今日营收分布占比</h2>
        <div id="echart-today-revenue-prop" class="map"></div>
    </div>
    <div class="today-payment">
        <h2>今日支付方式占比</h2>
        <div id="echart-today-pay-prop" class="map"></div>
    </div>

</div>
{% if base64_img %}
<div class="mobile-banner">
    <img src="data:image/png;base64,{{ base64_img }}" />
    <img src="{{ static_url('images/mobile.png') }}" />
    <i class="close"></i>
</div>
<script>
$('.mobile-banner').on('click', 'i', function(evt) {
    $('.mobile-banner').hide()
})
</script>
{% end %}
{% end %}

{% block foot %}
<script>
(function() {
    String.prototype.trim = function() {
        return this.replace(/(^\s*)|(\s*$)/g, "");
　　}
    function revenue(text, subtext, x_name, times, y_name, values) {
        var option = {
            title: {
                text: text,
                left: 'center',
                subtext: subtext,
                subtextStyle: {
                    color: '#000'
                }
            },
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                name: x_name,
                data: times,
                type: 'category',
                boundaryGap: false
            },
            yAxis: {
                name: y_name
            },
            series: [{
                name: y_name,
                type: 'line',
                smooth: true,
                itemStyle: {
                    normal: {
                        color: 'rgb(255, 70, 131)'
                    }
                },
                areaStyle: {
                    normal: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgb(255, 158, 68)'
                        }, {
                            offset: 1,
                            color: 'rgb(255, 70, 131)'
                        }])
                    }
                },
                data: values
            }]
        }
        return option
    }

    var today_revenue_dom = document.getElementById('echart-today-revenue'),
        today_revenue = echarts.init(today_revenue_dom);
    $.get('/revenue/hour').done(function(response) {
        var times = response['times'],
            values = response['values'],
            total_money = 0;

        if (times.length == 0) {
            $(today_revenue_dom).html('暂未获取到数据，请检查中转服务器相关服务或点击右上角页面刷新')
            return
        }

        times = _.map(times, function(time) {
            var hour = time.split(' ')[1]
            return hour
        })

        _.each(values, function(value) {
            total_money += parseFloat(value);
        })

        today_revenue.setOption(revenue('今日流水', '共计：' + total_money + '元', '时间（时）', times, '金额（元）', values))
    })

    var month_revenue_dom = document.getElementById('echart-month-revenue'),
        month_revenue = echarts.init(month_revenue_dom);
    $.get('/revenue/month').done(function(response) {
        var times = response['times'],
            values = response['values'],
            total_money = 0;

        if (times.length == 0) {
            $(month_revenue_dom).html('暂未获取到数据，请检查中转服务器相关服务或点击右上角页面刷新')
            return
        }
        times = _.map(times, function(time) {
            var day_info = time.split('-')
            return day_info[1] + '.' + day_info[2]
        })

        _.each(values, function(value) {
            total_money += parseFloat(value);
        })

        month_revenue.setOption(revenue('月流水', '共计：' + total_money + '元', '时间（日）', times, '金额（元）', values))
    })

    var year_revenue_dom = document.getElementById('echart-year-revenue'),
        year_revenue = echarts.init(year_revenue_dom);
    $.get('/revenue/year').done(function(response) {
        var times = response['times'],
            values = response['values'],
            total_money = 0;

        if (times.length == 0) {
            $(year_revenue_dom).html('暂未获取到数据，请检查中转服务器相关服务或点击右上角页面刷新')
            return
        }

        times = _.map(times, function(time) {
            var day_info = time.split('-')
            return day_info[1] + '月'
        })

        _.each(values, function(value) {
            total_money += parseFloat(value);
        })

        year_revenue.setOption(revenue('年流水', '共计：' + total_money + '元', '时间（月）', times, '金额（元）', values))
    })

    var today_revenue_prop_dom = document.getElementById('echart-today-revenue-prop'),
        today_revenue_prop = echarts.init(today_revenue_prop_dom);
    $.get('/prop/revenue').done(function(response) {
        var items = response['data'];

        if (items.length == 0) {
            $(today_revenue_prop_dom).html('暂未获取到数据，请检查中转服务器相关服务或点击右上角页面刷新')
            return
        }

        items = _.map(items, function(item) {
            return {
                value: item['Value'],
                name: item['Name'].trim() + item['ValueRate'] + ' ' + item['Value'] + '元'
            }
        })

        today_revenue_prop.setOption({
            series : [
                {
                    name: '营收分布',
                    type: 'pie',
                    data: items,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        })
    })

    var today_pay_prop_dom = document.getElementById('echart-today-pay-prop'),
        today_pay_prop = echarts.init(today_pay_prop_dom);
    $.get('/prop/pay').done(function(response) {
        var items = response['data'];

        if (items.length == 0) {
            $(today_pay_prop_dom).html('暂未获取到数据，请检查中转服务器相关服务或点击右上角页面刷新')
            return
        }

        items = _.map(items, function(item, index) {
            return {
                value: item['Value'],
                name: item['Name'].trim() + item['ValueRate'] + ' ' + item['Value'] + '元'
            }
        })

        today_pay_prop.setOption({
            series : [{
                name: '支付方式',
                type: 'pie',
                radius: ['70%', '90%'],
                avoidLabelOverlap: false,
                data: items,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '25',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        })
    })
})()
</script>
{% end %}
