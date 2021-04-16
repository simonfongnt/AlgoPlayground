# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:58:13 2019

@author: FB
"""
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pandas as pd
        
class database():
    # Initializer
    def __init__(
                self, 
                uri, 
                db, 
                table,
                ):
        # params
        self.uri        = uri
        self.db         = db
        self.table      = table
        print('DATABASE:', uri, db, table,)
        
    # read/write uri
    def seturi(self, uri):
        self.uri = uri
        return self.uri        
    def geturi(self):
        return self.uri
    
    # read/write database name
    def setdb(self, db):
        self.db = db
        return self.db        
    def getdb(self):
        return self.db
        
    # get tabke from database in dataframe format
    def getdfbyQuery(
            self,
            query,
            ):
        try:
            engine = sqlalchemy.create_engine(self.uri + self.db)
            conn    = engine.connect()
            df = pd.read_sql(query, conn)
            conn.close()
            engine.dispose()
            return df
        except Exception as e:
            print('database', self.db, 'getdfbyQuery', e)
            return None