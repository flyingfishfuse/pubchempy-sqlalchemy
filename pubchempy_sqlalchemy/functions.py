class Database_functions():
    def __init__(self):
        self.TESTING = TESTING
    
    def compound_by_formula(formula_str : str):
        return Compound.query.filter_by(formula=formula_str).first()

    def Compound_by_id(cid_of_compound : str):
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
            redprint(derp.with_traceback))
            return False

    ################################################################################
    def internal_local_database_lookup(entity : str, id_of_record:str ):
        """
        feed it a formula or CID followed buy "formula" or "cid" or "iupac_name
        searches by record and entry
        Returns False and raises and exception/prints exception on error
        Returns an SQLAlchemy database object if record exists
        Don't forget this is for compounds only!
        """
        try:
            greenprint("[+] performing internal lookup")
            from variables_for_reality import search_validate
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


    def add_to_db(thingie):
        """
        Takes SQLAchemy Class_model Objects 
        For updating changes to Class_model.Attribute using the form:

            Class_model.Attribute = some_var 
            add_to_db(some_var)

        """
        try:
            database.session.add(thingie)
            database.session.commit
            redprint("=========Database Commit=======")
            print(thingie)
            redprint("=========Database Commit=======")
        except Exception as derp:
            print(derp)
            redprint("[-] add_to_db() FAILED")
            print(str(Exception.__cause__))
    ################################################################################

    def update_db():
        """
        DUH
        """
        try:
            database.session.commit()
        except Exception as derp:
            print(derp)
            redprint("[-] Update_db FAILED")

    ###############################################################################

    def dump_db():
        """
    Prints database to screen
        """
        redprint("-------------DUMPING DATABASE------------")
        records1 = database.session.query(Compound).all()
        records2 = database.session.query(Composition).all()
        for each in records1, records2:
            print (each)
        redprint("------------END DATABASE DUMP------------")

    ###############################################################################

    def dump_compositions():
        """
    Prints database to screen
        """
        redprint("-------------DUMPING COMPOSITIONS------------")
        records = database.session.query(Composition).all()
        for each in records:
            print (each)
        redprint("--------------END DATABASE DUMP--------------")

    ###############################################################################

    def dump_compounds():
        """
    Prints database to screen
        """
        redprint("-------------DUMPING COMPOUNDS------------")
        records = database.session.query(Compounds).all()
        for each in records:
            print (each)
        redprint("-------------END DATABASE DUMP------------")
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
###############################################################################
    def composition_to_database(comp_name: str, units_used :str, \
                                formula_list : list , info : str):
        """
        The composition is a relation between multiple Compounds
        Each Composition entry will have required a pubchem_lookup on each
        Compound in the Formula field. 
        the formula_list is a CSV STRING WHERE: 
        ...str_compound,int_amount,.. REPEATING (floats allowed)
        EXAMPLE : Al,27.7,NH4ClO4,72.3

        BIG TODO: be able to input list of cas/cid/whatever for formula_list
        """
        # query local database for records before performing pubchem
        # lookups
        # expected to return FALSE if no record found
        # if something is there, it will evaluate to true
#        for each in formula_list:
#            input = Pubchem_lookup.formula_input_validation(each)

        # extend this but dont forget to add more fields in the database model!
        Database_functions.add_to_db(Composition(\
                name       = comp_name,               \
                units      = units_used,              \
                compounds  = formula_list,            \
                notes      = info                     ))

greenprint("[+] Loaded database")
