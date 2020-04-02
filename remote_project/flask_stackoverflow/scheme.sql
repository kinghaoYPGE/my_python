create user 'qa'@'localhost' IDENTIFIED BY 'qa';
drop database if exists 'qa';
create database qa character set = utf8;
grant all on qa.* to 'qa'@'localhost';