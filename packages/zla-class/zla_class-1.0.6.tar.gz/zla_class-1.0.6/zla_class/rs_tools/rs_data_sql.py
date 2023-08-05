from datetime import datetime
from zla_material_class.zla_class.common_tools import general_func as gfunc
from zla_utilities import \
    utility as ut

def get_sql_1(partnolist):
    sql_1 = 'rsdet.partno in {}'
    sql_2 = 'servdet.partno in {}'
    sel_rs = sql_1.format(ut.sel_insql(partnolist))
    sel_serv = sql_2.format(ut.sel_insql(partnolist))
    return sel_rs,sel_serv


def get_sql_2(customerlist):
    sql_1 = """rs.customerid in (select idcustomerlistkad from customerlistkad where idcustomersap in {})"""
    sql_2 = """serv.customerid in (select idcustomerlistkad from customerlistkad where idcustomersap in {})"""
    if customerlist is not None:
        rscus_data = sql_1.format(ut.sel_insql(customerlist))
        servcus_data = sql_2.format(ut.sel_insql(customerlist))
    else:
        rscus_data = None
        servcus_data = None
    return rscus_data,servcus_data


def get_sql_3(mlist):
    sql_base1 = 'rs.rsdate '
    sql_base2 = 'serv.docdate '
    if all(x is None for x in mlist):
        _rssql = sql_base1 + '>= DATE_SUB(now(), INTERVAL 48 MONTH)'
        _servsql = sql_base2 + '>= DATE_SUB(now(), INTERVAL 48 MONTH)'
    elif all(type(x) is str for x in mlist):
        _subsql = gfunc.convertor_bothdate(mlist)
        _rssql = sql_base1 + _subsql
        _servsql = sql_base2 + _subsql
    else:
        _subsql = gfunc.convertor_singledate(mlist)
        _rssql = sql_base1 + _subsql
        _servsql = sql_base2 + _subsql
    return _rssql,_servsql



def finishing_sql(_rswhere,_servwhere):
    _sqlrs = """select rs.rsdate as date,kad.idcustomersap as customerid, sum(rsdet.qty) as qty,rs.typeoforder
            from rsorder as rs inner join rsorderdetails as rsdet on rs.idrsorder = rsdet.idrsorder
            inner join customerlistkad as kad on kad.idcustomerlistkad = rs.customerid
            where"""
    _sqlserv = """select serv.docdate as date,kad.idcustomersap as customerid, sum(servdet.qty) as qty
                from servicedata as serv inner join servicedetails as servdet on serv.idservicedata = servdet.idservicedata
                inner join customerlistkad as kad on kad.idcustomerlistkad = serv.customerid
                where"""
    _groupbyrs = " group by rs.rsdate,kad.idcustomersap,rs.typeoforder"
    _groupbyserv = " group by serv.docdate,kad.idcustomersap"
    rs_msql = _sqlrs + _rswhere + _groupbyrs
    sev_msql = _sqlserv + _servwhere + _groupbyserv
    return rs_msql,sev_msql