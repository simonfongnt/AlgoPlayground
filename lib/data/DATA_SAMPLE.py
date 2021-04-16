from lib.moduleCore import DataBase

import sys
import os
import pandas as pd
import time


class Data(
    DataBase,
    ):

    filepath    = sys._getframe().f_code.co_filename
    filename    = filepath.split(os.sep)[-1]
    classname   = sys._getframe().f_code.co_name

    # data info
    info = [
        filename,
        'Example of Data Preprocessing.',        
    ]

    # data help ...
    helpinfo = {
        "help":[
                "MODULE INFO:",
                filename,
                "USAGE:",
                "data option [source] [operation]",
                ""
            ],
        "describe":[
                "INFO:",
                "describe features",
                "USAGE:",
                "data option [source] [operation]",
                ""
            ],
    }

    def __init__(
        self,
        ):
        DataBase.__init__(self)
        self.__initParam()

    def __initParam(self):
        self.raw       = {
            'ABC': None,
        }
        self.dataPack  = {
            'LABEL':    'TARGET',
        }

    def Command(
        self,
        cmds,
        ):
        if cmds[0] == 'describe':
            print(self.x.describe())

    def Raw(
        self,
        dir,
        ):
        # iterate csv file inside the directory
        for key in self.raw.keys():
            self.raw[key] = pd.read_csv(
                                    os.path.join(
                                        dir,
                                        key + '.csv',
                                        )
                                )

    def Create(
        self,
        ): 
        # Read loaded csv
        rawdf  = self.raw['ABC']
        rawdf = rawdf.set_index('Date')
        
        # Extra Data to other Functions (e.g. Model, Test)
        self.dataPack['RAW'] = rawdf
        df = rawdf

        # filtering
        df = df.astype(int)

        # Normalization
        df = df.subtract(   rawdf['L'], axis='index')
        df = df.divide(     rawdf['L'], axis='index')

        # Labelling
        df['L']  = rawdf['L']
        df['nL'] = rawdf['L'].shift(
                        periods=-1,
                    )
        df.loc[df['nL'] >  df['L'], 'TARGET'] = 1
        df.loc[df['nL'] <= df['L'], 'TARGET'] = 0
        df = df.drop(columns=['L', 'nL'])

        # Prepare for sharing
        df = df.dropna(how='any').reset_index(drop=True)
        # self.y  = df.pop('TARGET')
        self.y  = df[['TARGET',]]
        df.pop('TARGET')
        self.x  = df
