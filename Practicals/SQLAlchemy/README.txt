------ PART 1 ------

1) Install Flask-SQLAlchemy
  pip Install Flask-SQLAlchemy

2) Create packages
  a)  Create die "models" and "resources"
  b)  create file "__init__.py" in models and resources dir

3) Move resource files under "resources" folder
  a)  item.py
  b)  user.py

4) Update codes with new packages paths
  a)  from resources.user import User, UserRegister
  b)  from resources.item import Item, ItemList

------ PART 2 ------
Models - Internal for code
Resources - External that is API reference (customer facing)

1) Move User class from resources/user.py to models/user.py

2) Move other method except API to models/item.py

------ PART 3 ------
1) Under code create new file 'db.py'
2) import SQLAlchemy
  from flask_sqlalchemy import SQLAlchemy

3) Assign db to SQLAlchemy() object
  db = SQLAlchemy()

4) import the db in app.py inside __main__ and initialize app with SQLAlchemy
  from db import db
  db.init_app(app)

5) Extend the model class objects to SQLAlchemy by
  a)  import db in both model files
        from db import db
  b) models\user.py - User(db.Model)
  c) models\item.py - Item(db.Model)

6) Tell SQLAlchemy the tables and the columns

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

------ PART 4 ------
1) In app.py for  SQLAlchemy to know database, include
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

2) Creating table using SQLAlchemy
@app.before_first_request #decorator - create DB before any 1st request that comes to app
def create_tables():
    db.create_all()
