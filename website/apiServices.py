from datetime import datetime
from website.models import Transaction

# Classes and functions used by website API
class CustomerApiModel:
  Id = 0
  GivenName = ""
  Surname = ""
  Streetaddress = ""
  City = ""
  Zipcode = ""
  Country = ""
  CountryCode = ""
  Birthday = datetime.utcnow()
  NationalId = ""
  TelephoneCountryCode = 0
  Telephone = ""
  EmailAddress = ""

class TransactionApiModel:
  Id = 0
  Type = ""
  Operation = ""
  Date = datetime.utcnow()
  Amount = 0
  NewBalance = 0
  AccountId = 0

def _mapCustomerToApi(customer)->CustomerApiModel:
  customerApiModel = CustomerApiModel()
  customerApiModel.Id = customer.Id
  customerApiModel.GivenName = customer.GivenName
  customerApiModel.Surname = customer.Surname
  customerApiModel.Streetaddress = customer.Streetaddress
  customerApiModel.City = customer.City
  customerApiModel.Zipcode = customer.Zipcode
  customerApiModel.Country = customer.Country
  customerApiModel.CountryCode = customer.CountryCode
  customerApiModel.Birthday = customer.Birthday
  customerApiModel.NationalId = customer.NationalId
  customerApiModel.TelephoneCountryCode = customer.TelephoneCountryCode
  customerApiModel.Telephone = customer.Telephone
  customerApiModel.EmailAddress = customer.EmailAddress
  return customerApiModel

def _mapTransactionToApi(transaction)->TransactionApiModel:
  transactionApiModel = TransactionApiModel()
  transactionApiModel.Id = transaction.Id
  transactionApiModel.Type = transaction.Type
  transactionApiModel.Operation = transaction.Operation
  transactionApiModel.Date = transaction.Date
  transactionApiModel.Amount = transaction.Amount
  transactionApiModel.NewBalance = transaction.NewBalance
  transactionApiModel.AccountId = transaction.AccountId
  return transactionApiModel

def getAllTransactionsByAccountId(id)->list[Transaction]:
  transactionList = Transaction.query.filter(Transaction.AccountId == id).order_by(Transaction.Date.desc()).all()
  return transactionList