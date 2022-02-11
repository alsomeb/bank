from flask import render_template,request,redirect,url_for,flash, Blueprint, current_app
from website.models import db, Account, Customer, Transaction, User, UserRoles, Role
from website.forms import PersonEditForm,MoneyTransferForm,DepositWithdrawForm,ChangeEmailForm,AddCustomerForm, UserRolesForm, AddUserForm
from sqlalchemy.sql import functions
from datetime import datetime
from flask_user import login_required, roles_accepted, roles_required, current_user
from flask_user.password_manager import PasswordManager
from website.services import getCustomerbyId, getAllCustomerAccounts, getAccountTransactions, getAccountById, getUserById, getAllUserRoles, getUserRoleById, getSumAccountsBalance, getAccountCount, getCustomerCount, getAccountCountAndBalanceGroupedByCountry,getCustomerCountByCountry,getUserByEmail,getTopEarnersInCountry,sortTopEarners, sortBalanceByCountry, calcSumPages
from website.azureSearch import client, merge_document, upload_new_document



views = Blueprint('views', __name__)

# User Roles CRUD
@views.route("/userRoles", methods=["POST","GET"])
@roles_required("Admin")
def userRolesPage():
  title = "User Roles"
  #Hämtar alla aktiva Users
  users = getAllUserRoles()

  #CRUD Users
  form = UserRolesForm(request.form)
  formTwo = AddUserForm(request.form)
  addUser = request.args.get('add', False)
  editUser = request.args.get('edit', False)
  userId = int(request.args.get('userId',0)) #User Id
  edit = False
  add = False

  if editUser == 'edit':
    edit = True
    if form.validate_on_submit():
      edit_user = getUserById(userId)
      edit_user.first_name = form.GivenName.data
      edit_user.last_name = form.Surname.data

      if form.EmailAddress.data == "": #Kladdigt men funkar jättebra
        edit_user.email = edit_user.email
      else:
        edit_user.email = form.EmailAddress.data

      if form.Role.data == "admin":
        editRole = getUserRoleById(userId)
        editRole.role_id = 1 #Admin
        db.session.commit()
        flash(f'Updated User: {userId}', 'success')
        return redirect(url_for('views.userRolesPage'))

      if form.Role.data == "cashier":
        editRole = getUserRoleById(userId)
        editRole.role_id = 2 #Cashier
        db.session.commit()
        flash(f'Updated User: {userId}', 'success')
        return redirect(url_for('views.userRolesPage'))

  #Create New User
  if addUser == 'add':
    form = formTwo # Changing Form payload
    add = True
    if form.validate_on_submit():
      addUser = User()
      addUser.first_name = form.GivenName.data
      addUser.last_name = form.Surname.data
      addUser.email = form.EmailAddress.data
      addUser.email_confirmed_at = datetime.utcnow()

      # Hashing mha flasks egna
      password = form.Password.data
      PassManager = PasswordManager(current_app)
      hashedPassword = PassManager.hash_password(password)
      addUser.password = hashedPassword
      db.session.add(addUser)
      db.session.commit()

      # Används för UserRoles för att sätta ID
      theUser = getUserByEmail(form.EmailAddress.data)

      if form.Role.data == "admin":
        newUserRole = UserRoles()
        newUserRole.user_id = theUser.id
        newUserRole.role_id = 1
        db.session.add(newUserRole)
        db.session.commit()
        flash(f'Created Admin User: {addUser.first_name} {addUser.last_name}', 'success')
        return redirect(url_for('views.userRolesPage'))

      if form.Role.data == "cashier":
        newUserRole = UserRoles()
        newUserRole.user_id = theUser.id
        newUserRole.role_id = 2
        db.session.add(newUserRole)
        db.session.commit()
        flash(f'Created Cashier User: {addUser.first_name} {addUser.last_name}', 'success')
        return redirect(url_for('views.userRolesPage'))

  return render_template('userRolesPage.html', title=title, users=users, form=form, formTwo=formTwo, edit=edit, userId=userId, add=add)

# User Profile
@views.route("/profile", methods=["POST","GET"])
@roles_accepted("Admin","Cashier")
def myProfile():
  title = "My Profile"
  form = ChangeEmailForm(request.form)
  value = request.args.get('email', False)
  email = False # False i början
  if value == 'active':
    email = True
    if form.validate_on_submit():
      current_user.email = form.EmailAddress.data
      db.session.commit()
      flash(f'Changed email to {current_user.email}', 'success')
      return redirect(url_for('views.myProfile'))
  return render_template('myProfilePage.html', title=title, form=form, email=email)

# New Customer, måste kommentera bort has_roles i basetemp samt roles_req för att köra tester
@views.route("/addCustomer", methods=["POST","GET"])
@roles_required("Admin") 
def addCustomerPage():
  form = AddCustomerForm(request.form)
  title = "New Customer"
  if form.validate_on_submit():
    addCustomer = Customer()
    addCustomer.GivenName = form.GivenName.data
    addCustomer.Surname = form.Surname.data
    addCustomer.Streetaddress = form.Streetaddress.data
    addCustomer.City = form.City.data
    addCustomer.Zipcode = form.Zipcode.data
    addCustomer.Country = form.Country.data
    addCustomer.CountryCode = form.CountryCode.data
    addCustomer.Birthday = form.Birthday.data
    addCustomer.NationalId = form.NationalId.data
    addCustomer.TelephoneCountryCode = form.TelephoneCountryCode.data
    addCustomer.Telephone = form.Telephone.data
    addCustomer.EmailAddress = form.EmailAddress.data
    db.session.add(addCustomer)
    # 1 Personal Account is given aswell on creating a customer
    newAccount = Account()
    newAccount.AccountType = "Personal"
    newAccount.Created = datetime.utcnow()
    newAccount.Balance = 0
    addCustomer.Accounts.append(newAccount)
    #AZURE ADD
    fetchCustomer = Customer.query.filter(Customer.EmailAddress == addCustomer.EmailAddress).first()
    upload_new_document(str(fetchCustomer.Id), form.GivenName.data, form.Surname.data, form.City.data, form.Streetaddress.data, form.NationalId.data, form.Telephone.data)
    db.session.commit()
    flash(f"New Customer: {addCustomer.GivenName} {addCustomer.Surname}, created", "success")
    return redirect(url_for('views.customerProfile', id=addCustomer.Id))
  return render_template('addCustomerPage.html', title=title, form=form)

@views.route("/editCustomer/<id>", methods=["POST","GET"])
@roles_accepted("Admin","Cashier")
def editCustomerPage(id):
  form = PersonEditForm(request.form)
  customer = getCustomerbyId(id)
  title = "Editing: "

  if request.method == "GET":
    form.GivenName.data = customer.GivenName
    form.Surname.data = customer.Surname
    form.Streetaddress.data = customer.Streetaddress
    form.City.data = customer.City
    form.Zipcode.data = customer.Zipcode
    form.Country.data = customer.Country
    form.CountryCode.data = customer.CountryCode
    form.Birthday.data = customer.Birthday
    form.NationalId.data = customer.NationalId
    form.TelephoneCountryCode.data = customer.TelephoneCountryCode
    form.Telephone.data = customer.Telephone
    form.EmailAddress.data = customer.EmailAddress
    return render_template('editCustomer.html', title=title, customer=customer, form=form)

  if form.validate_on_submit():
    customer.GivenName = form.GivenName.data
    customer.Surname = form.Surname.data
    customer.Streetaddress = form.Streetaddress.data
    customer.City = form.City.data
    customer.Zipcode = form.Zipcode.data
    customer.Country = form.Country.data
    customer.CountryCode = form.CountryCode.data
    customer.Birthday = form.Birthday.data
    customer.NationalId = form.NationalId.data
    customer.TelephoneCountryCode = form.TelephoneCountryCode.data
    customer.Telephone = form.Telephone.data
    customer.EmailAddress = form.EmailAddress.data
    db.session.commit()
    #Azure search Update
    merge_document(str(id), form.GivenName.data, form.Surname.data, form.City.data, form.Streetaddress.data, form.NationalId.data, form.Telephone.data)
    flash(f"Changes Saved Sucessfully", "success")
    return redirect(url_for('views.customerProfile', id=customer.Id))
  return render_template('editCustomer.html', title=title, customer=customer, form=form)


# Måste kommentera bort roles_req för samt i base templ has_roles admin för Unit.Test
@views.route("/transfer", methods=["POST","GET"])
@roles_required("Admin")
def transferMoneyPage():
  title = "Transfer Money"
  form = MoneyTransferForm(request.form)
  if form.validate_on_submit():
    senderAccount = getAccountById(form.Sender.data)
    receiverAccount = getAccountById(form.Receiver.data)
    #Kollar att den hittar kontona
    if senderAccount != None and receiverAccount != None:
      amount = form.Amount.data
      if senderAccount.Balance >= amount:
        senderAccount.Balance -= amount
        receiverAccount.Balance += amount
        # Add to Transactions
        # -- Sender --
        senderTransaction = Transaction()
        senderTransaction.Date = datetime.now()
        senderTransaction.Type = "Credit"
        senderTransaction.Operation = "Transfer"
        senderTransaction.Amount = amount
        senderTransaction.NewBalance = senderAccount.Balance
        senderAccount.Transactions.append(senderTransaction)
        # -- Receiver --
        receiverTransaction = Transaction()
        receiverTransaction.Date = datetime.now()
        receiverTransaction.Type = "Debit"
        receiverTransaction.Operation = "Transfer Received"
        receiverTransaction.Amount = amount
        receiverTransaction.NewBalance = receiverAccount.Balance
        receiverAccount.Transactions.append(receiverTransaction)
        db.session.commit()
        flash(f'Transfered {amount} USD from Account Nr {form.Sender.data} to Account Nr {form.Receiver.data}', 'success')
        return redirect(url_for('views.transferMoneyPage'))
      else:
        flash(f'Not sufficient funds on Sender Account Nr: {form.Sender.data}', 'danger')
        return redirect(url_for('views.transferMoneyPage'))
    else:
      flash(f'Check Account Numbers, doesnt exist in our database', 'danger')
  return render_template('transferMoneyPage.html', title=title,form=form)

#Måste kommentera bort roles accepted för unittester
@views.route("/account/<id>", methods=["POST","GET"])
# @roles_accepted("Admin","Cashier")
def accountProfile(id):
  title = "Account Profile"
  some_account = getAccountById(id)
  #Hämtar namnet för kontoinnehavaren för att visa på sidan som info
  account_owner = getCustomerbyId(some_account.CustomerId)
  #Visar 20 Transactions I taget
  trans = getAccountTransactions(id)
  paginationObject = trans.paginate(1,20,False)

  # -- Deposit -- Withdrawal --
  #används för template för att visa fältet eller inte, för dep/with
  deposit_withdraw = False
  value = request.args.get('deposit_withdraw', False)
  form = DepositWithdrawForm(request.form)

  if value == 'active':
    deposit_withdraw = True
    # Deposit
    if form.validate_on_submit():
      if form.Choice.data == "dep":
        amount = form.Amount.data
        some_account.Balance += amount
        depTransaction = Transaction()
        depTransaction.Date = datetime.now()
        depTransaction.Type = "Debit"
        depTransaction.Operation = "Deposit Cash"
        depTransaction.Amount = amount
        depTransaction.NewBalance = some_account.Balance
        some_account.Transactions.append(depTransaction)
        db.session.commit()
        flash(f"You deposited {amount} USD", "success")
        return redirect(url_for("views.accountProfile", id=some_account.Id))
      # Withdrawal
      if form.Choice.data == "with":
        amount = form.Amount.data
        if some_account.Balance >= amount:
          some_account.Balance -= amount
          withTransaction = Transaction()
          withTransaction.Date = datetime.now()
          withTransaction.Type = "Credit"
          withTransaction.Operation = "Bank Withdrawal"
          withTransaction.Amount = amount
          withTransaction.NewBalance = some_account.Balance
          some_account.Transactions.append(withTransaction)
          db.session.commit()
          flash(f"You withdrew {amount} USD", "success")
          return redirect(url_for("views.accountProfile", id=some_account.Id))
        else:
          flash(f"Not sufficient funds on account", "danger")
          return redirect(url_for("views.accountProfile", id=some_account.Id, deposit_withdraw='active'))
  return render_template("accountProfile.html", title=title, some_account=some_account, account_owner=account_owner, form=form, deposit_withdraw=deposit_withdraw, trans=paginationObject.items)


@views.route("/", methods=["POST","GET"])
@roles_accepted("Admin","Cashier")
def indexPage():
  # Quick Search
  search = request.form.get("customerId")
  if search:
    #Kollar att den hittar en med sökets Id i Db
    found = getCustomerbyId(search)
    if found != None:
      return redirect(url_for("views.customerProfile", id=search))
    else:
        flash(f'{search} doest exist in database', 'danger') #danger boostrap style

  title = "Dashboard Index"
  antalKunder = getCustomerCount()
  antalKonton = getAccountCount()

  # Måste ha båda o zipa dem
  query1 = getAccountCountAndBalanceGroupedByCountry()
  sortedList = sortBalanceByCountry(query1) #Sorterar den för gick inte att sortera med SQL
  query2 = getCustomerCountByCountry()
  result = zip(sortedList,query2) # Zippas och sen skrivs ut i jinjan

  #sqlalch sum() med "functions", samt format på var tredje med ,
  sumAccountsBalance = getSumAccountsBalance()

  country = request.args.get('country','') # country for top earners
  countryName = country # För disp namn på land
  topEarnersList = getTopEarnersInCountry(country) # Visar ej i desc order, funkar ej med SQL

  sortedEarners = sortTopEarners(topEarnersList)

  topEarner = False
  value = request.args.get('topEarner', False)
  if value == 'active':
    topEarner = True

  return render_template("startPage.html", title=title, antalKunder=antalKunder, antalKonton=antalKonton, sumAccountsBalance=sumAccountsBalance, result=result, sortedEarners=sortedEarners, topEarner=topEarner, countryName=countryName)

@views.route("/customer/<id>", methods=["POST","GET"]) #<id> , PARAMETER, samma i funktionen
@roles_accepted("Admin","Cashier")
def customerProfile(id):
  title = "Customer Profile: "
  customer = getCustomerbyId(id)
  accounts = getAllCustomerAccounts(id)
  # Hämta Total Balance från alla konton sammanslaget,
  # Customer var används aldrig men behövs med, pga joinad query:
  total = 0
  for customer, account in accounts:
    total = total + account.Balance
  return render_template("customerProfile.html", title=title, customer=customer, accounts=accounts, total=total)


@views.route("/search")
@roles_accepted("Admin","Cashier")
def searchPage():
  # Default andra parametern
  sortColumn = request.args.get('sortColumn', 'id')
  sortOrder = request.args.get('sortOrder', 'asc')
  # måste ha en tom string med default värde
  searchWord = request.args.get('q','')
  # Anv för Paginiation
  page = int(request.args.get('page', 1))

  title = "Search"
  all_customers = Customer.query.filter(Customer.GivenName.like('%' + searchWord + '%') |
   Customer.Surname.like('%' + searchWord + '%') |
   Customer.City.like('%' + searchWord + '%') |
   Customer.Id.like(searchWord))

  # Sorting
  if sortColumn == "name":
    if sortOrder == "desc":
      all_customers = all_customers.order_by(Customer.GivenName.desc())
    else:
      all_customers = all_customers.order_by(Customer.GivenName.asc())
  
  if sortColumn == "id":
    if sortOrder == "desc":
      all_customers = all_customers.order_by(Customer.Id.desc())
    else:
      all_customers = all_customers.order_by(Customer.Id.asc())
  
  if sortColumn == "address":
    if sortOrder == "desc":
      all_customers = all_customers.order_by(Customer.Streetaddress.desc())
    else:
      all_customers = all_customers.order_by(Customer.Streetaddress.asc())

  if sortColumn == "city":
    if sortOrder == "desc":
      all_customers = all_customers.order_by(Customer.City.desc())
    else:
      all_customers = all_customers.order_by(Customer.City.asc())

  if sortColumn == "nationalId":
    if sortOrder == "desc":
      all_customers = all_customers.order_by(Customer.NationalId.desc())
    else:
      all_customers = all_customers.order_by(Customer.NationalId.asc())

  # Pagination, inbyggt i flask, 50 per page
  paginationObject = all_customers.paginate(page,50,False)

  return render_template("searchPage.html", 
  title=title,
  sortColumn=sortColumn,
  sortOrder=sortOrder,
  all_customers=paginationObject.items, 
  page=page, 
  has_next = paginationObject.has_next,
  has_prev = paginationObject.has_prev,
  pages= paginationObject.pages,
  q = searchWord)



@views.route("/search2", methods=["POST","GET"])
@roles_accepted("Admin","Cashier")
def azureSearch():
  title = "Azure Search Engine"
  sortColumn = request.args.get('sortColumn','GivenName')
  sortOrder = request.args.get('sortOrder', 'asc')
  page = int(request.args.get('page', 1))
  searchWord = request.args.get('q', '*')
  
  skip = (page-1) * 50
  result = client.search(search_text=searchWord, include_total_count=True, skip=skip, top=50, order_by=sortColumn + " " + sortOrder)
  alla = result

  summaSearch = result.get_count() # för antal hittade resultat
  top = 50 # antal res per sida
  antalSidor = calcSumPages(result)

  return render_template("azureSearch.html", title=title, alla=alla, sortColumn=sortColumn, sortOrder=sortOrder, page=page, q=searchWord, summaSearch=summaSearch, skip=skip, top=top, antalSidor=antalSidor)
