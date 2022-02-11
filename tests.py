# UNIT TESTS #
import unittest
from flask import request
from website import app
from website.models import Account


class AccountTestCases(unittest.TestCase):
  def setUp(self):
    self.ctx = app.app_context()
    self.ctx.push()
    app.config["SERVER_NAME"] = "alexander.se"
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["WTF_CSRF_METHODS"] = []
    app.config["TESTING"] = True
    # Lurar app lite, så vi kan köra utan webbläsare

  # def test_when_withdraw_not_sufficient_funds_not_able(self):
  #   test_client = app.test_client() # Skapar en test client typ en fake browser
  #   target = Account.query.filter(Account.Id == 1).first()
  #   amount = 10000000000000
  #   before_balance = target.Balance
  #   with test_client:
  #     url = '/account/1?deposit_withdraw=active'
  #     response = test_client.post(url, data={"Choice":"with", "Amount":amount})
  #     print("\n")
  #     print(f"HTTP Status Code: {response.status_code}")
  #     print(f"Balance Before Test '{before_balance}'")
  #     print(f"Balance After Test '{target.Balance}'")
  #     self.assertEqual(before_balance, target.Balance)
  #     assert response.status_code == 302 # Redirect status code

  def test_when_withdraw_minus_amount_not_able(self):
    test_client = app.test_client() # Skapar en test client typ en fake browser
    target = Account.query.filter(Account.Id == 1).first()
    amount = -10
    before_balance = target.Balance
    with test_client:
      url = '/account/1?deposit_withdraw=active'
      response = test_client.post(url, data={"Choice":"with", "Amount":amount})
      print("\n")
      print(f"Amount: {amount}")
      print(f"Balance Before Test '{before_balance}'")
      print(f"Balance After Test '{target.Balance}'")
      self.assertEqual(before_balance, target.Balance)
      assert url.endswith(url) #stannar på sidan

  def test_when_deposit_minus_amount_not_able(self):
    test_client = app.test_client() # Skapar en test client typ en fake browser
    target = Account.query.filter(Account.Id == 1).first()
    amount = -10
    before_balance = target.Balance
    with test_client:
      url = '/account/1?deposit_withdraw=active'
      response = test_client.post(url, data={"Choice":"dep", "Amount":amount})
      print("\n")
      print(f"Amount: {amount}")
      print(f"Balance Before Test '{before_balance}'")
      print(f"Balance After Test '{target.Balance}'")
      self.assertEqual(before_balance, target.Balance)
      assert url.endswith(url) #stannar på sidan

#   def test_when_withdraw_sufficient_funds_able(self):
#     test_client = app.test_client()
#     target = Account.query.filter(Account.Id == 1).first()
#     before_balance = target.Balance
#     amount = 10
#     with test_client:
#       url = '/account/1?deposit_withdraw=active'
#       response = test_client.post(url, data={"Choice":"with", "Amount":amount})
#       print("\n")
#       print(f"HTTP Status Code: {response.status_code}")
#       print(f"Balance Before Test '{before_balance}'")
#       print(f"Balance After Test '{target.Balance}'")
#       self.assertEqual(before_balance-amount, target.Balance)
#       assert response.status_code == 302

#   def test_when_transfering_not_able_no_sufficient_funds(self):
#     test_client = app.test_client()
#     targetSender = Account.query.filter(Account.Id == 1).first()
#     targetReceiver = Account.query.filter(Account.Id == 2).first()
#     before_balance_Sender = targetSender.Balance
#     before_balance_Receiver = targetReceiver.Balance
#     amount = 100000000
#     with test_client:
#       url = '/transfer'
#       response = test_client.post(url, data={"Sender":targetSender.Id, "Receiver":targetReceiver.Id, "Amount":amount})
#       print("\n")
#       print(f"HTTP Status Code: {response.status_code}")
#       print(f"Balance Before Test Sender: '{before_balance_Sender}'")
#       print(f"Balance Before Test Receiver: '{before_balance_Receiver}'")
#       print(f"Balance After Test Sender'{targetSender.Balance}'")
#       print(f"Balance After Test Receiver'{targetReceiver.Balance}'")
#       self.assertEqual(before_balance_Sender, targetSender.Balance)
#       self.assertEqual(before_balance_Receiver, targetReceiver.Balance)
#       assert response.status_code == 302

#   def test_when_transfering_able_with_sufficient_funds(self):
#     test_client = app.test_client()
#     targetSender = Account.query.filter(Account.Id == 1).first()
#     targetReceiver = Account.query.filter(Account.Id == 2).first()
#     before_balance_Sender = targetSender.Balance
#     before_balance_Receiver = targetReceiver.Balance
#     amount = 10
#     with test_client:
#       url = '/transfer'
#       response = test_client.post(url, data={"Sender":targetSender.Id, "Receiver":targetReceiver.Id, "Amount":amount})
#       print("\n")
#       print(f"HTTP Status Code: {response.status_code}")
#       print(f"Balance Before Test Sender: '{before_balance_Sender}'")
#       print(f"Balance Before Test Receiver: '{before_balance_Receiver}'")
#       print(f"Balance After Test Sender'{targetSender.Balance}'")
#       print(f"Balance After Test Receiver'{targetReceiver.Balance}'")
#       self.assertEqual(before_balance_Sender-amount, targetSender.Balance)
#       self.assertEqual(before_balance_Receiver+amount, targetReceiver.Balance)
#       #Alla mina formulär postar med 302 oavsett outcome pga redirect så får kolla annat också
#       #Typ jämföra balances osv före och efter
#       assert response.status_code == 302

#   def test_when_transfering_not_able_with_minus_amount(self):
#     test_client = app.test_client()
#     targetSender = Account.query.filter(Account.Id == 1).first()
#     targetReceiver = Account.query.filter(Account.Id == 2).first()
#     before_balance_Sender = targetSender.Balance
#     before_balance_Receiver = targetReceiver.Balance
#     amount = -10
#     with test_client:
#       url = '/transfer'
#       response = test_client.post(url, data={"Sender":targetSender.Id, "Receiver":targetReceiver.Id, "Amount":amount})
#       print("\n")
#       print(f"Amount trying to send: {amount}")
#       print(f"Balance Before Test Sender: '{before_balance_Sender}'")
#       print(f"Balance Before Test Receiver: '{before_balance_Receiver}'")
#       print(f"Balance After Test Sender'{targetSender.Balance}'")
#       print(f"Balance After Test Receiver'{targetReceiver.Balance}'")
#       self.assertEqual(before_balance_Sender, targetSender.Balance)
#       self.assertEqual(before_balance_Receiver, targetReceiver.Balance)
#       assert url.endswith(request.path)

# class CustomerTestCases(unittest.TestCase):
#   def setUp(self):
#     self.ctx = app.app_context()
#     self.ctx.push()
#     #self.client = app.test_client()
#     app.config["SERVER_NAME"] = "alexander.se"
#     app.config["WTF_CSRF_ENABLED"] = False
#     app.config["WTF_CSRF_METHODS"] = []
#     app.config["TESTING"] = True
#     # Lurar app lite, så vi kan köra utan webbläsare
  
#   def test_when_creating_new_should_validate_name_is_longer_than_three(self):
#     test_client = app.test_client()
#     url = "/addCustomer"
#     date = "2012-04-23"
#     with test_client:
#       response = test_client.post(url, data={"GivenName":"ab", "Surname":"cd", "Streetaddress":"Siggestuna 2", "City":"Uppsala","Zipcode":"19455","Country":"Sweden","CountryCode":"SE","Birthday":date,"NationalId":"19910823-3855","TelephoneCountryCode":46,"Telephone":"0792441155","EmailAddress":"test@test.se"})
#       assert url.endswith(request.path) # Kollar att den inte redirectar, dvs den promptar om för litet namn


#   def test_when_creating_new_should_be_ok_when_name_is_longer_than_three(self):
#     test_client = app.test_client()
#     url = "/addCustomer"
#     date = "2012-04-23"
#     with test_client:
#       response = test_client.post(url, data={"GivenName":"Alexander", "Surname":"Brownes", "Streetaddress":"Testgatan 2", "City":"Testesta","Zipcode":"19455","Country":"Sweden","CountryCode":"SE","Birthday":date,"NationalId":"19920823-9999","TelephoneCountryCode":46,"Telephone":"079352152","EmailAddress":"testaren@testarn.se"})
#       print(f"HTTP Status Code: {response.status_code}")
#       assert response.status_code == 302

if __name__ == "__main__":
  unittest.main()