import ConfigParser
from flask import Flask, redirect, url_for, render_template, flash, abort

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

@app.route('/config/')
def config():
  str = []
  str.append('Debug:'+app.config['DEBUG'])
  str.append('port:'+app.config['port'])
  str.append('url:'+app.config['url'])
  str.append('ip_address:'+app.config['ip_address'])
  return '\t'.join(str)

@app.route('/')
def welcome():
  return "hello"


if __name__ == "__main__":
  init(app)
  app.run(
      host=app.config['ip_address'],
      port=int(app.config['port']))
