create table users (id serial primary key, username text, auth text);
create table verifications(bearer text, timeout serial);
create table userrelations(id serial primary key, userid serial, relation serial, type smallint);
create table messages(id serial primary key, root serial, userid serial, content text, time serial);
create table games(id serial primary key, name text, slug text, cover text);
create table gamepreferences(id serial primary key, userid serial, game serial, rating smallint);
create table usergroups(id serial primary key, name text);
create table usergroupregister(id serial primary key, userid serial, inviter serial, usergroup serial, rights smallint, verified boolean, accepted boolean);
create table events(id serial primary key, owner serial, usergroup serial, name text, gameid serial, description text, created serial, ends serial, optupper smallint, optlower smallint);
create table eventinvites(id serial primary key, event serial, userid serial);
create table eventparticipants(id serial primary key, userid serial, event serial);
create table eventgamevotes(id serial primary key, userid serial, event serial, game serial, rating smallint);
create table eventdatevotes(id serial primary key, userid serial, event serial, date text, hour smallint);
create table comments(id serial primary key, userid serial, event serial, target serial, content text, time serial);