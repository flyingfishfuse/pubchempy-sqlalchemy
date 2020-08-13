
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, Request ,Config
from pubchempy_sqlalchemy

################################################################################
##############                      CONFIG                     #################
################################################################################
#TESTING = False
TEST_DB            = 'sqlite://'
DATABASE_HOST      = "localhost"
DATABASE           = "chembot"
DATABASE_USER      = "admin"
SERVER_NAME        = "lookup tool"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + DATABASE_HOST + DATABASE_USER + ".db"

class Config(object):
    if TESTING == True:
        SQLALCHEMY_DATABASE_URI = TEST_DB
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    elif TESTING == False:
        SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
        SQLALCHEMY_TRACK_MODIFICATIONS = False


try:
    pubchempy_database = Flask(__name__ , template_folder=templates )
    pubchempy_database.config.from_object(Config)
    database = SQLAlchemy(pubchempy_database)
    database.init_app(pubchempy_database)
except Exception:
    redprint(Exception.with_traceback)

###############################################################################
# from stack overflow
#In the second case when you're just restarting the app I would write a 
#test to see if the table already exists using the reflect method:

#db.metadata.reflect(engine=engine)

#Where engine is your db connection created using create_engine(), and see 
#if your tables already exist and only define the class if the table is undefined.

#this will clear the everything?
database.metadata.clear()
