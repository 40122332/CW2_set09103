import ConfigParser
import sqlite3
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
      app.config['log_file'] = config.get("logging","name")
      app.config['log_location'] = config.get("logging","location")
      app.config['log_level'] = config.get("logging","level")
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
    return redirect(url_for('login'))
  else:
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('You logged in as %s'%form.user.username)
    session['logged_in'] = True
    return redirect(url_for('welcome'))
  return render_template('login.html')

@app.route('/new_user', methods=['GET','POST'])
def new():
  error=None
  if request.method == 'POST':
    u=User(request.form['username'], request.form['password'])
  #  g.db.execute('insert into user (username,\
   # password)values(%s,%s)'%(request.form['name'],u.get_password())) 
    g.db.execute('insert into user (username,password) values(\'%s\',\'%s\')'
    %(request.form['name'], u.get_password()))
    g.db.commit()
    return redirect(url_for('welcome'))
  return render_template('new_user.html')

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash("You were logged out")
  return redirect(url_for('welcome'))


if __name__ == "__main__":
  init(app)
  init_db()
  app.run(
      host=app.config['ip_address'],
      port=int(app.config['port']))
