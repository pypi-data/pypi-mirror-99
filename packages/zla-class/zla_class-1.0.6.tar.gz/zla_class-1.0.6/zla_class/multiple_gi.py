from zla_material_class.zla_class.rs_tools.rs_method import *
from .common_tools import general_func as gfunc
from .gi_tools import gi_data_sql as gisql,\
    multiple_gi_sql as multigisql
import zla_material_class.zla_class.ws_tools.multiple_ws_sql as multiwssql
from zla_utilities import utility as ut
from zla_general import header_ecnbysap as header
import pandas as pd
from zla_general import \
    get_newdeldate_bydf as newdel


class get_multiple_gi(object):
    def __init__(self, list_partno=None, start=None, end=None, list_customer=None, parent=False):
        """
        For getting SKC whole sale data as your requirment by multiple material
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
        selecteditem = selected_partno(_dictlist)
        sql_sentence = multigisql.get_multiplesql(selecteditem, self.allcustomer)
        sql_timerange = gisql.get_sql_3([start, end])
        list_sql = [sql_sentence, sql_timerange]
        where_sql = gfunc.merge_wherecondition(list_sql)
        msql = multigisql.finishing_multisql(where_sql)
        _original = gfunc.get_data(msql)
        _original = header._parent_ecnchainbydf(_original, 'partno')
        self.raw_data = _original.copy()
        self.gidata = History(_original)

def selected_partno(_dict):
    if _dict is not None:
        return list(ut.merge_dict_inlist(_dict).keys())
    else:
        return None

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
        return gfunc.to_number(self.raw,_by,_datecol='billdate')