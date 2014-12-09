drop table if exists userdata;
create table userdata (
  username text primary key,
  password text not null
);

insert into userdata(username,password) values("admin","admin");

drop table if exists userinfo;
create table userinfo (
  username text primary key,
  u_gender text,
  u_email text,
  u_image text,
  u_state text,
  u_city text,
  u_interests text,
  foreign key (username) references userdata(username)
);

insert into userinfo(username,u_city,u_interests) values("admin","CP","football,video games");


drop table if exists event;
create table event (
  eventid integer primary key autoincrement,
  e_title text,
  e_detail text,
  e_time text,
  e_address text,
  category text
);

insert into event(e_title,e_address,category) values ("Hi","CP","football");
insert into event(e_title,e_address,category) values ("Hi2","VA","football");
insert into event(e_title,e_address,category) values ("Hi3","CP","swimming");
insert into event(e_title,e_address,category) values ("Hi4","CP","football,swimming");

drop table if exists event_user;
create table event_user(
  eventid integer primary key,
  creator text,
  member text,
  membercount integer,
  foreign key (eventid) references event(eventid)
);

insert into event_user(eventid,creator,member,membercount) values(1,"admin","goo,boo,foo",3);
insert into event_user(eventid,creator,member,membercount) values(2,"admin","goo,boo,foo",3);
insert into event_user(eventid,creator,member,membercount) values(3,"admin","goo",1);
insert into event_user(eventid,creator,member,membercount) values(4,"admin","goo,hoo",2);

drop table if exists parenlist:
create table parenlist(
 child text primary key,
 parent text
);

insert into parenlist(child,parent) values("football","sport");
insert into parenlist(child,parent) values("swimming","sport");
