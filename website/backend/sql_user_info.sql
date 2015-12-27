create database if not exists user;

show databases;
use user;

create table if not exists t_user(
    name varchar(20),
    wx_id varchar(50),
    phone varchar(20),
    other_info varchar(20),
    status boolean,
    comments varchar(200)
)ENGINE=MyISAM  DEFAULT CHARSET=utf8;

create table if not exists t_manage_user(
    name varchar(20),
    wx_id varchar(20),
    phone varchar(20),
    other_info varchar(20),
    status boolean,
    comments varchar(200)
)ENGINE=MyISAM DEFAULT CHARSET=utf8;

create table if not exists t_send_log(
    id int(11) NOt NULL AUTO_INCREMENT,
    from_user varchar(100),
    to_user varchar(50),
    comm_mode varchar(20),
    time varchar(50),
    status varchar(30),
    contents TEXT,
    primary key(id)

)ENGINE=MyISAM DEFAULT CHARSET=utf8;

alter table t_send_log add column id int(11) NOT NULL AUTO_INCREMENT;
