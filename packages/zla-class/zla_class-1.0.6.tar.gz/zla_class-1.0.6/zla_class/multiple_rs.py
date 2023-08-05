from zla_material_class.zla_class.rs_tools.rs_method import *
import zla_material_class.zla_class.rs_tools.rs_data_sql as rssql
import zla_material_class.zla_class.rs_tools.multiple_rs_sql as multirssql
from zla_material_class.zla_class.common_tools import general_func as gfunc
from zla_utilities import utility as ut
from zla_general import header_ecnbysap as header
import pandas as pd


class get_multiple_rs(object):
    def __init__(self, list_partno, start=None, end=None, list_customer=None, parent=False):
        """
        For getting SKC retail data as your requirment by multiple material
        :param partno: part number is need. (Must be input as list)
        :param start: start date (option)
        :param end: end date (option)
        :param customer: customer code by sap only (option- Must be input as list)
        :param parent: if True data will be get all of branch data together (default is False)
        """
        self.lstpartno = list_partno
        self.allcustomer = invert_tocustomerlv1(list_customer, parent)

        # Make sql_sentense
        _dictlist = header._parent_ecnchainbylist(self.lstpartno)
        select_partno = list(ut.merge_dict_inlist(_dictlist).keys())

        sql_frnt, sql_serv = multirssql.get_multiplesql(select_partno,self.allcustomer)
        sql_frnttimerange, sql_servtimerange = rssql.get_sql_3([start, end])
        list_frntsql = [sql_frnt, sql_frnttimerange]
        list_servsql = [sql_serv, sql_servtimerange]
        where_frntsql = gfunc.merge_wherecondition(list_frntsql)
        where_servsql = gfunc.merge_wherecondition(list_servsql)
        frnt_msql, serv_msql = multirssql.finishing_multisql(where_frntsql, where_servsql)
        frnt_data = gfunc.get_data(frnt_msql)
        serv_data = gfunc.get_data(serv_msql)
        frnt_data = header._parent_ecnchainbydf(frnt_data, 'partno')
        serv_data = header._parent_ecnchainbydf(serv_data, 'partno')
        self.frntraw = frnt_data.copy()
        self.servraw = serv_data.copy()
        self.rsraw = pd.concat([self.frntraw, self.servraw])
        self.frntdata = History(frnt_data)
        self.servdata= History(serv_data)
        self.rsdata= History(merge_data(self.frntdata.raw, self.servdata.raw))


def invert_tocustomerlv1(cust_item,parent):
    if parent == True:
        db = 'partsdatabase'
        msql = """select customerid,customername,parent
                from customerlistsap where parent in (select parent from customerlistsap where customerid in {})""".format(ut.sel_insql(cust_item))
        return dbcon.opendata(msql,db)['customerid'].unique()
    else:
        return cust_item

class History(pd.DataFrame):
    def __init__(self,_data):
        super(History, self).__init__()
        self.raw = _data

    def history(self,_by='days'):
        """
        generate SKC retails sale data as your requirement
        :param _by:
        - 'days'(default) is shown for dialy data
        - 'weeks' is shown for weekly data
        - 'months' is shown for monthly data
        - 'years' is shown for annual data}
        :return:
        Dataframe with date index
        """
        return gfunc.to_number(self.raw,_by,_datecol='date')

if __name__ == '__main__':
    _list = ['W9516-54172','W9516-54162']
    _x = get_multiple_rs(list_partno=_list)