from datetime import datetime
from zla_utilities import \
    utility as ut, \
    db_connector as dbcon

def get_multiplesql(itemlist,customerlist):
    if customerlist is not None:
        cust_kad = convertcustomersap_kad(customerlist)
        tup_mat = tuple([(i, j) for i in itemlist for j in cust_kad])
        sql_1 = '(rsdet.partno,rs.customerid) in {}'
        sql_2 = '(servdet.partno,serv.customerid) in {}'
        sel_rs = sql_1.format(ut.sel_insql(tup_mat))
        sel_serv = sql_2.format(ut.sel_insql(tup_mat))
    else:
        sql_1 = 'rsdet.partno in {}'
        sql_2 = 'servdet.partno in {}'
        sel_rs = sql_1.format(ut.sel_insql(itemlist))
        sel_serv = sql_2.format(ut.sel_insql(itemlist))
    return sel_rs,sel_serv

def convertcustomersap_kad(customerlist):
    db = 'partsdatabase'
    msql = 'select idcustomerlistkad from customerlistkad where idcustomersap in {}'.format(ut.sel_insql(customerlist))
    listkad = dbcon.opendata(msql,db)['idcustomerlistkad'].unique()
    return listkad

def finishing_multisql(_rswhere,_servwhere):
    _sqlrs = """select rs.rsdate as date,kad.idcustomersap as customerid,rsdet.partno, sum(rsdet.qty) as qty,rs.typeoforder
            from rsorder as rs inner join rsorderdetails as rsdet on rs.idrsorder = rsdet.idrsorder
            inner join customerlistkad as kad on kad.idcustomerlistkad = rs.customerid
            where"""
    _sqlserv = """select serv.docdate as date,kad.idcustomersap as customerid,servdet.partno, sum(servdet.qty) as qty
                from servicedata as serv inner join servicedetails as servdet on serv.idservicedata = servdet.idservicedata
                inner join customerlistkad as kad on kad.idcustomerlistkad = serv.customerid
                where"""
    _groupbyrs = " group by rs.rsdate,kad.idcustomersap,rsdet.partno,rs.typeoforder"
    _groupbyserv = " group by serv.docdate,kad.idcustomersap,servdet.partno"
    rs_msql = _sqlrs + _rswhere + _groupbyrs
    sev_msql = _sqlserv + _servwhere + _groupbyserv
    return rs_msql,sev_msql
