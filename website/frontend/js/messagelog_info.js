var page_Len = 50;
var total_Pages = 0;
var key_default = "旅行";

showPage(key_default);

function showPage(key_info) {
	var contents = {
		"CONTENTS" : "SEARCH",
		"QUERY" : key_info
	};
	console.log(contents);
	send_Data_Backend(contents);
}

function send_Data_Backend(content) {
	$.ajax({
		　　url : 'http://127.0.0.1:8080/',
		　　type : 'GET',
		　 data : content,
		　　 //调小超时时间会引起异常
		　　timeout : 5000,
		　　 //请求成功后触发
		　　success : function (data) {
			if (data.name == "search") {
				showMessageLogInfo(data);
			}
		},
		　　 //请求失败遇到异常触发
		　　error : function (xhr, errorInfo, ex) {
			console.log(errorInfo);
		},
		　　 //完成请求后触发。即在success或error触发后触发
		　　complete : function (xhr, status) {
			console.log(status);
		},
		　　 //发送请求前触发
		　　beforeSend : function (xhr) {
			xhr.setRequestHeader('Content-Type', 'application/json;charset=utf-8');
		},
		　　　　 //是否使用异步发送
		　　　　async : true
	})
}

function showMessageLogInfo(data) {
    console.log(data);
    
	var sendlogUL = document.getElementById("list_SendLog_UL");
	while (document.getElementById("li_id")) {
		var item = document.getElementById("li_id");
		item.remove();
	}

	var messageLog = data.data;

	for (var index in messageLog) {
		var li = $('<li/>', {
				"class" : "myli_content",
				"id" : "li_id"
			});

		var span_from = $('<span/>');
		span_from.text(messageLog[index].news_title);

		var span_to = $('<span/>');
		span_to.text(messageLog[index].news_source);

		var span_mode = $('<span/>');
		span_mode.text(messageLog[index].news_date);

		var span_contents = $('<span/>');
		var textarea = $('<textarea/>', {
				"rows" : 2,
				"cols" : 20
			});
		textarea.text(messageLog[index].news_content);
        textarea.appendTo(span_contents);
        
        var span_key = $('<span/>');
        var key_area = $('<textarea/>', {
				"rows" : 2,
				"cols" : 20
			});
		key_area.text(messageLog[index].news_key);
        key_area.appendTo(span_key);

		span_from.appendTo(li);
		span_to.appendTo(li);
		span_mode.appendTo(li);
		span_key.appendTo(li);
		span_contents.appendTo(li);

		li.appendTo(sendlogUL);
	}

}

function gotoIDPage() {
	key_default = document.getElementById("hint_totalPage").value;

	console.log(key_default);
	showPage(key_default);
}
