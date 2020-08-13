
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
    bond_stereo_count           = database.Column()
    bonds                       = database.Column()
    rotatable_bond_count        = database.Column()
    multipoles_3d               = database.Column()
    mmff94_energy_3d            = database.Column()
    mmff94_partial_charges_3d   = database.Column()
    atom_stereo_count           = database.Column()
    h_bond_acceptor_count       = database.Column()
    feature_selfoverlap_3d      = database.Column()
    cactvs_fingerprint          = database.Column()
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

