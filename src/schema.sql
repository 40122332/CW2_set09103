DROP TABLE if EXISTS user;
DROP TABLE if EXISTS message;

CREATE TABLE user(
  id integer primary key autoincrement, 
  username text not null,
  password text not null
);

CREATE TABLE message(
  id integer primary key autoincrement,
  message text not null,
  message_user integer not null,
  FOREIGN KEY (message_user) REFERENCES user(id)
);

