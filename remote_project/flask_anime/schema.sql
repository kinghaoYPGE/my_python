drop database if exists anime_recommend;
create database anime_recommend;
use anime_recommend;
drop table if exists user;
create table user(
  id int,
  name varchar(20),
  primary key(id)
);

drop table if exists anime;
create table anime(
  id int,
  name varchar(20),
  brief varchar(100),
  primary key(id)
);

insert into user values(1,"Tom");
insert into anime values(279,"a","A");
insert into anime values(3494,"b","B");
insert into anime values(3377,"c","C");
insert into anime values(3452,"d","D");
insert into anime values(782,"e","E");
insert into anime values(3421,"f","F");
insert into anime values(2730,"g","G");

drop table if exists anime_style;
create table anime_style(
  anime_id int,
  style_id int,
  foreign key(anime_id) references anime(id)
);


insert into anime_style values(279,26);
insert into anime_style values(279,30);
insert into anime_style values(279,32);
insert into anime_style values(279,8);
insert into anime_style values(279,7);

insert into anime_style values(3494,9);
insert into anime_style values(3494,19);
insert into anime_style values(3494,29);
insert into anime_style values(3494,46);

insert into anime_style values(3377,34);
insert into anime_style values(3377,7);
insert into anime_style values(3377,18);

insert into anime_style values(3452,30);
insert into anime_style values(3452,32);
insert into anime_style values(3452,7);
insert into anime_style values(3452,22);

insert into anime_style values(782,30);
insert into anime_style values(782,32);
insert into anime_style values(782,7);
insert into anime_style values(782,1);
insert into anime_style values(782,50);

insert into anime_style values(3421,30);
insert into anime_style values(3421,32);
insert into anime_style values(3421,7);
insert into anime_style values(3421,22);

insert into anime_style values(2730,11);
insert into anime_style values(2730,30);
insert into anime_style values(2730,22);

drop table if exists user_anime;
create table user_anime(
  user_id int,
  anime_id int,
  foreign key(user_id) references user(id),
  foreign key(anime_id) references anime(id)
);


insert into user_anime  values(1,782);
insert into user_anime  values(1,3421);
insert into user_anime  values(1,2730);

commit;