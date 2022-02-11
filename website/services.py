## Funktioner som används i routes
from website.models import Customer,Account, Transaction, db, User, UserRoles, Role
from sqlalchemy.sql import functions
import operator
import math

# Hämtar Person Object
def getCustomerbyId(id)->Customer:
  customer = Customer.query.filter(Customer.Id == id).first()
  return customer

# Hämtar Alla Account som tillhör Customer, joinar
def getAllCustomerAccounts(id):
  accounts = db.session.query(Customer, Account).join(Account).filter(Customer.Id == id).all()
  return accounts

#Hämtar trans för specific Account Id
def getAccountTransactions(id)->Transaction:
  transactions = Transaction.query.filter(Transaction.AccountId == id).order_by(Transaction.Date.desc())
  return transactions

# Hämtar "some_account" för att kunna visa Account.AccountType
def getAccountById(id)->Account:
  some_account = Account.query.filter_by(Id=id).first()
  return some_account

# Get User By Id
def getUserById(id)->User:
  user = User.query.filter(User.id == id).first()
  return user

# Function used by User Crud
def getAllUserRoles():
  users = db.session.query(UserRoles, User, Role).join(User).join(Role).order_by(User.id.desc()).all()
  return users

# Function used by User Crud
def getUserRoleById(userId)->UserRoles:
  user = UserRoles.query.filter(UserRoles.user_id == userId).first()
  return user

# Customer Count, Accounts Sum Grouped by Country
def getCustomerCountByCountry():
  query = db.session.query(Customer.Country, functions.count(Customer.Country)).group_by(Customer.Country).all()
  return query

# 
def getAccountCountAndBalanceGroupedByCountry():
  query = db.session.query(functions.count(Account.CustomerId), functions.sum(Account.Balance)).join(Customer).group_by(Customer.Country).all()
  return query
  
# Sum Accounts in DB
def getSumAccountsBalance()->str:
  sum = "{:,}".format(db.session.query(functions.sum(Account.Balance)).scalar())
  return sum

def getCustomerCount()->int:
  antalKunder = Customer.query.count()
  return antalKunder

def getAccountCount()->int:
  antalKonton = Account.query.count()
  return antalKonton

def getUserByEmail(email)->User:
  user = User.query.filter(User.email==email).first()
  return user

def getTopEarnersInCountry(country:str):
  query = db.session.query(Customer.Id, functions.sum(Account.Balance)).join(Account).filter(Customer.Country==country).group_by(Customer.Id).all()
  return query


# får en lista med touple där andra värdet är saldo, första är id, tar reverse på den == Desc order
# använder operator import
def sortTopEarners(list)->list[tuple]:
  list.sort(key=operator.itemgetter(1), reverse=True)
  list = list[:10] # Begränsat bara till 10
  sortedEarners = []
  for customer in list:
    customerObject = Customer.query.filter(Customer.Id == customer[0]).first()
                            #objektet      # summan av saldon för kunden = lista med touples
    sortedEarners.append((customerObject, customer[1]))
  return sortedEarners


def sortBalanceByCountry(list)->list[tuple]: # används för att sortera ländernas saldo
  list.sort(key=operator.itemgetter(1), reverse=True)
  return list

def calcSumPages(result:float)->int: # lösning för paginering 
  summaSearch = result.get_count()
  antalResPerSida = 50
  antalSidor = summaSearch/antalResPerSida
  antalSidor = math.ceil(antalSidor)
  return antalSidor
