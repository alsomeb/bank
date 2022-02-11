# Forms for the website
from flask_wtf import FlaskForm
from wtforms import Form,validators, StringField, SelectField,DateField, ValidationError, PasswordField
from wtforms.fields import IntegerField #HTML5 Int fält
from website.models import User, Customer


class PersonEditForm(FlaskForm):
  GivenName = StringField("First Name", [validators.Length(min=3, max=50, message="First Name Between 3-50 letters")])
  Surname = StringField("Last Name", [validators.Length(min=3, max=50, message="Last Name Between 3-50 letters")])
  Streetaddress = StringField("Street Address", [validators.Length(min=3, max=50, message="Street Address Between 3-50 letters")])
  City = StringField("City", [validators.Length(min=3, max=50, message="City Between 3-50 letters")])
  Zipcode = StringField("Zipcode", [validators.Length(min=1, max=10, message="Zip Code Between 1-10 letters")])
  Country = StringField("Country", [validators.Length(min=3, max=30, message="Country Between 3-50 letters")])
  CountryCode = StringField("Country Code", [validators.Length(min=2, max=3, message="Country Code Between 2-3 letters")])
  Birthday = DateField("Birthday", [validators.DataRequired()])
  NationalId = StringField("National Id", [validators.Length(min=12, max=20, message="Country Between 3-50 letters")])
  TelephoneCountryCode = IntegerField("Telephone Country Code", [validators.NumberRange(1,999, message="Between 2-3")])
  Telephone = StringField("TelePhone", [validators.Length(min=3, max=20, message="TelePhone Between 3-20 letters")])
  EmailAddress = StringField("Email Address", [validators.Email(), validators.Length(min=3, max=30, message="Check Email")])
  #Custom Validators
  def validate_EmailAddress(self, EmailAddress):
    customer = Customer.query.filter_by(EmailAddress=EmailAddress.data).first()
    if customer:
      currentEmail = customer.EmailAddress
      if EmailAddress.data == currentEmail:
        return EmailAddress.data
      else:
        raise ValidationError('Email Already Exist')
  
  def validate_NationalId(self, NationalId):
    customer = Customer.query.filter_by(NationalId=NationalId.data).first()
    if customer:
      currentNationalId = customer.NationalId
      if NationalId.data == currentNationalId:
        return NationalId.data
      else:
        raise ValidationError('National Id already exists')


class MoneyTransferForm(FlaskForm):
  Sender = IntegerField("From Account Nr",[validators.NumberRange(min=1), validators.DataRequired(message="Please enter Account Nr")])
  Receiver = IntegerField("To Account Nr",[validators.NumberRange(min=1),validators.DataRequired(message="Please enter Account Nr")])
  Amount = IntegerField("Amount, USD",[validators.NumberRange(min=1),validators.DataRequired(message="Please enter amount above 0")])


class DepositWithdrawForm(FlaskForm):
  Choice = SelectField("Select Operation", [validators.DataRequired(message="Please choose one")], choices=[("dep","Deposit"), ("with","Withdraw")])
  Amount = IntegerField("Amount, USD",[validators.NumberRange(min=1), validators.DataRequired(message="Please enter amount above 0")])


class ChangeEmailForm(FlaskForm):
  EmailAddress = StringField("Email Address", [validators.DataRequired(), validators.Email(), validators.Length(min=3, max=250, message="Check Email")])
  #Custom Validators
  def validate_EmailAddress(self, EmailAddress):
    user = User.query.filter_by(email=EmailAddress.data).first()
    if user:
      currentEmail = user.email
      if EmailAddress.data == currentEmail:
        return EmailAddress.data
      else:
        raise ValidationError('Email Already Exist')

  
class AddCustomerForm(FlaskForm):
  GivenName = StringField("First Name", [validators.Length(min=3, max=50, message="First Name Between 3-50 letters")])
  Surname = StringField("Last Name", [validators.Length(min=3, max=50, message="Last Name Between 3-50 letters")])
  Streetaddress = StringField("Street Address", [validators.Length(min=3, max=50, message="Street Address Between 3-50 letters")])
  City = StringField("City", [validators.Length(min=3, max=50, message="City Between 3-50 letters")])
  Zipcode = StringField("Zipcode", [validators.Length(min=1, max=10, message="Zip Code Between 1-10 letters")])
  Country = StringField("Country", [validators.Length(min=3, max=30, message="Country Between 3-50 letters")])
  CountryCode = StringField("Country Code", [validators.Length(min=2, max=3, message="Country Code Between 2-3 letters")])
  Birthday = DateField("Birthday", [validators.DataRequired()], format="%Y-%m-%d")
  NationalId = StringField("National Id", [validators.Length(min=12, max=20, message="Nat Id Between 12-20 letters")])
  TelephoneCountryCode = IntegerField("Telephone Country Code", [validators.NumberRange(1,999, message="Between 2-3")])
  Telephone = StringField("TelePhone", [validators.Length(min=3, max=20, message="TelePhone Between 3-20 letters")])
  EmailAddress = StringField("Email Address", [validators.Email(), validators.Length(min=3, max=30, message="Check Email")])
  #Custom Validators
  def validate_EmailAddress(self, EmailAddress):
    customer = Customer.query.filter_by(EmailAddress=EmailAddress.data).first()
    if customer:
      raise ValidationError('Email Already Exist')
  
  def validate_NationalId(self, NationalId):
    customer = Customer.query.filter_by(NationalId=NationalId.data).first()
    if customer:
      raise ValidationError('National Id already exists')


class UserRolesForm(FlaskForm):
  GivenName = StringField("First Name", [validators.Length(min=3, max=100, message="First Name Between 3-100 letters")])
  Surname = StringField("Last Name", [validators.Length(min=3, max=100, message="Last Name Between 3-100 letters")])
  Role = SelectField("Select Role", [validators.DataRequired(message="Please choose one")], choices=[("admin","Admin"), ("cashier","Cashier")])
  EmailAddress = StringField("Email Address", render_kw={"placeholder":"Leave Email Blank If No Change"})

  #Custom Validators
  def validate_EmailAddress(self, EmailAddress):
    user = User.query.filter_by(email=EmailAddress.data).first()
    if user:
      raise ValidationError('Email Already Exist')


class AddUserForm(FlaskForm):
  GivenName = StringField("First Name", [validators.Length(min=3, max=100, message="First Name Between 3-100 letters")])
  Surname = StringField("Last Name", [validators.Length(min=3, max=100, message="Last Name Between 3-100 letters")])
  Password = PasswordField("Enter Password", [validators.Length(min=5, max=20, message="Between 6-20 letters"), validators.EqualTo('Confirm', message="Password must match")])
  Confirm = PasswordField("Confirm Password", [validators.Length(min=5, max=20, message="Between 6-20 letters")])
  Role = SelectField("Select Role", [validators.DataRequired(message="Please choose one")], choices=[("admin","Admin"), ("cashier","Cashier")])
  EmailAddress = StringField("Email Address", render_kw={"placeholder":"Leave Email Blank If No Change"})

  #Custom Validators
  def validate_EmailAddress(self, EmailAddress):
    user = User.query.filter_by(email=EmailAddress.data).first()
    if user:
      raise ValidationError('Email Already Exist')

