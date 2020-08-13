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
"""
PubChemPy caching wrapper

Caching extension to the Python interface for the PubChem PUG REST service.

https://github.com/mcs07/PubChemPy

"""
import os
import re
import lxml
import base64
import requests
from PIL import Image
from io import BytesIO
import pubchempy as pubchem
from bs4 import BeautifulSoup
from requests.utils import requote_uri
#from models.Atom import Atom
from config import Compound
from config import Database_functions
from config import redprint,blueprint,greenprint,makered
from config import API_BASE_URL,search_validate,yellow_bold_print

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

###################################################################################
# The meat and potatoes
###################################################################################
class pubchemREST_Description_Request():
    # hey it rhymes
    '''
    This class is to be used only with validated information
    Returns the description field using the XML return from the REST service
    Does Compounds ONLY!, Needs a second class or modifications to this one 
    To return a Substance type

    results are stored in :
        pubchemREST_Description_Request.parsed_results

    the url of the API call is stored in :
        pubchemREST_Description_Request.request_url
    '''
    def __init__(self, record_to_request: str ,input_type = 'iupac_name' ):
        if search_validate(input_type) :#in pubchem_search_types:
            if TESTING           == True:
                greenprint("searching for a Description : " + record_to_request)
            if input_type        == "iupac_name":
                self.thing_type  = "name"
            else :
                self.thing_type  = input_type
        self.record_to_request   = record_to_request
        self.request_url         = requote_uri("{}/compound/{}/{}/description/XML".format(\
                                    API_BASE_URL,self.thing_type,self.record_to_request))
        blueprint("[+] Requesting: " + makered(self.request_url) + "\n")
        self.request_return      = requests.get(self.request_url)
        self.soupyresults        = BeautifulSoup(self.request_return.text , features='lxml').contents[1]
        self.parsed_result       = self.soupyresults.find_all(lambda tag:  tag.name =='description')
        if self.parsed_result    != [] :
            self.parsed_result   = str(self.parsed_result[0].contents[0])
            greenprint("[+] Description Found!")
            print(self.parsed_result)
        elif self.parsed_result  == [] or NoneType:
            blueprint("[-] No Description Available in XML REST response")
            self.parsed_result   = "No Description Available in XML REST response"
            
###################################################################################

class Image_lookup():
    '''
Performs a pubchem lookup

INPUT:
    input_type :str
        - Default : name ( can be fed "iupac_name" from the rest of the app)

OUTPUT:
    self.rest_request
        - Response from remote server
    self.image_storage
        - Base64 Encoded string of the raw response 

    '''
    def __init__(self, record_to_request: str , input_type = "name"):
        #############################
        if search_validate(input_type) :#in pubchem_search_types:
            greenprint("searching for an image : " + record_to_request)
            # fixes local code/context to work with url/remote context
            if input_type  == "iupac_name":
                self.input_type = "name"
            else :
                self.input_type = input_type
            self.request_url        = requote_uri("{}/compound/{}/{}/PNG".format(\
                                            API_BASE_URL,self.input_type,record_to_request))
            blueprint("[+] Requesting: " + makered(self.request_url))
            self.rest_request = requests.get(self.request_url)
            if self.was_there_was_an_error() == False:
                self.image_storage = self.encode_image_to_base64(self.image_storage)
            else:
                redprint("[-] Error with Class Variable self.encode_image_to_base64")
        else:
            redprint("[-] Input type was wrong for Image Search")
            return None
     
    def encode_image_to_base64(self, image, image_format = "png"):
        greenprint("[+] Encoding Image as Base64")
        buff = BytesIO()
        image.save(buff, format=image_format)
        img_str = base64.b64encode(buff.getvalue())
        return img_str

    def decode_image_from_base64(self, data):
        buff = BytesIO(base64.b64decode(data))
        return Image.open(buff)
    
#    def save_image(self, PIL_image, name, image_format):
#        greenprint("[+] Saving image as {}".format(name))
#        PIL_image.save(self.filename, format=image_format)

    def decode_and_save(self, base64_image, name, image_format):
        '''
    Can be used to save images from the db to a file
    not part of normal function but useful for the end user
        '''
        greenprint("[+] Decoding and Saving image as {}".format(name))
        decoded_image = self.decode_image_from_base64(base64_image) 
        decoded_image.save(name, format=image_format)
        decoded_image.close()

    def was_there_was_an_error(self):
        # server side error
        set1,set2,set3 = [404,504,503,500] , [400,405,501] , [500]
        if self.rest_request.status_code in set1 :
            blueprint("[-] Server side error - No Image Available in REST response")
            yellow_bold_print("Error Code {}".format(self.rest_request.status_code))
            return True # "[-] Server side error - No Image Available in REST response"
        if self.rest_request.status_code in set2:
            redprint("[-] User error in Image Request")
            yellow_bold_print("Error Code {}".format(self.rest_request.status_code))
            return True # "[-] User error in Image Request"
        if self.rest_request.status_code in set3:
            #unknown error
            blueprint("[-] Unknown Server Error - No Image Available in REST response")
            yellow_bold_print("Error Code {}".format(self.rest_request.status_code))
            return True # "[-] Unknown Server Error - No Image Available in REST response"
        # no error!
        if self.rest_request.status_code == 200:
            return False
###############################################################################
class Pubchem_lookup():
    '''
Class to perform lookups on CID's and IUPAC names

Provide a search term and "term type", term types are "cas" , "iupac_name" , "cid"

    Example 1 : .pubchem_lookup methanol iupac_name
    Example 2 : .pubchem_lookup 3520 cid
    Example 3 : .pubchem_lookup 113-00-8 cas

OUTPUTS:
    self.lookup_object
        - The SQLAlchemy object
        - Attemps local SQLAlchemy object first, then performs a remote lookup
    self.local_output_container
        - The Human Readable Representation of the Data
    self.image
        -   Base64 binary string

NOTE: to grab a description or image requires a seperate REST request.
    I need to add a switch to control this
    '''
    def __init__(self, user_input, type_of_input):
        self.internal_lookup_bool   = bool
        self.user_input             = user_input
        self.type_of_input          = type_of_input
        self.grab_description       = True
        self.grab_image             = True
        self.image                  = str
        if TESTING == True:
            self.local_output_container = {} # {"test" : "sample text"} # uncomment to supress linter errors
                                                                        # in the IDE
        else: 
            self.local_output_container = {}
        #do the thing 
        self.validate_user_input(self.user_input , self.type_of_input)
        #say the thing
        self.local_output_container = { 'lookup'      : self.lookup_object       ,\
                                        'description' : self.lookup_description  ,\
                                        'image'       : self.image                }

    def do_lookup(self, user_input, type_of_input):
        '''
        after validation, the user input is used in 
        Pubchem_lookup.pubchem_lookup_by_name_or_CID() 
        pubchemREST_Description_Request(user_input, type_of_input)
        Image_lookup()
        '''
        try:
            internal_lookup = Database_functions.internal_local_database_lookup(user_input, type_of_input)
            # if internal lookup is false, we do a remote lookup and then store the result
            if internal_lookup == None or False:
                redprint("[-] Internal Lookup returned false")
                self.internal_lookup_bool = False
                # we grab things in the proper order
                # description first
                try:
                    description_lookup      = pubchemREST_Description_Request(user_input, type_of_input)
                except Exception as derp:
                    redprint("[-] Description Lookup Failed")
                    print(derp)
                    self.lookup_description = "Description Lookup Failed"
                #then image
                try:
                    image_lookup = Image_lookup(user_input, input_type = type_of_input)
                except Exception as derp:
                    redprint("[-] Image Lookup Failed")
                    print(derp)
                    image_lookup = None
                    self.image   = "No Image Available"
                if (image_lookup!= None):
                    self.image = str(image_lookup.image_storage)
                else:
                    redprint("[-] Something wierd happened in do_lookup")
                # Now pubchem
                self.lookup_description     = description_lookup.parsed_result
                self.lookup_object          = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
            # we return the internal lookup if the entry is already in the DB
            # for some reason, asking if it's true doesn't work here so we use a NOT instead of an Equals.
            elif internal_lookup != None or False:
                greenprint("[+] Internal Lookup returned TRUE")
                self.internal_lookup_bool = True
                self.lookup_description   = internal_lookup.description
                self.lookup_object        = internal_lookup
                self.image                = internal_lookup.image
                #redprint("==BEGINNING==return query for DB lookup===========")
                #greenprint(str(internal_lookup))
                #redprint("=====END=====return query for DB lookup===========")
        # its in dire need of proper exception handling              
        except Exception as derp:
            redprint('[-] Something happened in the try/except block for the function do_lookup')
            print(derp.with_traceback)

    def validate_user_input(self, user_input: str, type_of_input:str):
        """
User Input is expected to be the proper identifier.
   - type of input is one of the following: 
        cid , iupac_name , cas

Ater validation, the user input is used in :
    - Pubchem_lookup.do_lookup()
    - Pubchem_lookup.pubchem_lookup_by_name_or_CID()
        
        """
        import re
        cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')
        try:
            if search_validate(type_of_input) :#in pubchem_search_types:
                greenprint("user supplied a : " + type_of_input)
                try:
                    if type_of_input == "cas":
                        greenprint("[+} trying to match regular expression for CAS")
                        if re.match(cas_regex,user_input):
                            greenprint("[+] Good CAS Number")
                            self.do_lookup(user_input, type_of_input)
                        else:
                            redprint("[-] Bad CAS Number")
                    elif type_of_input == "cid" or "iupac_name":
                        self.do_lookup(user_input, type_of_input)
                    else:
                        redprint("[-] Something really wierd happened inside the validation flow")
                except Exception as derp:
                    redprint("[-] reached the exception in validate_user_input")
                    print(derp.with_traceback)
            else:
                redprint("Bad User Input")
        except Exception as derp:
            redprint("search_validate_failed")
            print(derp.with_traceback)
        
    def pubchem_lookup_by_name_or_CID(self , compound_id, type_of_data:str):
        '''
        Provide a search term and record type
        requests can be CAS,CID,IUPAC NAME/SYNONYM

        Stores lookup in database if lookup is valid
        '''
        return_relationships = []
        # you get multiple records returned from a pubchem search VERY often
        # so you have to choose the best one to store, This needs to be 
        # presented as an option to the user,and not programmatically 
        # return_index is the result to return
        return_index = 0
        data = ["iupac_name","cid","cas"]
        if type_of_data in data:
        # different methods are used depending on the type of input
        # one way
            if type_of_data == ("iupac_name" or "cas"):                     
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.get_compounds(compound_id,'name')
                except Exception as derp:# pubchem.PubChemPyError:
                    print(derp.with_traceback)
                    redprint("[-] Error in pubchem_lookup_by_name_or_CID : NAME exception")
        # CID requires another way
            elif type_of_data == "cid":
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.Compound.from_cid(compound_id)
                except Exception as derp:# pubchem.PubChemPyError:
                    print(derp.with_traceback)
                    redprint("lookup by NAME/CAS exception - name")
        # once we have the lookup results, do something
            if isinstance(lookup_results, list):# and len(lookup_results) > 1 :
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    query_appendix = [{'cid' : each.cid                                 ,\
                            #'cas'                     : each.cas                       ,\
                            'smiles'                   : each.isomeric_smiles           ,\
                            'formula'                  : each.molecular_formula         ,\
                            'molweight'                : each.molecular_weight          ,\
                            'charge'                   : each.charge                    ,\
                            'bond_stereo_count'        : each.bond_stereo_count         ,\
                            'bonds'                    : each.bonds                     ,\
                            'rotatable_bond_count'     : each.rotatable_bond_count      ,\
                            'multipoles_3d'            : each.multipoles_3d             ,\
                            'mmff94_energy_3d'         : each.mmff94_energy_3d          ,\
                            'mmff94_partial_charges_3d': each.mmff94_partial_charges_3d ,\
                            'atom_stereo_count'        : each.atom_stereo_count         ,\
                            'h_bond_acceptor_count'    : each.h_bond_acceptor_count     ,\
                            'feature_selfoverlap_3d'   : each.feature_selfoverlap_3d    ,\
                            'cactvs_fingerprint'       : each.cactvs_fingerprint        ,\
                            'iupac_name'               : each.iupac_name                ,\
                            'description'              : self.lookup_description        ,\
                            'image'                    : self.image                     }]
                    return_relationships.append(query_appendix)
                    # Right here we need to find a way to store multiple records
                    # and determine the best record to store as the main entry
                    #compound_to_database() TAKES A LIST!!! First element of first element
                    #[ [this thing here] , [not this one] ]
                    #print(return_relationships[return_index])
                    Database_functions.compound_to_database(return_relationships[return_index])
            
            # if there was only one result or the user supplied a CID for a single chemical
            elif isinstance(lookup_results, pubchem.Compound) :#\
              #or (len(lookup_results) == 1 and isinstance(lookup_results, list)) :
                greenprint("[+] One Result Returned!")
                query_appendix = [{'cid'               : lookup_results.cid                 ,\
                            #'cas'                     : lookup_results.cas                 ,\
                            'smiles'                   : lookup_results.isomeric_smiles     ,\
                            'formula'                  : lookup_results.molecular_formula   ,\
                            'molweight'                : lookup_results.molecular_weight    ,\
                            'charge'                   : lookup_results.charge              ,\
                            'bond_stereo_count'        : each.bond_stereo_count             ,\
                            'bonds'                    : each.bonds                         ,\
                            'rotatable_bond_count'     : each.rotatable_bond_count          ,\
                            'multipoles_3d'            : each.multipoles_3d                 ,\
                            'mmff94_energy_3d'         : each.mmff94_energy_3d              ,\
                            'mmff94_partial_charges_3d': each.mmff94_partial_charges_3d     ,\
                            'atom_stereo_count'        : each.atom_stereo_count             ,\
                            'h_bond_acceptor_count'    : each.h_bond_acceptor_count         ,\
                            'feature_selfoverlap_3d'   : each.feature_selfoverlap_3d        ,\
                            'cactvs_fingerprint'       : each.cactvs_fingerprint            ,\
                            'iupac_name'               : each.iupac_name                    ,\
                            'description'              : self.lookup_description            ,\
                            'iupac_name'               : lookup_results.iupac_name          ,\
                            'description'              : self.lookup_description            ,\
                            'image'                    : self.image                         }]
                return_relationships.append(query_appendix)
                #print(query_appendix)
                Database_functions.compound_to_database(return_relationships[return_index])
            else:
                redprint("PUBCHEM LOOKUP BY CID : ELSE AT THE END")
    #after storing the lookup to the local database, retrive the local entry
    #This returns an SQLALchemy object
        return_query = return_relationships[return_index]
        query_cid    = return_query[0].get('cid')
        local_query  = Compound.query.filter_by(cid = query_cid).first()
        return local_query
    # OR return the remote lookup entry, either way, the information was stored
    # and you get a common "api" to draw data from.


###############################################################################
# TODO: Testing procedure requires bad data, craft a list of shitty things a 
# user can attempt. Be malicious and stupid with it
# break shit
greenprint("[+] Loaded Pubchem Lookup")

try:
    if __name__ == '__main__':
        if TESTING == True:
            import time
            #craft a list of queries to test with
            test_query_list = [["420","cid"],\
                ["methanol","iupac_name"],\
                ["phenol","iupac_name"],\
                ["methylene chloride","iupac_name"] ,\
                ["6623","cid"],\
                ["5462309","cid"],\
                ["24823","cid"],\
                ["water","iupac_name"]]
    ###################################################################
    # First we do some lookups to pull data and populate the database
    #add more tests
    ###################################################################
        for each in test_query_list:
            time.sleep(5)
            Pubchem_lookup(each[0],each[1])
    ###################################################################
    # then we test the "is it stored locally?" function
    # doesnt need a timer, not gonna ban myself from my own service
    ###################################################################
        for each in test_query_list:
            Pubchem_lookup(each[0],each[1])
except Exception as derp :
    print(derp)
    redprint("[-] Cannot run file for some reason")

