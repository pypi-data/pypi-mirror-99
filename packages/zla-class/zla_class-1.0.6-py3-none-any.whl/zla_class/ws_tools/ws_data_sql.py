from datetime import datetime
from zla_material_class.zla_class.common_tools import general_func as gfunc
from zla_utilities import \
    utility as ut

def get_sql_1(partnolist):
    sql_1 = 'orders.partno in {}'
    sel_data = sql_1.format(ut.sel_insql(partnolist))
    return sel_data


def get_sql_2(customerlist):
    sql_1 = 'ws.customerid in {}'
    if customerlist is not None:
        cus_data = sql_1.format(ut.sel_insql(customerlist))
    else:
        cus_data = None
    return cus_data


def get_sql_3(mlist):
    sql_base = 'orders.del1stdate '
    if all(x is None for x in mlist):
        _sql = sql_base + '>= DATE_SUB(now(), INTERVAL 48 MONTH)'
    elif all(type(x) is str for x in mlist):
        _subsql = gfunc.convertor_bothdate(mlist)
        _sql = sql_base + _subsql
    else:
        _subsql = gfunc.convertor_singledate(mlist)
        _sql = sql_base + _subsql
    return _sql



def finishing_sql(_where):
    _sql = """select orders.partno, ws.customerid, ws.shipto ,ws.sotype,ws.sorg,ws.distch, ws.orderdate, 
            orders.del1stdate,sum((cast(orders.qty as signed) -ifnull(cast(canc.qty as signed), 0))) as qty
            from partssaleorder as ws inner join orderdetails as orders on ws.saleorder = orders.saleorder
            left join orders_cancellation as canc on (orders.saleorder,orders.orderitem) = (canc.saleorder,canc.orderitem)
            where"""
    _groupby = " group by orders.partno, ws.customerid, ws.shipto , ws.sotype, ws.sorg, ws.distch, ws.orderdate,orders.del1stdate"
    msql = _sql + _where + _groupby
    return msql