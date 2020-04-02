drop table if exists sample_blog;
create table sample_blog(
  id integer primary key autoincrement,
  title string not null,
  text string not null
);