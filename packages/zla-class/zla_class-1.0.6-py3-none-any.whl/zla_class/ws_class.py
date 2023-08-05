import zla_material_class.zla_class.ws_tools.ws_data_sql as wssql
import zla_material_class.zla_class.common_tools.master_sql as mastersql
from .common_tools import general_func as gfunc
import pandas as pd
from zla_general import \
    vendor_finding_bymat as vmat, \
    header_ecnbysap as header, \
    get_newdeldate_bydf as newdel, \
    movingcost_bymat as mov


class get_ws(object):
    def __init__(self, partno, start=None, end=None, customer=None, parent=False):
        """
        For getting SKC whole sale data as your requirment
        :param partno: part number is needed.
        :param start: start date (option)
        :param end: end date (option)
        :param customer: customer code by sap only (option)
        :param parent: if True data will be get all of branch data together (default is False)
        """
        # Make character sentense
        self.partno = partno
        self.allcustomer = mastersql.customer_parentable(customer, parent)
        self.dictchain = header._parent_ecnchainbymat(partno)
        self.master = mastersql.get_partsmaster(partno)
        self.character = mastersql.get_partscharacter(partno)
        self.purchasing = mastersql.get_partspurchasing(partno)
        self.movingcost = mov.get_movingcost(partno)
        self.vendor, self.cost, self.mapping = vmat.get_vendor_mat(partno, self.purchasing.get('spt'))

        # Make sql_sentense
        sql_nontapa = "orders.itemcat <> 'TAPA'"
        lst_partno = list(self.dictchain.keys())
        select_partno = lst_partno[lst_partno.index(partno):]
        sql_partno = wssql.get_sql_1(select_partno)
        sql_customer = wssql.get_sql_2(self.allcustomer)
        sql_timerange = wssql.get_sql_3([start, end])
        list_sql = [sql_nontapa, sql_partno, sql_customer, sql_timerange]
        where_sql = gfunc.merge_wherecondition(list_sql)
        msql = wssql.finishing_sql(where_sql)
        _original = gfunc.get_data(msql)
        _original['deldate'] = _original['del1stdate']
        _original['partno_header'] = partno
        self.raw_data = _original.copy()
        self.new_deldata = newdel.generate_deldate(_original).copy()
        self.original_data = History(_original)
        self.newdel_data = History(newdel.generate_deldate(_original))



class History(pd.DataFrame):
    def __init__(self,_data):
        super(History, self).__init__()
        self.raw = _data

    def history(self,_filter ='all',_by='days'):
        """
        generate SKC whole sale data as your requirement
        :param _filter:
        - 'all' (default) is overall volume
        - 'dom_all' is domestic all'
        - 'dom_ndist' is domestic for non distributor,
        - 'dom_dist' is domestic for distributor only,
        - 'exp_all' is export all
        - 'exp_nkbt' is export for SKC territory only
        - 'exp_kbt' is export for non territory}
        :param _by:
        - 'days'(default) is shown for dialy data
        - 'weeks' is shown for weekly data
        - 'months' is shown for monthly data
        - 'years' is shown for annual data}
        :return:
        Dataframe with date index
        """
        _his = self.raw.copy()
        if _filter == 'all':
            _ans = gfunc.to_number(_his,_by,_datecol='deldate')
        elif _filter == 'dom_all':
            filter_1 = (self.raw['sorg'] == 'DY10')
            _ans = gfunc.to_number(_his[filter_1],_by,_datecol='deldate')
        elif _filter == 'dom_ndist':
            filter_1 = (self.raw['sorg'] == 'DY10')
            filter_2 = (self.raw['distch'] != '20')
            _ans = gfunc.to_number(_his[filter_1 & filter_2], _by,_datecol='deldate')
        elif _filter == 'dom_dist':
            filter_1 = (self.raw['sorg'] == 'DY10')
            filter_2 = (self.raw['distch'] == '20')
            _ans = gfunc.to_number(_his[filter_1 & filter_2], _by,_datecol='deldate')
        elif _filter == 'exp_all':
            filter_1 = (self.raw['sorg'] == 'DY20')
            _ans = gfunc.to_number(_his[filter_1], _by,_datecol='deldate')
        elif _filter == 'exp_nkbt':
            filter_1 = (self.raw['sorg'] == 'DY20')
            filter_2 = (self.raw['distch'] != '30')
            _ans = gfunc.to_number(_his[filter_1 & filter_2], _by,_datecol='deldate')
        elif _filter == 'exp_kbt':
            filter_1 = (self.raw['sorg'] == 'DY20')
            filter_2 = (self.raw['distch'] == '30')
            _ans = gfunc.to_number(_his[filter_1 & filter_2], _by,_datecol='deldate')
        else:
            raise Exception("Sorry, your filter was wrong (allow only : ['all','dom_all','dom_ndist','dom_dist','exp_all','exp_nkbt','exp_kbt'])")
        return _ans