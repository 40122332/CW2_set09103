from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from models import User
class LoginForm(Form):
  username=StringField('Username', [validators.Required()])
  password=PasswordField('Password', [validators.Required()])

  def __init__(self, *args, **kwargs):
    Form.__init__(self,*args, **kwargs)
    self.user = None

  def validate(self):
    rv=Form.validate(self)
    if not rm:
      return False

    user=User.query.filter_by(
      username=self.username.data).first()
    if user is None:
      self.username.errors.append('Umknown Username')
      return False

    if not user.check_password(self.password.data):
      self.password.errors.append('Invalid Password')
      return False

    self.user=user
    return True
