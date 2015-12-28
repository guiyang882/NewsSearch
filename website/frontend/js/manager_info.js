var g_user_data = "";

(function ($){

    $('#user_Refresh').click(function () {
    　　　　$.ajax({
        　　　　　　url: 'http://127.0.0.1:8080/',
        　　　　　　type: 'GET',
        　　　　　　data: "CONTENTS=MANAGERS",
        　　　　　　//调小超时时间会引起异常
        　　　　　　timeout: 3000,
        　　　　　　//请求成功后触发
        　　　　　　success: function (data) {
                console.log(data.data);
                g_user_data = data.data;
                showUserInfo(data); 
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
    });

    $(document).ready(function() {
        $('.dropdown-menu li a').hover(
        function() {
            $(this).children('i').addClass('icon-white');
        },
        function() {
            $(this).children('i').removeClass('icon-white');
        });
    });

})(jQuery)

function send_Data_Backend(content) {
    $.ajax({
        　　　　　　url: 'http://127.0.0.1:8080/',
        　　　　　　type: 'GET',
        　　　　　　data: content,
        　　　　　　//调小超时时间会引起异常
        　　　　　　timeout: 3000,
        　　　　　　//请求成功后触发
        　　　　　　success: function (data) { 
                g_user_data = data.data;
                showUserInfo(data); 
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

function showUserInfo(data){
    if(data.name == "ManagersInfo"){
        console.log('Here Show User Info !!');
        if(document.getElementById("BackEndUserTable") == null) {
            var total_show_div = document.getElementById("ShowUserInfo_DIV");
            var table_info = getTable(data.data);
            table_info.appendTo(total_show_div);
        }else if(document.getElementById("BackEndUserTable") != null) {
            var edit_face = document.getElementById("edit_face_table");
            console.log(edit_face);
            if(edit_face != null){
                document.getElementById("edit_btn_save").remove();
                document.getElementById("edit_btn_reset").remove();
                edit_face.remove();
            }

            var table_user = document.getElementById("BackEndUserTable");
            table_user.remove();
            var total_show_div = document.getElementById("ShowUserInfo_DIV");
            var table_info = getTable(data.data);
            table_info.appendTo(total_show_div);
        }
    }
}

function getTable(perf) {
    var table = $('<table/>', {"class": "table table-striped table-bordered table-condensed",'id':"BackEndUserTable"});

    var head_thead = getTableItemHeader();
    head_thead.appendTo(table);
    var content_tbody = $('<tbody/>');

    for (var i = 0; i < perf.length; i++) {
        var td_item = getTableItemContent(i+1,perf[i]);
        td_item.appendTo(content_tbody);
    }
    content_tbody.appendTo(table);
    return table;
}

function getTableItemHeader() {
    var td_list = ['ID','姓名','微信号','手机号码','其他联系方式','状态','备注','操作'];
    var thead = $('<thead/>');
    var title_row = $('<tr/>');
    for(var index in td_list) {
        var nametd = $('<th/>', {text: td_list[index]});
        nametd.appendTo(title_row);
    }
    title_row.appendTo(thead);
    return thead
}

function getTableItemContent(index,Item) {
    var title_row = $('<tr/>',{"class":"list-users"});
    var content_id = $('<td/>', {text:index});
    content_id.appendTo(title_row);
    var content_name = $('<td/>', {text:Item.name});
    content_name.appendTo(title_row);
    var content_wx_id = $('<td/>', {text:Item.wx_id});
    content_wx_id.appendTo(title_row);
    var content_phone = $('<td/>', {text:Item.phone});
    content_phone.appendTo(title_row);
    var content_other_info = $('<td/>', {text:Item.other_info});
    content_other_info.appendTo(title_row);
    var content_active = $('<td/>');
    var span = $('<span/>',{"class":"label label-success"});
    if(Item.status == 1) {
        span.text("Active");
    }
    if(Item.status == 0) {
        span.text("InActive");
    }
    content_active.append(span);
    content_active.appendTo(title_row);

    var content_comments = $('<td/>',{text:Item.comments});
    content_comments.appendTo(title_row);

    var content_div = $('<div/>',{'class':"btn-group"});
    var content_a = $('<a/>',{'class':'btn btn-mini dropdown-toggle','data-toggle':'dropdown','href':'#'});
    content_a.text("操作");
    var div_span = $('<span/>',{'class':"caret"});
    div_span.appendTo(content_a);
    content_a.appendTo(content_div);
    var ul = $('<ul/>',{'class':'dropdown-menu'});

    var li_edit = $('<li/>');
    var li_edit_a = $('<a/>',{'id':index,'href':"#",'onclick':'edit_user_info(this);'});
    li_edit_a.text("编辑");
    var li_edit_i = $('<i/>');
    li_edit_a.appendTo(li_edit);
    li_edit_i.appendTo(li_edit);
    li_edit.appendTo(ul);

    var li_Delete = $('<li/>');
    var li_Delete_a = $('<a/>',{'id':index,'href':"#",'onclick':'delete_user_info(this);'});
    li_Delete_a.text("删除");
    var li_Delete_i = $('<i/>');
    li_Delete_a.appendTo(li_Delete);
    li_Delete_i.appendTo(li_Delete);
    li_Delete.appendTo(ul);

    var li_Details = $('<li/>');
    var li_Details_a = $('<a/>',{'id':index,'href':"#",'onclick':'send_Message_info(this);'});
    li_Details_a.text("发送信息");
    var li_Details_i = $('<i/>');
    li_Details_a.appendTo(li_Details);
    li_Details_i.appendTo(li_Details);
    li_Details.appendTo(ul);

    ul.appendTo(content_div);
    var td_actions = $('<td/>');
    td_actions.append(content_div);
    
    td_actions.appendTo(title_row);

    return title_row
}

function edit_user_info(obj) {
    show_edit_face(obj.id);
    console.log(obj.id);
}

function delete_user_info(obj) {
    var user_id = obj.id;
    var single_data = g_user_data[user_id-1];
    var data_list = [single_data.name,single_data.wx_id,single_data.phone,single_data.other_info,single_data.status,single_data.comments];
    var content = {"operator":"managers-deleted","name":single_data.name,"wx_id":single_data.wx_id,"phone":single_data.phone};
    send_Data_Backend(content);
}

function send_Message_info(obj) {
    show_send_face(obj.id);
    console.log(obj.id);
    console.log("send info");
}

function show_send_face(index) {
    single_user = g_user_data[index-1];
    
    var td_list = ['姓名','微信号','手机号码','其他联系方式','状态','备注'];
    var bk_info = [single_user.name,single_user.wx_id,single_user.phone,single_user.other_info,single_user.status,single_user.comments];

    if(document.getElementById("send_btn_reset") == null) {
        var table = $('<table>',{"class": "table table-striped table-condensed","id":"send_face_table"});

        var tr1 = $('<tr/>',{"class":"list-users"});

        var td1 = $('<td/>',{'style':'text-align:center'});
        var select_Obj = $('<select/>',{"class":"list-users", "id":"send_select"});
        select_Obj.append("<option value='send_hint'>-- 发送方式 --</option>");
        wx_value = "send_wx_id"
        wx_text = bk_info[1]
        select_Obj.append("<option id='send_wx_id' value='"+wx_value+"'>微信: "+wx_text+"</option>");
        phone_value = "send_phone"
        phone_text = bk_info[2]
        select_Obj.append("<option id='send_phone' value='"+phone_value+"'>手机: "+phone_text+"</option>");
        others_value = "send_others"
        others_text = bk_info[3]
        select_Obj.append("<option id='send_others' value='"+others_value+"'>其它: "+others_text+"</option>");
        select_Obj.appendTo(td1);
        td1.appendTo(tr1);

        var tr2 = $('<tr/>',{"class":"list-users"});
        var td2 = $('<td/>',{'style':'text-align:center'});
        var textarea = $('<textarea rows="5" cols="40">');
        textarea.appendTo(td2);
        td2.appendTo(tr2);

        var tr3 = $('<tr/>',{"class":"list-users"});
        var td3 = $('<td/>',{'style':'text-align:center'});
        var button_submit = $("<input class='btn btn-success' type='button' value=' 发 送 ' id='send_btn_save' onclick='send_User_Message()' style='margin-right:40px'/>");
        var button_reset = $('<input/>',{'class':'btn btn-success','type':'button','value':' 重 置 ','id':'send_btn_reset','onclick':'reset_User_Message()','name':index});
        button_submit.appendTo(td3);
        button_reset.appendTo(td3);
        td3.appendTo(tr3);

        var operator_div = document.getElementById("ShowOperator_DIV");
        tr1.appendTo(table);
        tr2.appendTo(table);
        tr3.appendTo(table);
        table.appendTo(operator_div);

    }else if(document.getElementById("send_btn_reset").name == index) {
        console.log("Same thing, Do nothing !!");
    }else if(document.getElementById("send_btn_reset").name != index) {
        //update the info
        var tmp_Wx = document.getElementById("send_wx_id");
        tmp_Wx.text = "微信: "+bk_info[1];
        var tmp_Phone = document.getElementById("send_phone");
        tmp_Phone.text = "手机: "+bk_info[2];
        var tmp_Other = document.getElementById("send_others");
        tmp_Other.text = "其它: "+bk_info[3];
        var tmp_btn = document.getElementById("send_btn_reset");
        tmp_btn.name = index;
    }
}

//send wx or phone to user, that include the message
function send_User_Message() {
    console.log("Send user Message !!");
}

function reset_User_Message() {
    console.log("Reset User Message !!");
}

//show the edit interface to user, that edit the user info
function show_edit_face(index) {
    single_user = g_user_data[index-1];
    
    var td_list = ['姓名','微信号','手机号码','其他联系方式','状态','备注'];
    var id_list = ['name','wx_id','phonenum','other_info','status','comments'];
    var bk_info = [single_user.name,single_user.wx_id,single_user.phone,single_user.other_info,single_user.status,single_user.comments];

    if(document.getElementById("edit_btn_reset") == null) {
        var table = $('<table/>',{"class": "table table-striped table-bordered table-condensed","id":"edit_face_table"});

        for(var i in td_list) {
            var content_tr = $('<tr/>',{"class":"list-users"});
            var content_name = $('<td/>',{text:td_list[i],'style':'text-align:center'});
            var content_data = $('<td/>',{'style':'text-align:center'});
            var input_info = $('<input/>',{'class':'btn','type':'text','value':bk_info[i],'id':id_list[i]});
            input_info.appendTo(content_data);
            content_name.appendTo(content_tr);
            content_data.appendTo(content_tr);
            content_tr.appendTo(table);
        }

        var button_submit = $("<input class='btn btn-success' type='button' value=' 保 存 ' id='edit_btn_save' onclick='save_change_user_info()' style='margin-right:40px'/>");
        var button_reset = $('<input/>',{'class':'btn btn-success','type':'button','value':' 重 置 ','id':'edit_btn_reset','onclick':'reset_user_info()','name':index});
        var operator_div = document.getElementById("ShowOperator_DIV");
        table.appendTo(operator_div);
        button_submit.appendTo(operator_div);
        button_reset.appendTo(operator_div);

    }else if(document.getElementById("edit_btn_reset").name == index) {
        console.log("Same thing, Do nothing !!");

    }else if(document.getElementById("edit_btn_reset").name != index) {
        //update the data
        for(var i in td_list) {
            var tmp = document.getElementById(id_list[i]);
            tmp.value = bk_info[i]
        }
        var tmp = document.getElementById("edit_btn_reset");
        tmp.name = index;
        console.log("show other info is "+index);
    }
    
    console.log("Show Edit Face !!!");
}

function save_change_user_info() {
    var user_id = document.getElementById("edit_btn_reset").name;
    var id_list = ['name','wx_id','phonenum','other_info','status','comments'];
    var new_user_info = new Array();
    for(var i in id_list) {
        var item = document.getElementById(id_list[i]);
        new_user_info.push(item.value);
    }
    var single_data = g_user_data[user_id-1];
    var data_list = [single_data.name,single_data.wx_id,single_data.phone,single_data.other_info,single_data.status,single_data.comments];
    var b_Same = true;
    for(var i in data_list) {
        if(data_list[i] != new_user_info[i]) {
            b_Same = false;
            break;
        }
    }
    if(b_Same == false) {
        //post data to server
        console.log("Please Enter the code here, to fill the data !");
    }
}

function reset_user_info() {
    var user_id = document.getElementById("edit_btn_reset").name;
    var single_data = g_user_data[user_id-1];
    var id_list = ['name','wx_id','phonenum','other_info','status','comments'];
    var data_list = [single_data.name,single_data.wx_id,single_data.phone,single_data.other_info,single_data.status,single_data.comments];
    for(var i in id_list) {
        var item = document.getElementById(id_list[i]);
        item.value = data_list[i];
    }
}