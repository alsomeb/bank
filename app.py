#RUNFILE
from flask_migrate import Migrate,upgrade
from website import app
from website.models import db,seedData
from website.azureSearch import createIndex, addDocuments

#Migrate
migrate = Migrate(app,db)

if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(db)
        createIndex() # Azure Search
        addDocuments() # Azure Search
    app.run(debug=True) #debug=True dev