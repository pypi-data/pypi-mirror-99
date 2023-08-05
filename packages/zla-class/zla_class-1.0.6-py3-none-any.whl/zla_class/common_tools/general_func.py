from datetime import datetime
import pandas as pd
from zla_utilities import \
    db_connector as dbcon, utility as ut

def merge_wherecondition(sql_sentense):
    _where = [' (' + _sen + ') ' for _sen in sql_sentense if _sen is not None]
    return "and".join(_where)

def get_data(msql):
    db = 'partsdatabase'
    df = dbcon.opendata(msql, db)
    return df

def convertor_bothdate(dlist):
    _start = datetime.strptime(dlist[0], '%Y-%m-%d')
    _end = datetime.strptime(dlist[1], '%Y-%m-%d')
    if _start > _end:
        print('Not allow start_date less than end_date !!')
        _sub = 'between "x" and "y"'
    else:
        _sub = 'between "{}" and "{}"'.format(dlist[0], dlist[1])

    return _sub

def convertor_singledate(dlist):
    if dlist[0] is not None:
        _sub = '>= "{}"'.format(dlist[0])
    else:
        _sub = 'between DATE_SUB("{}", INTERVAL 48 MONTH) and "{}"'.format(dlist[1], dlist[1])
    return _sub


def to_number(df, _by,_datecol):
    _data = df[[_datecol, 'qty']].groupby(_datecol).sum()
    if not _data.empty:
        _data.index = pd.to_datetime(_data.index, format='%Y-%m-%d')
    _data = ut.full_daterange(_data, by=_by)
    return _data