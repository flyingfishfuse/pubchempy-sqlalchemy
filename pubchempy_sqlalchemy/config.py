# -*- coding: utf-8 -*-
################################################################################
##      Pubchempy / SqlAlchemy Caching Extension - Sqlite3/base64             ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
####
################################################################################
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, Request ,Config
# Database functions are at the bottom
# Database Models are above them
# then above that are the random variables necessary for program operation
# above that is the database configuration
###################################################################################
# Color Print Functions
###################################################################################
import colorama
from colorama import init
init()
from colorama import Fore, Back, Style
blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None
# inline colorization for lambdas in a lambda
makered    = lambda text: Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL
makegreen  = lambda text: Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL
makeblue   = lambda text: Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL
makeyellow = lambda text: Fore.YELLOW + ' ' +  text + ' ' + Style.RESET_ALL
yellow_bold_print = lambda text: print(Fore.YELLOW + Style.BRIGHT + ' {} '.format(text) + Style.RESET_ALL) if (TESTING == True) else None
################################################################################
##############                      CONFIG                     #################
################################################################################
TESTING = True
TEST_DB            = 'sqlite://'
DATABASE_HOST      = "localhost"
DATABASE           = "pubchempy_sqlalchemy"
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
    pubchempy_database = Flask(__name__ )
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

###################################################################################
# Stuff
###################################################################################
list_to_string       = lambda list_to_convert: ''.join(list_to_convert)
GRAB_DESCRIPTION     = True
pubchem_search_types = ["iupac_name", "cid", "cas"]
search_validate      = lambda search: search in pubchem_search_types 
API_BASE_URL         = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

element_list = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', \
        'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', \
        'Magnesium', 'Aluminum', 'Silicon', 'Phosphorus', 'Sulfur', \
        'Chlorine', 'Argon', 'Potassium', 'Calcium', 'Scandium', \
        'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt',\
        'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', \
        'Selenium', 'Bromine', 'Krypton', 'Rubidium', 'Strontium', \
        'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium',\
        'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium', \
        'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon', \
        'Cesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', \
        'Neodymium', 'Promethium', 'Samarium', 'Europium', 'Gadolinium', \
        'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', \
        'Ytterbium','Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', \
        'Rhenium', 'Osmium', 'Iridium', 'Platinum', 'Gold', 'Mercury', \
        'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', \
        'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium', \
        'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', \
        'Americium', 'Curium', 'Berkelium', 'Californium', \
        'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', \
        'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', \
        'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium', \
        'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', \
        'Moscovium', 'Livermorium', 'Tennessine']

symbol_list = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', \
        'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', \
        'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', \
        'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', \
        'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', \
        'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', \
        'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', \
        'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', \
        'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', \
        'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts']


class Compound(database.Model):
    __tablename__       = 'Compound'
    __table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer, \
                            index=True, \
                            primary_key = True, \
                            unique=True, \
                            autoincrement=True)
    cid                         = database.Column(database.String(16))
    iupac_name                  = database.Column(database.Text)
    cas                         = database.Column(database.String(64))
    smiles                      = database.Column(database.Text)
    formula                     = database.Column(database.Text)
    molweight                   = database.Column(database.String(32))
    charge                      = database.Column(database.String(32))
    #TODO: serialize data and use proper type
    bond_stereo_count           = database.Column(database.Text)
    bonds                       = database.Column(database.Text)
    rotatable_bond_count        = database.Column(database.Text)
    multipoles_3d               = database.Column(database.Text)
    mmff94_energy_3d            = database.Column(database.Text)
    mmff94_partial_charges_3d   = database.Column(database.Text)
    atom_stereo_count           = database.Column(database.Text)
    h_bond_acceptor_count       = database.Column(database.Text)
    feature_selfoverlap_3d      = database.Column(database.Text)
    cactvs_fingerprint          = database.Column(database.Text)
    description                 = database.Column(database.Text)
    image                       = database.Column(database.Text)

    def __repr__(self):
        return 'IUPAC name         : {} \n \
CAS                : {} \n \
Formula            : {} \n \
Molecular Weight   : {} \n \
Charge             : {} \n \
CID                : {} \n \
Description:       : {} \n '.format(self.iupac_name, self.cas , self.formula, self.molweight,self.charge, self.cid, self.description)


###################################################################################
# Database stuff
###################################################################################
class Database_functions():
    def __init__(self):
        print("This class is lazy, don't call on it!")

    def compound_by_formula(self, formula_str : str):
        return Compound.query.filter_by(formula=formula_str).first()

    def Compound_by_id(self, cid_of_compound : str):
        """
        Returns a compound from the local DB
        Returns FALSE if entry does not exist
        :param: cid_of_compound
        """
        cid_passed = cid_of_compound
        try:
            #return database.session.query(Compound).filter_by(Compound.cid == cid_passed)
            #                                * See that right there? "cid" ?
            return Compound.query.filter_by(cid = cid_passed).first()
            # SQL-Alchemy interprets that as the record to lookup
            # it DOES NOT evaluate the contents of a variable
            # do not forget that! It uses the name as is! The contents do not matter!
        except Exception as derp:
            print(derp)
            redprint("[-] Failure in Compound_by_id")
            redprint(derp.with_traceback)
            return False

    ################################################################################
    def internal_local_database_lookup(self, entity : str, id_of_record:str ):
        """
        feed it a formula or CID followed buy "formula" or "cid" or "iupac_name
        searches by record and entry
        Returns False and raises and exception/prints exception on error
        Returns an SQLAlchemy database object if record exists
        """
        try:
            greenprint("[+] performing internal lookup")
            if search_validate(id_of_record): # in pubchem_search_types:
                kwargs  = { id_of_record : entity}
                lookup_result  = Compound.query.filter_by(**kwargs ).first()
                #lookup_result  = database.Compound.query.filter_by(id_of_record = entity).first()
            return lookup_result
        except Exception as derp:
            print(derp)
            redprint("[-] Not in local database")
            # None if empty
            return None


    def add_to_db(self, thingie):
        """
        Takes SQLAchemy model Objects 
        For updating changes to Class_model.Attribute using the form:

            Class_model.Attribute = some_var 
            add_to_db(some_var)

        """
        try:
            database.session.add(thingie)
            database.session.commit
            redprint("=========Database Commit=======")
            greenprint(thingie)
            redprint("=========Database Commit=======")
        except Exception as derp:
            print(derp)
            print(makered("[-] add_to_db() FAILED"))
    ################################################################################

    def update_db(self):
        """
        DUH
        """
        try:
            database.session.commit()
        except Exception as derp:
            print(derp.with_traceback)
            print(makered("[-] Update_db FAILED"))

    ###############################################################################

    def dump_db(self):
        """
    Prints database to screen
        """
        print(makered("-------------DUMPING DATABASE------------"))
        records1 = database.session.query(Compound).all()
        for each in records1:
            print (each)
        print(makered("------------END DATABASE DUMP------------"))

    ###############################################################################

    def dump_compounds(self):
        """
    Prints database to screen
        """
        print(makered("-------------DUMPING COMPOUNDS------------"))
        records = database.session.query(Compounds).all()
        for each in records:
            print (each)
        print(makered("-------------END DATABASE DUMP------------"))
    ###############################################################################

    def compound_to_database(self, lookup_list: list):
        """
        Puts a pubchem lookup to the database
        ["CID", "cas" , "smiles" , "Formula", "Name", "Description", "image", WAY MORE]
        """
        self.add_to_db(Compound(cid = lookup_list[0].get('cid')                                                   ,\
                                     #lookup_cas                 = lookup_list[0].get('cas')                      ,\
                                     smiles                      = lookup_list[0].get('smiles')                   ,\
                                     formula                     = lookup_list[0].get('formula')                  ,\
                                     molweight                   = lookup_list[0].get('molweight')                ,\
                                     charge                      = lookup_list[0].get('charge')                   ,\
                                     iupac_name                  = lookup_list[0].get('iupac_name')               ,\
                                     description                 = lookup_list[0].get('description')              ,\
                                     bond_stereo_count           = lookup_list[0].get('bond_stereo_count')        ,\
                                     bonds                       = lookup_list[0].get('bonds')                    ,\
                                     rotatable_bond_count        = lookup_list[0].get('rotatable_bond_count')     ,\
                                     multipoles_3d               = lookup_list[0].get('multipoles_3d')            ,\
                                     mmff94_energy_3d            = lookup_list[0].get('multipoles_3d')            ,\
                                     mmff94_partial_charges_3d   = lookup_list[0].get('mmff94_partial_charges_3d'),\
                                     atom_stereo_count           = lookup_list[0].get('atom_stereo_count')        ,\
                                     h_bond_acceptor_count       = lookup_list[0].get('h_bond_acceptor_count')    ,\
                                     feature_selfoverlap_3d      = lookup_list[0].get('feature_selfoverlap_3d')   ,\
                                     cactvs_fingerprint          = lookup_list[0].get('cactvs_fingerprint')       ,\
                                     image                       = lookup_list[0].get('image')                    ))



greenprint("[+] Loaded database")
