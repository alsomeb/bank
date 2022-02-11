from datetime import datetime
now = datetime.now()

#helt vanligt klass som har properties
#blackbox
class ConfigDebug():
  # Flask settings
  SECRET_KEY = 'A521sK5B25X'

  # Flask-SQLAlchemy settings 
  # DBEAVER useSSL = TRUE när connect
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:sparven23@localhost/bank' # File-Based SQL db
  # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://alexdb:SparveN23@brundb.mysql.database.azure.com/bank' # File-Based SQL db
  SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

  # Flask mail smtp server settings
  MAIL_SERVER = '127.0.0.1'
  MAIL_PORT = 1025
  MAIL_USE_SSL = False
  MAIL_USE_TLS = False
  MAIL_USERNAME = 'email@fakebank.com'     
  MAIL_PASSWORD = 'password'
  MAIL_DEFAULT_SENDER = '"Fake Bank" <noreply@fakebank.com>'

  # Flask-User settings
  USER_APP_NAME = "Fake Bank Corp"      # Shown in and email templates and page footers
  USER_APP_VERSION = "Version 1337"
  USER_COPYRIGHT_YEAR = f"{now.year}"
  USER_CORPORATION_NAME = "Fake Bank"
  USER_ENABLE_EMAIL = True        # Enable email aution
  USER_ENABLE_USERNAME = False    # Disable username authentication
  USER_EMAIL_SENDER_NAME = USER_APP_NAME
  USER_EMAIL_SENDER_EMAIL = "noreply@fakebank.com"
  USER_ENABLE_REGISTER = False # Allow new users to register
  USER_ENABLE_INVITE_USER = False # Allow unregistered users to be invited
  USER_REQUIRE_INVITATION = False # Only Invited Users may register