DROP TABLE if EXISTS user;
DROP TABLE if EXISTS message;
DROP TABLE if EXISTS friends;

CREATE TABLE user(
  id integer primary key autoincrement, 
  username text not null,
  password text not null
);

CREATE TABLE message(
  id integer primary key autoincrement,
  message_text text not null, 
  message_user integer not null,
  FOREIGN KEY (message_user) REFERENCES user(id)
);

CREATE TABLE friends(
  user_one integer not null,
  user_two integer not null,
  status integer not null,
  action_user integer not null,
  FOREIGN KEY (user_one) REFERENCES user(id)
  FOREIGN KEY (user_two) REFERENCES user(id)
 );

INSERT into user
(username,password)values("Kate","$2a$12$xBNa4/8eP0sM6pgJRawt6u0qfPhWtP2WbNmsXlg59jFsTakKmzZQ2");

INSERT into user
(username,password)values("James","$2a$12$xBNa4/8eP0sM6pgJRawt6u0qfPhWtP2WbNmsXlg59jFsTakKmzZQ2");
