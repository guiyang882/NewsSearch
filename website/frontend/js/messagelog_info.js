var page_Len = 50;
var total_Pages = 0;
var cur_Page = 1;

showPage(cur_Page);
addSendUserName();

function showPage(page_id){
    var begin = (page_id-1)*page_Len+1;
    var end = begin+page_Len-1;

    var contents = {"CONTENTS":"MESSAGELOG","begin":begin,"end":end};
    send_Data_Backend(contents);
}

function addSendUserName() {
    var contents = {"CONTENTS":"USERNAMES"};
    send_Data_Backend(contents);
}

function send_Data_Backend(content) {
    $.ajax({
        　　　　　　url: 'http://127.0.0.1:8080/',
        　　　　　　type: 'GET',
        　　　　　　data: content,
        　　　　　　//调小超时时间会引起异常
        　　　　　　timeout: 5000,
        　　　　　　//请求成功后触发
        　　　　　　success: function (data) {
                    if(data.name == "MessageLog" || data.name == "UserSendLog"){
                        showMessageLogInfo(data);    
                    }
                    if(data.name == "UserNames") {
                        showUsersName(data);
                    }
              },
        　　　　　　//请求失败遇到异常触发
        　　　　　　error: function (xhr, errorInfo, ex) { console.log(errorInfo);},
        　　　　　　//完成请求后触发。即在success或error触发后触发
        　　　　　　complete: function (xhr, status) { console.log(status); },
        　　　　　　//发送请求前触发
        　　　　　　beforeSend: function (xhr) {
            　　　　　　xhr.setRequestHeader('Content-Type', 'application/json;charset=utf-8');
            },
    　　　　　　//是否使用异步发送
    　　　　　　async: true
    　　　　})
}

function showUsersName(data) {
    if(data.name == "UserNames") {
        var select_Obj = document.getElementById("Select_To");
        select_Obj.options.length = 1;
        for(var index in data.data){
            select_Obj.add(new Option(data.data[index],data.data[index]));
        }
    }
}

function showMessageLogInfo(data){
    if(data.name == "MessageLog" || data.name == "UserSendLog"){
        var sendlogUL = document.getElementById("list_SendLog_UL");

        while(document.getElementById("li_id")){
            var item = document.getElementById("li_id");
            item.remove();
        }

        var messageLog = data.data;
        var length = data['total_length'];
        total_Pages = parseInt(length/page_Len);
        document.getElementById("hint_totalPage").placeholder = "共 "+total_Pages+" 页";

        for(var index in messageLog) {
            var li = $('<li/>',{"class":"myli_content","id":"li_id"});
            var span_id = $('<span/>');
            span_id.text(messageLog[index].id);

            var span_from = $('<span/>');
            span_from.text(messageLog[index].from);

            var span_to = $('<span/>');
            span_to.text(messageLog[index].to);

            var span_mode = $('<span/>');
            span_mode.text(messageLog[index].mode);

            var span_time = $('<span/>');
            span_time.text(messageLog[index].time);

            var span_status = $('<span/>');
            span_status.text("已发送");

            var span_contents = $('<span/>');   
            var textarea = $('<textarea/>',{"rows":2,"cols":20});
            textarea.text(messageLog[index].contents);
            textarea.appendTo(span_contents);

            span_id.appendTo(li);
            span_from.appendTo(li);
            span_to.appendTo(li);
            span_mode.appendTo(li);
            span_time.appendTo(li);
            span_status.appendTo(li);
            span_contents.appendTo(li);

            li.appendTo(sendlogUL);
        }
    }
}

function  getPagePre(){
    if(cur_Page-1>0){
        cur_Page = cur_Page-1;
        showPage(cur_Page);
    }else{
        window.alert("这已经是第一页");
    }
}

function getPageNext() {
    if(cur_Page+1<=total_Pages){
        cur_Page = cur_Page+1;
        showPage(cur_Page);
    }else{
        window.alert("这已经是最后一页");
    }
}

function gotoIDPage() {
    var id = document.getElementById("hint_totalPage").value;
    var n_idth = parseInt(id);
    
    console.log(n_idth);
    if(!isNaN(n_idth)){
        console.log(n_idth);
        if(n_idth > total_Pages){
            window.alert("这已经是最后一页");
            document.getElementById("hint_totalPage").placeholder = "共 "+total_Pages+" 页";
        }else if(n_idth < 1){
            window.alert("这已经是第一页");   
            document.getElementById("hint_totalPage").placeholder = "共 "+total_Pages+" 页";
        }else{
            cur_Page = n_idth;
            showPage(n_idth);   
            document.getElementById("hint_totalPage").placeholder = "共 "+total_Pages+" 页";
        }
    }
}

function filterUserSendLog(name) {
    console.log(name);
    var contents = {"CONTENTS":"FILTERUSER","NAME":name};
    send_Data_Backend(contents);
}