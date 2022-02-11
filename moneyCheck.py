# REGLER: en enskild transaktion större än 15000 kr, 
# Eller totala transaktioner de senaste tre dygnen (72h) från aktuellt tidpunkt större än 23000
from website.models import Customer, Transaction, Account, db
from datetime import timedelta,datetime
from termcolor import cprint
from website import app
from website import mail
from flask_mail import Message
from sqlalchemy.sql import functions



def checkSingleTransActionBy_x_days(x_days,countryName):
  customers = db.session.query(Account, Transaction, Customer).join(Customer).join(Transaction).filter(Transaction.Amount > 15000).filter(Transaction.Date > (datetime.now() - timedelta(days=x_days))).filter(Customer.Country == countryName).order_by(Transaction.Date.desc()).all()
  return customers

def checkAmountOfTotalTransactions(countryName):
  customers = db.session.query(Customer.Id, Customer.GivenName, Customer.Surname,  functions.sum(Transaction.Amount)).select_from(Customer).join(Account).join(Transaction).filter(Customer.Country==countryName).filter(Transaction.Date > (datetime.now() - timedelta(days=3))).group_by(Account.CustomerId).all()
  return customers


def runScan():
  listCountryNames = getAllCountries()
  for nameCountry in listCountryNames:
    listOfMails = []
    resultTwo = checkAmountOfTotalTransactions(nameCountry) 
    result = checkSingleTransActionBy_x_days(3, nameCountry)
    if not result and not resultTwo:
      cprint("--------------------------------------------------", 'green', attrs=['bold'])
      cprint(f"Country: {nameCountry} - No suspicious Activity", 'green', attrs=['bold'])
      cprint("--------------------------------------------------", 'green', attrs=['bold'])
      continue
    
    # checking total sums
    for customerId, customerFirstName, customerLastName, sum in resultTwo:
      if sum > 23000:
        cprint(f"---------COUNTRY {nameCountry}-----------------------------", 'red', attrs=['bold'])
        cprint(f"Id: {customerId} {customerFirstName} {customerLastName} has sent a total of: {sum}", 'red', attrs=['bold'])
        cprint("--------------------------------------------------", 'red', attrs=['bold'])
        listOfMails.append(f"Id: {customerId} - {customerFirstName} {customerLastName}\nHas Sent Total: {sum}\n")

     # single trans
    for account, transaction, customer in result:
      cprint(f"---------COUNTRY {nameCountry}-------------------------", 'red', attrs=['bold'])
      cprint(f"Id: {customer.Id}", 'red', attrs=['bold'])
      cprint(f"Name: {customer.GivenName} {customer.Surname}", 'red', attrs=['bold'])
      cprint(f"Country: {customer.Country}", 'red', attrs=['bold'])
      cprint(f"AccountNr: {account.Id}", 'red', attrs=['bold'])
      cprint(f"TransactionNr: {transaction.Id} - Date: {transaction.Date}", 'red', attrs=['bold'])
      cprint(f"Amount: {transaction.Amount}", 'red', attrs=['bold'])
      cprint(f"Type: {transaction.Type} - Operation: {transaction.Operation}", 'red', attrs=['bold'])
      cprint("--------------------------------------------------", 'red', attrs=['bold'])
      listOfMails.append(f"{customer.GivenName} {customer.Surname}\nAccountId: {account.Id}\nTransactionId: {transaction.Id}\nAmount: {transaction.Amount}\nType: {transaction.Type} - Operation: {transaction.Operation}\nDate: {transaction.Date}\n")
    
    #SENDING MAILS TO DEPARTMENTS
    with mail.connect() as conn:
      message = "" #Tom str i början
      for messages in listOfMails:
        message = message + str(messages) + "\n"
        subject = "Potential Money Laundring from Daily Scan"
        msg = Message(recipients=[f"{nameCountry}@fakebank.se"], body=message, subject=subject)
      conn.send(msg)
  cprint(f"Scan Complete, emails have been sent with potential threats to departments", 'green', attrs=['bold'])

def getAllCountries():
  list = []
  for customer in Customer.query.all():
    if customer.Country not in list:
      list.append(customer.Country)
  return list

if __name__  == "__main__":
    with app.app_context():
      runScan()

