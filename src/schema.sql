DROP TABLE if EXISTS user;

CREATE TABLE user(
  id integer primary key autoincrement, 
  username text not null,
  password text not null
);

CREATE TABLE message(
  id integer primary key autoincrement,
  message text not null,
  messaeg_user integer not null,
  FOREIGN KEY (message_list) REFERENCES user(id)
);

