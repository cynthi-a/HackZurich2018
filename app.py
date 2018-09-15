#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, session, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import requests
import json
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


########## MODDELS #############


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.email = email
        self.password = password



class Drugs(db.Model):
    __tablename__ = 'Drugs'

    drugId = db.Column(db.Integer, primary_key=True)

    def __init__(self, drugId=None):
        self.drugId = drugId



# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('forms/login.html', form=form)
    else:
        name = str(form.name)
        passw = str(form.password)
        email = str(form.email)
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        new_user = User(username=str(form.name), password=str(form.password), email=str(form.email))
        db.session.add(new_user)
        db.session.commit()
        return render_template('pages/home.html', form=form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot' )
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/search')
def searchDrug():
    form = SearchDrugForm(request.form)
    #return render_template('forms/search_drugs.html', form=form, testuser = testuser) 
    return render_template('forms/search_drugs.html', form=form)

@app.route('/search/result', methods = ['POST', 'GET'])
def searchResult():
   if request.method == 'POST':
      drugname = request.form['drugname']
      url = 'https://health.axa.ch/hack/api/drugs?name=' + drugname
      response = requests.get(url, headers={"Authorization":"awesome attention"})

      #parse api response
      drugs = json.loads(response.text)

      # loop thourgh all returned objects and all their strings
      drugsList = []
      for drug in drugs:
        drugsList.append(drug)

      global drugId
      drugId = drugs[0]["swissmedicIds"]
      #setDrugId(drugs[0]["swissmedicIds"])
      return render_template("pages/searchresult.html", drugslist=drugsList)

@app.route('/add')
def addDrug():
    return render_template("pages/add_drug.html", result = drugId)


@app.route('/interaction')
def checkInteraction():
    #TODO: get list of drugs

    #getNormIdByName(name)

    name1 = 'aspirin'
    name2 = 'test'
    #get RxNorm
    RxUrl = "https://rxnav.nlm.nih.gov/REST/rxcui?name=" + name1
    RxResponse = requests.get(RxUrl)
    print("----RESPONSE-----")
    print(RxResponse.text)
    response = RxResponse.text
    normId = response["rxnormId"]
    print("-----PARSE----")
    #print(normId)

    return render_template("pages/interaction.html")

#def getNormIdByName(name)
#    RxUrl = "https://rxnav.nlm.nih.gov/REST/rxcui?name=" + name
#    RxResponse = requests.get(RxUrl)




# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':

    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
