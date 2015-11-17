from werkzeug.security import generate_password_hash, \
check_password_hash

class User(object):

  def __init__(self, username, password):
    self.set_password(password)
    self.username = username

  def set_password(self, password):
    self.pw_hash = generate_password_hash(password)

  def get_password(self):
    return self.pw_hash

  def check_password(self, password):
    return check_password_hash(self.pw_hash, password)
