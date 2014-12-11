drop table if exists userdata;
create table userdata (
  username text primary key,
  password text not null
);

insert into userdata(username,password) values("admin","admin");

drop table if exists userinfo;
create table userinfo (
  username text primary key,
  displayname text,
  u_gender text,
  u_birth text,
  u_email text,
  u_image text,
  u_address text,
  u_state text,
  u_city text,
  u_interests text,
  u_bio text,
  foreign key (username) references userdata(username)
);

insert into userinfo(username,u_city,u_interests) values("admin","CP","Football,Video Games");


drop table if exists event;
create table event (
  eventid integer primary key autoincrement,
  e_title text,
  e_detail text,
  e_time text,
  e_address text,
  e_city text,
  e_state text,
  e_tag text,
  category text
);

insert into event(e_title,e_city,category) values ("Hi","CP","Football");
insert into event(e_title,e_city,category) values ("Hi2","AL","Football");
insert into event(e_title,e_city,category) values ("Hi3","CP","Swimming");
insert into event(e_title,e_city,category) values ("Hi4","CP","Football,Swimming");

drop table if exists event_user;
create table event_user(
  eventid integer primary key,
  creator text,
  member text,
  membercount integer,
  foreign key (eventid) references event(eventid)
);

insert into event_user(eventid,creator,member,membercount) values(1,"admin","goo,boo,foo",3);
insert into event_user(eventid,creator,member,membercount) values(2,"admin","goo,boo,admin",3);
insert into event_user(eventid,creator,member,membercount) values(3,"admin","goo",1);
insert into event_user(eventid,creator,member,membercount) values(4,"admin","goo,hoo",2);

drop table if exists parenlist;
create table parenlist(
 child text primary key,
 parent text
);

insert into parenlist(child,parent) values("Football","Sport");
insert into parenlist(child,parent) values("Swimming","Sport");
insert into parenlist(child,parent) values("Art","Arts & Entertainment");
insert into parenlist(child,parent) values("Fiction","Arts & Entertainment");
insert into parenlist(child,parent) values("Film","Arts & Entertainment");
insert into parenlist(child,parent) values("Lean Startup","Business & Career");
insert into parenlist(child,parent) values("Marketing","Business & Career");
insert into parenlist(child,parent) values("Investing","Business & Career");
insert into parenlist(child,parent) values("Social Media","Internet & Technology");
insert into parenlist(child,parent) values("Interaction Design","Internet & Technology");
insert into parenlist(child,parent) values("Cloud Computing","Internet & Technology");
