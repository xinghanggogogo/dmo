function clander(obj) {
	//创建日历控件基本结构
	var val;
	var obody = document.body;
	createbox();

	function createbox() {
		var ddbox = document.createElement("div");
		ddbox.id = "box" + obj.id;
		ddbox.className = 'calender_box';
		var str = "";
		str += '<div id="title' + obj.id + '" class="title"><div id="prevyear' + obj.id + '" class="prevyear"><<</div><div id="prevmonth' + obj.id + '" class="prevmonth"><</div><div id="month' + obj.id + '" class="month"></div><div id="year' + obj.id + '" class="year"></div><div id="nextmonth' + obj.id + '" class="nextmonth">></div><div id="nextyear' + obj.id + '" class="nextyear">>></div></div>';
		str += '<div id="week' + obj.id + '" class="week"><div>日</div><div>一</div><div>二</div><div>三</div><div>四</div><div>五</div><div>六</div></div>';
		str += '<div id="con' + obj.id + '" class="clearfix con"></div>';
		str += '<div id="btns' + obj.id + '" class="btns"><div id="nowtime' + obj.id + '" class="nowtime">当前时间</div><div id="cleartime' + obj.id + '" class="cleartime">清空</div></div>';
		ddbox.innerHTML = str;
		obody.appendChild(ddbox);
	};
	//===================get ele===============================
	var omonth = document.getElementById("month" + obj.id);
	var oyear = document.getElementById("year" + obj.id);
	var con = document.getElementById("con" + obj.id);
	var prevmonth = document.getElementById("prevmonth" + obj.id);
	var nextmonth = document.getElementById("nextmonth" + obj.id);
	var prevyear = document.getElementById("prevyear" + obj.id);
	var nextyear = document.getElementById("nextyear" + obj.id);
	var nowtime = document.getElementById("nowtime") + obj.id;
	var box = document.getElementById("box" + obj.id);
	var cleartime = document.getElementById("cleartime" + obj.id);
	box.style.display = "block";
	//===================show date===============================
	obj.onfocus = function() { //显示控件
		box.style.display = 'block';
	};
	con.onclick = function(event) {
		if (event.target.tagName == "DIV" && event.target.nodeType == "1" && hasclass(event.target.className, "edate")) {
			obj.value = "";
			val = dateObj.getFullYear() + "-" + toyear(dateObj) + "-" + event.target.innerHTML;
			obj.value = val;
			box.style.display = "none";
		};
	};
	//===================set year month===============================
	//默认时间对象
	var dateObj = new Date();
	//动态控制
	prevmonth.onclick = function() { //上一月
		var ddm = null;
		var ddy = null;
		if ((dateObj.getMonth() - 1) == -1) {
			ddm = 11;
			ddy = dateObj.getFullYear() - 1;
		} else {
			ddm = dateObj.getMonth() - 1;
			ddy = dateObj.getFullYear();
		};
		dateObj.setFullYear(ddy);
		dateObj.setMonth(ddm);
		omonth.innerHTML = toyear(dateObj) + "月";
		oyear.innerHTML = dateObj.getFullYear() + "年";
		remove();
		oneweek = oneyearoneday(dateObj);
		alld = alldays(dateObj);
		nowd = nowday(dateObj);
		init(oneweek, alld, nowd);
	};
	nextmonth.onclick = function() { //下一月
		var ddm = null;
		var ddy = null;
		if ((dateObj.getMonth() + 1) == 12) {
			ddm = 0;
			ddy = dateObj.getFullYear() + 1;
		} else {
			ddm = dateObj.getMonth() + 1;
			ddy = dateObj.getFullYear();
		};
		dateObj.setFullYear(ddy);
		dateObj.setMonth(ddm);
		omonth.innerHTML = toyear(dateObj) + "月";
		oyear.innerHTML = dateObj.getFullYear() + "年";
		remove();
		oneweek = oneyearoneday(dateObj);
		alld = alldays(dateObj);
		nowd = nowday(dateObj);
		init(oneweek, alld, nowd);
	};
	//返回到今时今日
	//年月获取
	var year = dateObj.getFullYear();
	var month = toyear(dateObj); //0是12月
	//月年的显示
	omonth.innerHTML = month + "月";
	oyear.innerHTML = year + "年";
	//===================set day===============================
	//获取本月1号的周值
	var oneweek = oneyearoneday(dateObj);
	//本月总日数
	var alld = alldays(dateObj);
	//当前是几
	var nowd = nowday(dateObj);
	//初始化显示本月信息
	init(oneweek, alld, nowd);
	//===================function===============================
	//有无指定类名的判断
	function hasclass(str, cla) {
		var i = str.search(cla);
		if (i == -1) {
			return false;
		} else {
			return true;
		};
	};
	//初始化日期显示方法
	function remove() {
		con.innerHTML = "";
	};

	function init(oneweek, alld, nowd) {
		for (var i = 1; i <= oneweek; i++) { //留空
			var eday = document.createElement("div");
			eday.innerHTML = "";
			con.appendChild(eday);
		};
		for (var i = 1; i <= alld; i++) { //正常区域
			var eday = document.createElement("div");
			if (i == nowd) {
				if (i <= 31) {
					eday.innerHTML = i;
				}
				eday.className = "now edate";
				con.appendChild(eday);
			} else {
				if (i <= 31) {
					eday.innerHTML = i;
				}
				eday.className = "edate";
				con.appendChild(eday);
			};
		};
	};
	//获取本月1号的周值
	function oneyearoneday(dateObj) {
		var oneyear = new Date();
		var year = dateObj.getFullYear();
		var month = dateObj.getMonth(); //0是12月
		oneyear.setFullYear(year);
		oneyear.setMonth(month); //0是12月
		oneyear.setDate(1);
		return oneyear.getDay();
	};
	//当前是几
	function nowday(dateObj) {
		return dateObj.getDate();
	};
	//获取本月总日数方法
	function alldays(dateObj) {
		var year = dateObj.getFullYear();
		var month = dateObj.getMonth();
		if (isLeapYear(year)) { //闰年
			switch (month) {
				case 0:
					return "31";
					break;
				case 1:
					return "29";
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
	//闰年判断函数
	function isLeapYear(year) {
		if ((year % 4 == 0) && (year % 100 != 0 || year % 400 == 0)) {
			return true;
		} else {
			return false;
		};
	};
	//月份转化方法
	function toyear(dateObj) {
		var month = dateObj.getMonth()
		switch (month) {
			case 0:
				return "1";
				break;
			case 1:
				return "2";
				break;
			case 2:
				return "3";
				break;
			case 3:
				return "4";
				break;
			case 4:
				return "5";
				break;
			case 5:
				return "6";
				break;
			case 6:
				return "7";
				break;
			case 7:
				return "8";
				break;
			case 8:
				return "9";
				break;
			case 9:
				return "10";
				break;
			case 10:
				return "11";
				break;
			case 11:
				return "12";
				break;
			default:
		};
	};
	return val;
}