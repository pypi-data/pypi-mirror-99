from datetime import datetime
from zla_utilities import \
    utility as ut, \
    db_connector as dbcon

def get_multiplesql(itemlist,customerlist):
    if (customerlist is None) & (itemlist is not None):
        sql_1 = 'orders.partno in {}'
        sel_ws = sql_1.format(ut.sel_insql(itemlist))
    elif (customerlist is not None) & (itemlist is not None):
        tup_mat = tuple([(i, j) for i in itemlist for j in customerlist])
        sql_1 = '(orders.partno,ws.shipto) in {}'
        sel_ws = sql_1.format(ut.sel_insql(tup_mat))
    elif (customerlist is not None) & (itemlist is None):
        sql_1 = 'ws.shipto in {}'
        sel_ws = sql_1.format(ut.sel_insql(itemlist))
    else:
        sel_ws = None
    return sel_ws

def finishing_multisql(_where):
    _sql = """select orders.partno, ws.customerid, ws.shipto ,ws.sotype,ws.sorg,ws.distch, ws.orderdate, 
            orders.del1stdate,(cast(orders.qty as signed) -ifnull(cast(canc.qty as signed), 0)) as qty
            from partssaleorder as ws inner join orderdetails as orders on ws.saleorder = orders.saleorder
            left join orders_cancellation as canc on (orders.saleorder,orders.orderitem) = (canc.saleorder,canc.orderitem)
            where"""
    msql = _sql + _where
    return msql
