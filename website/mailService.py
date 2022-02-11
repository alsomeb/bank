from flask import Blueprint, request
from website.models import Customer, Transaction, Account
from website import mail
from flask_mail import Message

mailService = Blueprint('mailService', __name__)

@mailService.route("/sendTestEmail")
def sendEmail():
  msg = Message('Hello from the other side!', sender = 'alex@fakebank.se', recipients = ['test@test.se'])
  msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
  mail.send(msg)
  return "Message sent!"
