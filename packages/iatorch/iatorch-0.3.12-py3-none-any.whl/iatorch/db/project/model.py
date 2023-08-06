from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Sequence, Integer, String, DateTime, ForeignKey

Base = declarative_base()

################################################################
# User - users
################################################################
# 추후 User Model 정의하여 사용할 것
# id
# name
# email
# password
# avatar
# organization 


################################################################
# History - history
################################################################
class History(Base):
    '''
    Table 'history'
    
    Fields
    ------
    id: Sequence, primary_key
    name: <string>
      dataset lot name = directory name in ./origin
    description: <string>
    added: <string>
    n_origin: <string>
    n_valid: <string>
    n_revised: <string>
    '''
    __tablename__ = 'history'
    
    id = Column(Integer, Sequence('history_id_sequence'), primary_key=True)
    name = Column(String, nullable=False)
    provider = Column(String)
    description = Column(String)
    added = Column(DateTime)
    n_origin = Column(Integer)
    n_valid = Column(Integer)
    n_revised = Column(Integer)
    
    # relationship
    dataset = relationship('Inventory', backref="lot")
    
    def __repr__(self):
        return f"<History(id={self.id}, name={self.name}, description={self.description}, added={self.added}, n_origin={self.n_origin}, n_valid={self.n_valid}, n_revised={self.n_revised})>"

    
################################################################
# Inventory - inventory
################################################################
class Inventory(Base):
    '''
    Table 'inventory'
    
    Fields
    ------
    id: Sequence, primary_key
    filepath: <string>, nullable_false
    filename: <string>
    lot: <string>
    split: <string>
    status: <Integer>
      0: invalid, 1: valid, 2: modified (valid)
    '''
    __tablename__ = 'inventory'
    
    id = Column(Integer, Sequence('inventory_id_sequence'), primary_key=True)
    originpath = Column(String, nullable=False)
    filepath = Column(String)
    filename = Column(String)
    lot_id = Column(Integer, ForeignKey('history.id'))
    split = Column(String)
    label = Column(String)
    label_ = Column(String)
    status = Column(Integer)
    
    # relationship
    revisions = relationship('Revision', backref="data")
    
    def __repr__(self):
        return f"<Inventory(filepath={self.filepath}, filename={self.filename}, lot={self.lot}, split={self.split}, status={self.status})>"

    
################################################################
# Revision - revisions !!!
################################################################
class Revision(Base):
    '''
    Table 'revisions'
    
    Fields
    ------
    id: Sequence, primary_key
    filepath: <string>, foreign_key
    confirmer: <string>
    revised: <datetime>
    prev_status: <string>
    prev_label: <string>
    prev_split: <string>
    detail: <string>    
    '''
    __tablename__ = 'revisions'
    
    id = Column(Integer, Sequence('revisions_id_sequence'), primary_key=True)
    filepath = Column(String, ForeignKey('inventory.filepath'))
    confirmer = Column(String)
    revised = Column(DateTime)
    job = Column(String)
    prev_status = Column(Integer)
    prev_label = Column(String)
    prev_split = Column(String)
    detail = Column(String)
    
    def __repr__(self):
        return f"<Revision(id={self.id}, filepath={self.filepath}, confirmer={self.confirmer}, revised={self.revised}, job={self.job})>"
