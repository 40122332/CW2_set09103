import ConfigParser
import sqlite3
import bcrypt
from flask import Flask, redirect, url_for, render_template, flash, abort,\
request, session, g
from contextlib import closing
from login_form import LoginForm
from models import User

DATABASE = '/tmp/flaskr.db'
DEBUG =True
SECRET_KEY ='\xd8\xae/\xee\xd9\xb1\xfc\x85\x85\xb2\xea\xc2\x7f\xeb\x86\x8b\xfdKh\x01\x82h\xea\x17'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def init(app):
  config = ConfigParser.ConfigParser()
  try:
      config_location = "etc/defaults.cfg"
      config.read(config_location)
      app.config['DEBUG'] = config.get("config","debug")
      app.config['ip_address'] = config.get("config", "ip_address")
      app.config['port'] = config.get("config", "port")
      app.config['url'] = config.get("config","url")
    #  app.config['log_file'] = config.get("logging","name")
    #  app.config['log_location'] = config.get("logging","location")
    #  app.config['log_level'] = config.get("logging","level")
  except:
    print"Could not read configs from: ", config_location

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route('/config/')
def config():
  str = []
  str.append('Debug:'+app.config['DEBUG'])
  str.append('port:'+app.config['port'])
  str.append('url:'+app.config['url'])
  str.append('ip_address:'+app.config['ip_address'])
  return '\t'.join(str)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def welcome():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    cur = g.db.execute('select message."message_text" from message inner join user on message."message_user"=user."id" where user.username=?',[session.get('username')])
    message = [dict(message_text=row[0])for row in cur.fetchall()]
    cur1 = g.db.execute('select id from user where username =?',[session.get('username')])
    if request.method == 'POST':
      return redirect(url_for('friend_search', search=request.form['search']))
    if not session.get('new_user'):
      (row,) = cur1.fetchone()
      session['id']=row
      cur2 = g.db.execute('select * from friends where (user_one = ? or\
      user_two=?) and status = ?',[session.get('id'),session.get('id'),0])
      notifacation = [dict(user_one=row[0],user_two=row[1],status=row[2],action_user=row[3])for row in cur2.fetchall()]
      return render_template('posts.html', message=message, notifacation=notifacation )
    else:
      flash('welcom New user')
      return render_template('posts.html', message=message, notifacation=notifacation)

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    user = request.form['username']
    pw = request.form['password']
    if check_auth(user,pw):
      session['logged_in']=True
      session['username']=user
      return redirect(url_for('welcome'))
    flash('could not log in')
    return redirect(url_for('welcome'))

@app.route('/new_user', methods=['GET','POST'])
def new():
  error=None
  if request.method == 'POST':
    u=User(request.form['username'], request.form['password'])
    pas=u.get_password()
    nam=u.get_username()
    g.db.execute('insert into user (username,password)values(?,?)',[nam, pas])
    flash(nam)
    flash(pas)
    g.db.commit()
    session['logged_in'] = True
    session['new_user'] = True
    return redirect(url_for('welcome'))
  return render_template('new_user.html')

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  session.pop('new_user', None)
  session.pop('username', None)
  session.pop('id', None)
  flash("You were logged out")
  return redirect(url_for('welcome'))

def check_auth(username, password):
  cur = g.db.execute('select username, password from user where username = ? ',[username])
  result = cur.fetchall()
  all = result[0]
  u = all[0]
  p = all[1]
  print u, p
  #result_u=[dict(name=row[0])for row in cur.fetchall()]
  #result_pass=[dict(pw=row[1])for row in cur.fetchall()]

  #print result_u, result_pass

  #result_user = get_use(result_u)
  #result_pw = get_pass(result_pass)
  if (username == u) and p == bcrypt.hashpw(password.encode('utf-8'),p):
    return True
  return False

@app.route('/message')
def message_page():
  return render_template('message.html')

@app.route('/message_create', methods=['GET','POST'])
def add_message():
  mess=request.form['message']
  use=session.get('id')
  print use
  g.db.execute('insert into \
  message(message_text,message_user)values(?,?)',[mess,use])
  g.db.commit()
  return redirect(url_for('welcome'))

@app.route('/world_feed')
def world():
  cur = g.db.execute('select message_text from message')
  messages = [dict(message = row[0])for row in cur.fetchall()]
  return render_template('world_feed.html', messages=messages)

@app.route('/search/')
def friend_search():
  search_friend=request.args.get('search', '')
  cur = g.db.execute('select id,username from user where username like?',["%"+search_friend+"%"])
  names = [dict(id=row[0],name=row[1])for row in cur.fetchall()]
  return render_template('friend_search.html', names = names)

@app.route('/friend_request', methods=['GET','POST'])
def friend_notify():
  add=request.form['id']
  print"got here one %s"%add
  g.db.execute('insert into friends(user_one,user_two, status,\
  action_user)values (?,?,?,?)',[session.get('id'),add,0,session.get('id')])
  g.db.commit()
  print "got_here"
  return redirect(url_for('welcome'))

@app.route('/adding_friend', methods=['GET','POST'])
def add_friend():
  g.db.execute('update friends set status=1')


if __name__ == "__main__":
  init(app)
  init_db()
  app.run(
      host=app.config['ip_address'],
      port=int(app.config['port']))
