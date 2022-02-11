from flask import Blueprint, request,jsonify
from website.services import getAccountTransactions
from website.models import Customer, Transaction
from website.apiServices import _mapCustomerToApi, _mapTransactionToApi, getAllTransactionsByAccountId

api = Blueprint('api', __name__)



# Visa 1 spec customer
@api.route("/api/customer/<id>")
def getCustomer(id):
  customer = Customer.query.filter(Customer.Id == id).first()
  customerApiModel = _mapCustomerToApi(customer)
  return jsonify(customerApiModel.__dict__)

@api.route("api/account/<id>")
def getTrans(id):
  transactionList = getAllTransactionsByAccountId(id)
  listTransactionsByAccount = []
  for transaction in transactionList:
    transactionApiModel = _mapTransactionToApi(transaction)
    listTransactionsByAccount.append(transactionApiModel)
  return jsonify([transaction.__dict__ for transaction in listTransactionsByAccount])


# Används för "Show 20 more" på account trans
@api.route("/api/<id>/trans")
def transactionAccount(id):
  page = int(request.args.get('page',2))
  listaMedTrans = []
  trans = getAccountTransactions(id)
  paginationObject = trans.paginate(page,20,False)
  hasMore = paginationObject.has_next

  #trans innehåller de 20 transobjekt som ska visas
  for trans in paginationObject.items:
    t = {"Id":trans.Id, "Date":trans.Date, "Type":trans.Type, "Operation":trans.Operation, "Amount":trans.Amount, "NewBalance":trans.NewBalance, "AccountId":trans.AccountId}
    listaMedTrans.append(t)
  return jsonify(listaMedTrans, hasMore)
