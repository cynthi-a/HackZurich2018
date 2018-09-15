from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

class User(db.Model):
    __tablename__ = 'User'

    name = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    drug = db.Column(db.Integer)

    def __init__(self, name=None, password=None, drug=None):
        self.name = name
        self.password = password
        self.drug = drug

class Drugs(db.Model):
    __tablename__ = 'Drugs'

    drugId = db.Column(db.IntegerField)

    def __init__(self, drugId=None):
        self.drugId = drugId

'''
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
'''

# Create tables.
Base.metadata.create_all(bind=engine)
    #db.session.commit()