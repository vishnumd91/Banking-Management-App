from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,BooleanField,SubmitField,RadioField
from wtforms.validators import DataRequired,EqualTo,ValidationError
from app_package.models import User

class LoginForm(FlaskForm):
    username=StringField("Username:",validators=[DataRequired()])
    password=PasswordField("Password:",validators=[DataRequired()])
    remember_me=BooleanField("Remember Me")
    submit=SubmitField("Sign in")
    
class RegistrationForm(FlaskForm):
    username=StringField("Username:",validators=[DataRequired()])
    password=PasswordField("Password:",validators=[DataRequired()])
    password2=PasswordField("Reenter Password:",validators=[DataRequired(),EqualTo("password")])
    submit=SubmitField("Sign up")
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username exists,choose another one")

class CreationForm(FlaskForm):
    cid=IntegerField("account no:",validators=[DataRequired()])
    name=StringField("customername:",validators=[DataRequired()])
    acctype=RadioField('customertype', choices = [('ordinary','ordinary'),('prime','prime')])
    balance=IntegerField("customerbalance:",validators=[DataRequired()])
    mobile=IntegerField("customermobile:",validators=[DataRequired()])
    aadhar=IntegerField("customeraadhar:",validators=[DataRequired()])
    submit=SubmitField("Add Customer")
    
class WithdrawForm(FlaskForm):
    cid=IntegerField("Customer account no:",validators=[DataRequired()])
    amt=IntegerField("Amount to Withdraw:")
    
    submit=SubmitField("Withdraw")
    
class DepositForm(FlaskForm):
    cid=IntegerField("Customer account no:",validators=[DataRequired()])
    amt=IntegerField("Amount to be deposited:")
    submit=SubmitField("Deposit")
    
class DeleteForm(FlaskForm):
    cid=IntegerField("Customer account no:",validators=[DataRequired()])
    
    
    submit=SubmitField("Delete")
    
class BalanceForm(FlaskForm):
    cid=IntegerField("Customer account no:",validators=[DataRequired()])
    
    
    submit=SubmitField("Check Balance")
    
class ConfirmForm(FlaskForm):
    cid=IntegerField("Customer account no:",validators=[DataRequired()])
    submit=SubmitField("confirm")
    
    
    
