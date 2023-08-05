import pandas as pd
from zla_utilities import \
    db_connector as dbcon, utility as ut
import warnings
warnings.filterwarnings("ignore")

def merge_data(df1,df2):
    df3 = df1.set_index(['date', 'customerid']).join(df2.set_index(['date', 'customerid']), lsuffix='_frnt',rsuffix='_serv', how='outer').fillna(0)
    df3['qty'] = df3['qty_frnt'] + df3['qty_serv']
    df3 = df3[['qty']].reset_index()
    return df3
