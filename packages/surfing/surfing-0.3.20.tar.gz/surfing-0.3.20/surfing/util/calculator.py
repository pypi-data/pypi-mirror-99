
import dataclasses
import datetime
import pandas
import numpy as np
import math
import statsmodels.api as sm
from statsmodels import regression
from scipy.stats import gmean
from functools import partial
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from ..data.api.basic import BasicDataApi
from ..data.struct import TAAParam, TaaTunerParam, AssetWeight
from ..data.api.derived import DerivedDataApi
from ..fund.engine.asset_helper import TAAHelper, TAAStatusMode
from ..data.wrapper.mysql import *
from ..data.view.basic_models import *
from ..data.view.derived_models import *
from ..data.manager.manager_fund import DataManager
from .calculator_item import CalculatorBase

@dataclasses.dataclass
class SeriesStatUnit:

    start_date: datetime.date           # 序列的开始时间
    end_date: datetime.date             # 序列的结束时间
    trade_year: float                   # 交易年限
    last_unit_nav: float                # 末期单位净值
    annualized_ret: float               # 年化收益
    annualized_vol: float               # 年化波动率
    sharpe: float                       # 夏普率
    recent_1m_ret: float                # 最近1月收益
    recent_3m_ret: float                # 最近3月收益
    recent_6m_ret: float                # 最近6月收益
    recent_y1_ret: float                # 近一年收益
    recent_y3_ret: float                # 近三年收益
    recent_y5_ret: float                # 近五年收益
    mdd: float                          # 最大回撤
    mdd_date1: datetime.date            # 最大回撤开始时间
    mdd_date2: datetime.date            # 最大回撤结束时间
    mdd_lens: int                       # 最大回撤区间持续时间
    ret_over_mdd: float                 # Calmar 年化收益除以最大回撤
    last_mv_diff: float                 # 末期市值增量              
    last_increase_rate: float           # 末期涨幅
    worst_3m_ret: float                 # 最差三月收益
    worst_6m_ret: float                 # 最差六月收益
    recent_drawdown: float              # 最近回撤
    recent_mdd_date1: datetime.date     # 最近回撤开始时间
    downside_std :float                 # 下行风险
    var : float                         # 风险价值VaR
    cvar: float                         # 条件风险价值 CVaR


@dataclasses.dataclass
class BenchmarkSeiesStatUnit(SeriesStatUnit):

    alpha: float                # 超额收益
    beta: float                 # 风险暴露
    track_err: float            # 跟踪误差
    ir: float                   # 信息比率
    alpha_cl: float             # 择股收益
    beta_cl: float              # 择时收益
    treynor: float              # 特雷诺
    win_rate: float             # 胜率
    win_rate_0: float           # 对零胜率
    continue_value: float       # 业绩持续性

@dataclasses.dataclass
class RetStatUnit:

    recent_natural_year_ret: float      # 今年以来收益 未年化
    recent_1w_ret: float                # 最近一周收益 未年化
    recent_1m_ret: float                # 最近一月收益 未年化
    recent_3m_ret: float                # 最近三月收益 未年化
    recent_6m_ret: float                # 最近半年收益 未年化
    recent_1y_ret: float                # 最近一年收益 未年化
    recent_3y_ret: float                # 最近三年收益 未年化
    recent_5y_ret: float                # 最近五年收益 未年化
    history_ret: float                  # 成立以来收益 未年化
    history_annual_ret: float           # 成立以来收益 年化

@dataclasses.dataclass
class VolStatUnit:

    recent_natural_year_vol: float      # 今年以来风险 年化
    recent_1w_vol: float                # 最近一周风险 年化
    recent_1m_vol: float                # 最近一月风险 年化
    recent_3m_vol: float                # 最近三月风险 年化
    recent_6m_vol: float                # 最近半年风险 年化
    recent_1y_vol: float                # 最近一年风险 年化
    recent_3y_vol: float                # 最近三年风险 年化
    recent_5y_vol: float                # 最近五年风险 年化
    history_vol: float                  # 成立以来风险 年化

class Calculator:

    TRADING_DAYS_PER_YEAR = 242
    
    @staticmethod
    def get_risk_free_rate():
        return 0.025

    @staticmethod
    def get_yearly_multiplier(frequency:str='daily'):
        # daily weekly 2-weekly monthly yearly
        if frequency == 'daily':
            return 1
        if frequency == 'weekly':
            return 5
        if frequency == '2-weekly':
            return 10
        if frequency == 'monthly':
            return 20
        if frequency == 'yearly':
            return 242

    @staticmethod
    def get_datatime_date(dt):
        dt = dt if isinstance(dt, datetime.datetime) else pandas.to_datetime(dt).date()
        return dt

    @staticmethod
    def get_stat_result(dates: pandas.core.series.Series,
                        values: pandas.core.series.Series,
                        frequency: str='1D',
                        risk_free_rate: float=0.025,
                        ): #['1D','1W','2W','1M']
        res = CalculatorBase.get_stat_result(dates=dates,values=values,frequency=frequency,risk_free_rate=risk_free_rate)
        return SeriesStatUnit(
            start_date=res['start_date'],
            end_date=res['end_date'],
            trade_year=res['trade_year'],
            last_unit_nav=res['last_unit_nav'],
            annualized_ret=res['annual_ret'],
            annualized_vol=res['annual_vol'],
            sharpe=res['sharpe'],
            recent_1m_ret=res['recent_1m_ret'],
            recent_3m_ret=res['recent_3m_ret'],
            recent_6m_ret=res['recent_6m_ret'],
            recent_y1_ret=res['recent_1y_ret'],
            recent_y3_ret=res['recent_3y_ret'],
            recent_y5_ret=res['recent_5y_ret'],
            worst_3m_ret=res['worst_3m_ret'],
            worst_6m_ret=res['worst_6m_ret'],   
            mdd=res['mdd'],
            mdd_date1=res['mdd_date1'],
            mdd_date2=res['mdd_date2'],
            mdd_lens=res['mdd_lens'],
            ret_over_mdd=res['calmar'],
            last_mv_diff=res['last_mv_diff'],
            last_increase_rate=res['last_increase_rate'],
            recent_drawdown=res['recent_drawdown'],
            recent_mdd_date1 = res['recent_mdd_date1'],
            downside_std=res['downside_risk'],
            var=res['var'],
            cvar=res['cvar'],
        )

    @staticmethod
    def get_cur_mdd(dates:  pandas.core.series.Series,
                    values: pandas.core.series.Series):
        sr = pandas.Series(values, index=dates).sort_index().dropna()
        df = pandas.DataFrame(sr/sr.cummax() - 1)
        df.columns =['cur_mdd']
        return df

    @staticmethod
    def get_monthly_ret(dates:  pandas.core.series.Series,
                        values: pandas.core.series.Series,
                        ret_period: int=2021):
        df = pandas.Series(values, index=dates).sort_index().dropna()
        df = df.set_axis(pandas.to_datetime(df.index), inplace=False).resample(rule='1M').last()
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        df = pandas.DataFrame(df.pct_change(1).loc[datetime.date(ret_period,1,1):datetime.date(ret_period+1,1,1)])
        df.columns = ['monthly_ret']
        return df

    @staticmethod
    def get_benchmark_stat_result(dates: pandas.core.series.Series,
                                  values: pandas.core.series.Series,
                                  benchmark_values: pandas.core.series.Series,
                                  frequency:str='1D',
                                  risk_free_rate: float=0.025,
                                  ):#['1D','1W','2W','1M']
        res = CalculatorBase.get_stat_result(dates=dates,values=values,benchmark_values=benchmark_values,frequency=frequency,risk_free_rate=risk_free_rate)
        return BenchmarkSeiesStatUnit(
            start_date=res['start_date'],
            end_date=res['end_date'],
            trade_year=res['trade_year'],
            last_unit_nav=res['last_unit_nav'],
            annualized_ret=res['annual_ret'],
            annualized_vol=res['annual_vol'],
            sharpe=res['sharpe'],
            recent_y5_ret=res['recent_5y_ret'],
            mdd=res['mdd'],
            mdd_date1=res['mdd_date1'],
            mdd_date2=res['mdd_date2'],
            mdd_lens=res['mdd_lens'],
            ret_over_mdd=res['calmar'],
            alpha=res['alpha'],
            beta=res['beta'],
            track_err=res['track_err'],
            ir=res['info'],
            last_mv_diff=res['last_mv_diff'],
            last_increase_rate=res['last_increase_rate'],
            recent_1m_ret=res['recent_1m_ret'],
            recent_3m_ret=res['recent_3m_ret'],
            recent_6m_ret=res['recent_6m_ret'],
            recent_y1_ret=res['recent_1y_ret'],
            recent_y3_ret=res['recent_3y_ret'],
            worst_3m_ret=res['worst_3m_ret'],
            worst_6m_ret=res['worst_6m_ret'],
            recent_drawdown=res['recent_drawdown'],
            recent_mdd_date1 = res['recent_mdd_date1'],
            downside_std=res['downside_risk'],
            var=res['var'],
            cvar=res['cvar'],
            win_rate=res['win_rate'],
            win_rate_0=res['win_rate_0'],
            treynor=res['treynor'],
            alpha_cl=res['alpha_cl'],
            beta_cl=res['beta_cl'],
            continue_value=res['continue_value_m'],
        )

    @staticmethod
    def get_recent_ret(dates:             pandas.core.series.Series,
                       values:            pandas.core.series.Series,
                       frequency:         str='1D'):
        res = CalculatorBase.calc_recent_ret(dates=dates,values=values,frequency=frequency)
        return RetStatUnit(
            recent_natural_year_ret=res['recent_natural_year_ret'],
            recent_1w_ret=res['recent_1w_ret'],
            recent_1m_ret=res['recent_1m_ret'],
            recent_3m_ret=res['recent_3m_ret'],
            recent_6m_ret=res['recent_6m_ret'],
            recent_1y_ret=res['recent_1y_ret'],
            recent_3y_ret=res['recent_3y_ret'],
            recent_5y_ret=res['recent_5y_ret'],
            history_ret=res['history_ret'],
            history_annual_ret=res['history_annual_ret'],
        )

    @staticmethod
    def get_recent_vol(dates:             pandas.core.series.Series,
                       values:            pandas.core.series.Series,
                       frequency:         str='1D'):
        res = CalculatorBase.calc_recent_vol(dates=dates,values=values,frequency=frequency)
        return VolStatUnit(
            recent_natural_year_vol=res['recent_natural_year_vol'],
            recent_1w_vol=res['recent_1w_vol'],
            recent_1m_vol=res['recent_1m_vol'],
            recent_3m_vol=res['recent_3m_vol'],
            recent_6m_vol=res['recent_6m_vol'],
            recent_1y_vol=res['recent_1y_vol'],
            recent_3y_vol=res['recent_3y_vol'],
            recent_5y_vol=res['recent_5y_vol'],
            history_vol=res['history_vol'],
        )

    @staticmethod
    def get_penetraded_stock_analysis(fund_list: pandas.core.series.Series,
                                      weight_list: pandas.core.series.Series):
        # fund_list 基金代码 比如 ['000017!0', '000020!0', '000031!0', '000051!0', '000061!0'] 形式
        # weight_list 权重代码 比如 [0.1,0.2,0.2,0.2,0.3] 形式
        df = pandas.DataFrame({'fund_id':fund_list,'weight':weight_list}).set_index('fund_id')
        fund_info = DataManager.basic_data(func_name=f'get_fund_info', fund_list = fund_list.tolist())
        fund_type = 'stock'
        fund_list = df.index.tolist()
        stock_weights = DataManager.basic_data(func_name=f'get_fund_hold_{fund_type}_latest', fund_list = fund_list)
        stock_weights = stock_weights.set_index('fund_id').drop(columns=['datetime','_update_time'])
        weight_list = [i for i in stock_weights if 'weight' in i]
        stock_weights = stock_weights.replace({None:np.nan})
        for r in stock_weights.iterrows():
            fund_id = r[0]
            fund_weight = df.loc[fund_id, 'weight']
            for weight_i in weight_list:
                stock_weights.loc[fund_id, weight_i] = stock_weights.loc[fund_id, weight_i] / 100 * fund_weight
        _df = stock_weights.join(df)
        _res = []
        for r in stock_weights.iterrows():
            fund_id = r[0]
            for i in range(1,11):
                dic = {
                    'fund_id' : fund_id,
                    f'{fund_type}_name':r[1][f'rank{i}_{fund_type}'],
                    f'{fund_type}_weight':r[1][f'rank{i}_{fund_type}weight'], 
                    f'{fund_type}_id':r[1][f'rank{i}_{fund_type}_code']
                }
                _res.append(dic)
        df = pandas.DataFrame(_res)
        df = pandas.merge(df,fund_info[['fund_id','desc_name']],on='fund_id')
        #_sum = df[f'{fund_type}_weight'].sum()
        df[f'{fund_type}_weight'] = df[f'{fund_type}_weight']# / _sum
        df = df.sort_values(f'{fund_type}_weight',ascending=False)

        stock_list = df.stock_id.tolist()
        stock_info = DataManager.raw_data(func_name=f'get_em_stock_info', stock_list=stock_list)
        industry_info = DataManager.raw_data(func_name='get_em_industry_info',ind_class_type=IndClassType.SWI1)
        stock_info.loc[:,'sw_indus_1'] = stock_info.bl_sws_ind_code.map(lambda x: x.split('-')[0] if x is not None else None)
        _df1 = stock_info[['stock_id','name','sw_indus_1']]
        _df2 = industry_info[['em_id','ind_name']].rename(columns={'em_id':'sw_indus_1'})
        stock_info = pandas.merge(_df1,_df2,on='sw_indus_1')
        df = df.join(stock_info[['stock_id','ind_name']].set_index('stock_id'),on='stock_id')
        stock_price = DataManager.raw_data(func_name='get_em_stock_price_recent',codes=stock_list,columns=['pre_close'])
        stock_price.loc[:,'ret'] =  stock_price.close / stock_price.pre_close - 1
        df.join(stock_price[['stock_id','close','ret']].set_index('stock_id'), on='stock_id')
        return df

    @staticmethod
    def group_left_year(x):
        if x <= 1:
            return '1年'
        if x <= 3:
            return '3年'
        if x <= 5:
            return '5年'
        if x <= 10:
            return '10年'

    @staticmethod
    def get_penetraded_bond_analysis(fund_list: pandas.core.series.Series,
                                      weight_list: pandas.core.series.Series):
        # fund_list 基金代码 比如 ['000005!0', '000015!0', '000016!0', '000032!0', '000033!0']  array 形式
        # weight_list 权重代码 比如 [0.1,0.2,0.2,0.2,0.3] array 形式
        df = pandas.DataFrame({'fund_id':fund_list,'weight':weight_list}).set_index('fund_id')
        fund_info = DataManager.basic_data(func_name=f'get_fund_info', fund_list = fund_list.tolist())
        fund_type = 'bond'
        fund_list = df.index.tolist()
        stock_weights = DataManager.basic_data(func_name=f'get_fund_hold_{fund_type}_latest', fund_list = fund_list)
        stock_weights = stock_weights.set_index('fund_id').drop(columns=['datetime','_update_time'])
        weight_list = [i for i in stock_weights if 'weight' in i]
        stock_weights = stock_weights.replace({None:np.nan})
        for r in stock_weights.iterrows():
            fund_id = r[0]
            fund_weight = df.loc[fund_id, 'weight']
            for weight_i in weight_list:
                stock_w = stock_weights.loc[fund_id, weight_i]
                stock_weights.loc[fund_id, weight_i] = stock_w / 100 * fund_weight
        
        _df = stock_weights.join(df)
        _res = []
        for r in stock_weights.iterrows():
            fund_id = r[0]
            for i in range(1,11):
                dic = {
                    'fund_id' : fund_id,
                    f'{fund_type}_name':r[1][f'rank{i}_{fund_type}'],
                    f'{fund_type}_weight':r[1][f'rank{i}_{fund_type}weight'], 
                    f'{fund_type}_id':r[1][f'rank{i}_{fund_type}_code']
                }
                _res.append(dic)
        df = pandas.DataFrame(_res)
        df = pandas.merge(df,fund_info[['fund_id','desc_name']],on='fund_id')
        df = df.dropna(subset=['bond_name'])
        _bond_list = df.bond_id.tolist()
        _bond_rate = DataManager.raw_data(func_name='get_em_bond_rate_maturity',codes=_bond_list)
        df = df.set_index('bond_id').join(_bond_rate[['bond_id','maturity','subject_rate']].set_index('bond_id')).reset_index()
        bond_info = DataManager.raw_data(func_name='get_em_bond_info',bond_id_list=_bond_list)
        _bond_info_bond_list = bond_info.bond_id.tolist()
        _conv_bond_list = [i for i in _bond_list if i not in _bond_info_bond_list]
        bond_info.loc[:,'cbl1_type'] = bond_info.cbl1_type.map(lambda x: x.replace('(中债)','').replace('（中债）',''))
        conv_bond_info = DataManager.raw_data(func_name='get_em_conv_bond_info',bond_id_list=_conv_bond_list)
        if conv_bond_info.empty:
            df = df.join(bond_info[['bond_id','cbl1_type']].set_index('bond_id'), on='bond_id')
        else:
            conv_bond_info = conv_bond_info[['CODES']].rename(columns={'CODES':'bond_id'})
            conv_bond_info.loc[:,'cbl1_type'] = '可转债'
            df = df.join(bond_info[['bond_id','cbl1_type']].append(conv_bond_info[['bond_id','cbl1_type']]).set_index('bond_id'), on='bond_id')
        check_df = df.copy()
        #_sum = df[f'{fund_type}_weight'].sum()
        df[f'{fund_type}_weight'] = df[f'{fund_type}_weight']# / _sum
        df = df.sort_values(f'{fund_type}_weight',ascending=False)
        today = datetime.datetime.now().date()
        td = (df.maturity - today)
        _years = [_.days / 365 for _ in td]
        df.loc[:,'maturity_yearly'] = _years
        df.loc[:,'left_year'] = df.maturity_yearly.map(lambda x: Calculator.group_left_year(x))
        bond_weight_df = df[['cbl1_type','bond_weight']].dropna().groupby('cbl1_type').sum()
        bond_weight_df = bond_weight_df / bond_weight_df.sum()
        bond_rate_df = df[['subject_rate','bond_weight']].dropna().groupby('subject_rate').sum()
        bond_rate_df = bond_rate_df / bond_rate_df.sum()
        left_maturity_year = df[['left_year','bond_weight']].dropna().groupby('left_year').sum()
        left_maturity_year = left_maturity_year / left_maturity_year.sum()
        result = {
            'bond_in_funds': df, #基金组合持有债券穿透分析
            'bond_type_weight': bond_weight_df, #基金组合债券种类分布
            'bond_rate_weight': bond_rate_df, # 基金组合债券评级分布
            'bond_maturity_weight': left_maturity_year, # 债券组合债券到期分布
        }
        return result

    @staticmethod
    def get_fund_last_week_last_trade_df(dt:datetime.date=None, fund_list:list=[]):
        # 日期不填默认上周最后交易日开始
        if dt is None:
            dt = DataManager.basic_data(func_name='get_last_week_last_trade_dt')
        fund_nav = DataManager.basic_data(func_name='get_fund_nav_with_date',start_date=dt,fund_list=fund_list)
        fund_nav = fund_nav.pivot_table(index='datetime',columns='fund_id',values='adjusted_net_value')
        fund_nav = pandas.DataFrame((fund_nav / fund_nav.iloc[0]).iloc[-1] - 1)
        fund_nav.columns = ['ret']
        return fund_nav

    @staticmethod
    def get_fund_annual_ret_vol_recent_and_history(fund_list:list, hold_date_list:list):
        nav = DataManager.basic_data(func_name='get_fund_nav_with_date',fund_list=fund_list)
        nav = nav.pivot_table(index='datetime',columns='fund_id',values='adjusted_net_value')
        result = {}
        for fund_id, hold_date in zip(fund_list,hold_date_list):
            result[fund_id] = {}
            for b_d in [None, hold_date]:
                if b_d is None:
                    nav_i = nav[fund_id].dropna()
                else:
                    nav_i = nav[fund_id].loc[b_d:].dropna()
                last_unit_nav = nav_i.iloc[-1] / nav_i.iloc[0]
                days = (nav_i.index[-1] - nav_i.index[0]).days
                annual_ret = math.pow(last_unit_nav, CalculatorBase.TOTAL_DAYS_PER_YEAR/days) - 1
                annual_vol = nav_i.pct_change(1).std(ddof=1) * np.sqrt(CalculatorBase.TRADING_DAYS_PER_YEAR)
                if b_d is None:
                    result[fund_id]['history_annual_ret'] = annual_ret
                    result[fund_id]['history_annual_vol'] = annual_vol
                else:
                    result[fund_id]['hold_annual_ret'] = annual_ret
                    result[fund_id]['hold_annual_vol'] = annual_vol
        return result

    @staticmethod
    def get_manager_result(dates: pandas.core.series.Series,
                          values: pandas.core.series.Series,
                          frequency:str='daily'):
        assert len(dates) == len(values), 'date and value has different numbers'
        
        if len(dates) > 1:
            sr = pandas.Series(values, index=dates).sort_index()
            risk_fee_rate = Calculator.get_risk_free_rate()
            start_date = sr.index[0] 
            end_date = sr.index[-1]
            yearly_multiplier = Calculator.get_yearly_multiplier(frequency)
            trade_year = sr.shape[0] * yearly_multiplier / Calculator.TRADING_DAYS_PER_YEAR
            last_unit_nav = sr[-1] / sr[0]
            annualized_ret = np.exp(np.log(last_unit_nav) / trade_year) - 1
            annualized_vol = (sr / sr.shift(1)).std(ddof=1) * np.sqrt(Calculator.TRADING_DAYS_PER_YEAR / yearly_multiplier)
            sharpe = (annualized_ret - risk_fee_rate) / annualized_vol
            mdd_part =  sr[:] / sr[:].rolling(window=sr.shape[0], min_periods=1).max()
            mdd = 1 - mdd_part.min()
        # 如果只输入一天，返回空
        else:
            start_date = dates[0] if len(dates) > 0 else None
            end_date = dates[0] if len(dates) > 0 else None
            trade_year = 0
            last_unit_nav = 1
            annualized_ret = 0
            annualized_vol = 0
            sharpe = 0 
            mdd = 0

        return {
            'start_date': start_date,
            'end_date': end_date,
            'trade_year' : trade_year,
            'annualized_ret' : annualized_ret,
            'annualized_vol' : annualized_vol,
            'sharpe' : sharpe,
            'mdd' : mdd,
        }
        
    @staticmethod
    def get_manager_stat_result(dates: pandas.core.series.Series,
                                  values: pandas.core.series.Series,
                                  benchmark_values: pandas.core.series.Series,
                                  frequency:str='daily'):
        
        assert len(dates) == len(values), 'date and port_values has different numbers'
        assert len(dates) == len(benchmark_values), 'date and bench_values has different numbers'
        res = Calculator.get_manager_result(dates, values)
        sr_values  = pandas.Series(values, index=dates).sort_index()  
        sr_values = sr_values / sr_values[0]
        yearly_multiplier = Calculator.get_yearly_multiplier(frequency)
        sr_benchmark_values = pandas.Series(benchmark_values, index=dates).sort_index()  
        sr_benchmark_values = sr_benchmark_values / sr_benchmark_values[0]
        sr_values_ret = sr_values.pct_change(1)
        sr_benchmark_ret = sr_benchmark_values.pct_change(1)
        x = sr_benchmark_ret.dropna().values
        y = sr_values_ret.dropna().values
        x = sm.add_constant(x)
        if x.shape[1] < 2:
            return {
                'start_date': res['start_date'],
                'end_date': res['end_date'],
                'trade_year':res['trade_year'],
                'annualized_ret':res['annualized_ret'],
                'annualized_vol':res['annualized_vol'],
                'sharpe':res['sharpe'],
                'mdd':res['mdd'],
                'alpha':np.nan,
                'beta':np.nan,
                'track_err':np.nan,
            }
        model = regression.linear_model.OLS(y,x).fit()
        x = x[:,1]
        alpha = model.params[0] * Calculator.TRADING_DAYS_PER_YEAR / yearly_multiplier
        beta = model.params[1]
        track_err = (sr_values_ret - sr_benchmark_ret).std(ddof=1) * np.sqrt(Calculator.TRADING_DAYS_PER_YEAR / yearly_multiplier)
        
        return {
                'start_date': res['start_date'],
                'end_date': res['end_date'],
                'trade_year':res['trade_year'],
                'annualized_ret':res['annualized_ret'],
                'annualized_vol':res['annualized_vol'],
                'sharpe':res['sharpe'],
                'mdd':res['mdd'],
                'alpha':alpha,
                'beta':beta,
                'track_err':track_err,
        }

    @staticmethod
    def calc_cl_alpha_beta(total: np.ndarray):
        if total.shape[0] <= 1:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    }
        X = np.array([total[:, 1], total[:, 1]]).T
        X[:, 0][X[:, 0] < 0] = 0
        X[:, 1][X[:, 1] > 0] = 0
        if np.count_nonzero(X[:, 1]) == 0:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    }
        est2 = sm.OLS(total[:, 0], sm.add_constant(X, prepend=False)).fit()
        return {'beta':est2.params[0] - est2.params[1],
                'alpha':est2.params[-1],
                }
    
    @staticmethod
    def calc_continue_regress_v(monthly_ret):
        # 半年周期
        window = 6
        yearly_multiplier = 2
        period_num = 12
        risk_fee_rate = Calculator.get_risk_free_rate()
        annual_ret = monthly_ret.rolling(window=window).apply(lambda x : x.sum() * yearly_multiplier - risk_fee_rate)
        annual_vol = monthly_ret.rolling(window=window).apply(lambda x : x.std(ddof=1) * np.sqrt(period_num))
        sharpe = (annual_ret / annual_vol)
        sharpe = sharpe.replace(np.Inf, np.nan).replace(-np.Inf, sharpe).dropna() # 空值sharpe赋值np.nan
        if sharpe.shape[0] < 6:
            return np.nan
        mod = AutoReg(endog=sharpe.values, lags=1)
        res = mod.fit()
        continue_regress_v = res.params[0]
        return continue_regress_v

    @staticmethod
    def get_benchmark(index_price: pandas.DataFrame,
                        weight_list: list,
                        index_list: list,
                        begin_date: datetime.date,
                        end_date: datetime.date)->pandas.DataFrame:

        assert len(weight_list) == len(index_list), 'weight_list and index_list has different numbers'
        assert index_price.shape[1] == len(weight_list), 'columns in index_price are not equal to index list'
        assert begin_date <= end_date, 'end date must bigger than begin date'
        if len(weight_list) < 1:
            return pandas.DataFrame()
        index_price = index_price.loc[begin_date:end_date,].fillna(method='bfill').fillna(method='ffill')
        index_price = index_price / index_price.iloc[0]
        weight_dict = [{'index_id':index_id, 'weight':weight_i } for index_id, weight_i in zip(index_list, weight_list)]
        weight_df = pandas.DataFrame(weight_dict)
        weight_df['weight'] = weight_df['weight'] / weight_df.weight.sum()
        weight_df = weight_df.set_index('index_id').T
        index_price['benchmark'] = index_price.mul(weight_df.values).sum(axis=1)
        return index_price[['benchmark']]

    @staticmethod
    def get_turnover_rate(dates: pandas.core.series.Series,
                          values: pandas.core.series.Series,
                          total_amount: float):
        year_num = len(list(set([_.year for _ in dates])))
        return total_amount / gmean(values) / year_num * 100

    @staticmethod
    def get_stat_result_from_df(df: pandas.DataFrame,
                                date_column: str,
                                value_column: str,
                                frequency: str = '1D'):
        dates = df[date_column].values
        values = df[value_column].values
        return Calculator.get_stat_result(dates, values, frequency)

    @staticmethod
    def get_benchmark_stat_result_from_df(df: pandas.DataFrame,
                                          date_column: str,
                                          port_value_column: str,
                                          bench_value_column: str,
                                          frequency: str = '1D'
                                          ):
        dates = df[date_column].values
        port_values = df[port_value_column].values
        bench_values = df[bench_value_column].values
        return Calculator.get_benchmark_stat_result(dates, port_values, bench_values, frequency)

    @staticmethod
    def get_benchmark_result(index_list:list,
                             weight_list:list,
                             begin_date: datetime.date,
                             end_date: datetime.date) -> pandas.DataFrame:
        '''
        index_list = ['hs300','national_debt']
        weight_list = [0.7,0.3]
        begin_date = datetime.date(2005,1,1)
        end_date = datetime.date(2020,1,1)
        Calculator.get_benchmark_result(index_list, weight_list, begin_date, end_date)
        '''                   
        basic = BasicDataApi()
        index_price = basic.get_index_price(index_list).pivot_table(index='datetime', columns='index_id', values='close')
        return Calculator.get_benchmark(index_price, weight_list, index_list, begin_date, end_date)
    
    @staticmethod
    def get_index_pct_data_df(index_id:str='hs300',
                           index_val:str=None,
                           windows:int=10*242,
                           min_periods:int=5*242,
                           pct_list:list=[0.15, 0.5, 0.6, 0.8]):
        
        assert (index_id in list(TaaTunerParam.PCT_PAIR.keys())) or (index_val is not None), \
            f'neither index_id{index_id} nor index_val {index_val} is valid'

        index_val = index_val if index_val else TaaTunerParam.PCT_PAIR[index_id]
        # load data
        index_val_data = DerivedDataApi().get_index_valuation_develop_without_date(index_ids=[index_id])
        
        values = index_val_data[index_val].values
        dates = index_val_data.datetime.values
        return  Calculator.get_index_pct_data(dates=dates,
                                            values=values,
                                            pct_list=pct_list,
                                            windows=windows,
                                            min_periods=min_periods)

    @staticmethod
    def roll_pct(x, pct_list, res):
        l = sorted(x)
        lens = len(l)
        res.append([l[int(lens*pct_i)] for pct_i in pct_list])
        return 1

    @staticmethod
    def get_index_pct_data(dates:pandas.core.series.Series,
                              values: pandas.core.series.Series,
                              pct_list:list,
                              windows:int,
                              min_periods:int):
        df = pandas.DataFrame(values, index=dates).dropna()
        res = []
        df[0].rolling(window= windows, min_periods=min_periods).apply(partial(Calculator.roll_pct, pct_list=pct_list, res=res), raw=True)
        return pandas.DataFrame(res, index=dates[-len(res):])

    @staticmethod
    def get_taa_detail(index_id:str='hs300',
                       index_val:str='roe_pct',
                       taa_param:TAAParam=TAAParam(),
                       ):
        
        # load data
        _dts = BasicDataApi().get_trading_day_list()
        dts = _dts.datetime 
        index_val_data = DerivedDataApi().get_index_valuation_develop_without_date(index_ids=[index_id])
        index_val_data = index_val_data.set_index('datetime').reindex(dts).fillna(method='ffill')
        asset_func_index = 'hs300'
        index_val_data['index_id'] = asset_func_index
        index_val_data = index_val_data.reset_index().set_index(['datetime','index_id'])
        fake_weight = AssetWeight(**{asset_func_index:1})
        taa_helper = TAAHelper(taa_params=taa_param)
        for dt in dts:
            asset_pct = index_val_data.loc[dt]
            taa_helper.on_price(dt=dt, asset_price=None, cur_saa=fake_weight, asset_pct=asset_pct, select_val={asset_func_index:index_val}, score_dict={})
        df = pandas.DataFrame(taa_helper.tactic_history).T.dropna()
        df['last_date'] = df.index.to_series().shift(1)
        con = df[asset_func_index] != df[asset_func_index].shift(1)
        df_diff_part = df[con].copy()
        df_diff_part = df_diff_part.reset_index().rename(columns={'index':'begin_date'})
        next_date = df_diff_part['last_date'].shift(-1).tolist()
        next_date[-1] = df.index.values[-1]
        df_diff_part['end_date'] = next_date
        df_result = df_diff_part[df_diff_part[asset_func_index] != TAAStatusMode.NORMAL][['begin_date','end_date',asset_func_index]]
        df_result = df_result.rename(columns = {asset_func_index:'status'})
        return df_result.to_dict('records') 

    @staticmethod
    def get_val_level(x):
        val_dict = {
            'PB百分位':'pb_pct',
            'PE百分位':'pe_pct',
            'PS百分位':'ps_pct',
        }
        pct = getattr(x, val_dict[x.tag_method])
        pe = x.pe_ttm
        if None in [pct,pe]:
            return None
        if pct < 0.3 and pe < 20:
            res = 'low'
        elif pct > 0.7 and pe > 20:
            res = 'high'
        else:
            res = 'median'
        return res

    @staticmethod
    def get_index_level(dt:datetime.date=datetime.date(2020,7,20)):
    
        with BasicDatabaseConnector().managed_session() as db_session:
            query = db_session.query(
                    IndexInfo
            )
            index_info = pandas.read_sql(query.statement, query.session.bind)
        with DerivedDatabaseConnector().managed_session() as mn_session:
            query = mn_session.query(
                IndexValuationLongTerm
            ).filter(
                IndexValuationLongTerm.datetime== dt,
            )
            index_val_df = pandas.read_sql(query.statement, query.session.bind)
        index_val = index_val_df.set_index('index_id').join(index_info.set_index('index_id')[['tag_method']]).reset_index()
        index_val['val_level'] = index_val.apply(lambda x : Calculator.get_val_level(x), axis=1 )
        return index_val[['index_id','val_level']]

    @staticmethod
    def get_index_level_index(index_id:str='hs300'):
        with BasicDatabaseConnector().managed_session() as db_session:
            query = db_session.query(
                    IndexInfo
            )
            index_info = pandas.read_sql(query.statement, query.session.bind)
        with DerivedDatabaseConnector().managed_session() as mn_session:
            query = mn_session.query(
                IndexValuationLongTerm
            ).filter(
                IndexValuationLongTerm.index_id.in_([index_id]),
            )
            index_val_df = pandas.read_sql(query.statement, query.session.bind)
        index_val = index_val_df.set_index('index_id').join(index_info.set_index('index_id')[['tag_method']]).reset_index()
        index_val['val_level'] = index_val.apply(lambda x : Calculator.get_val_level(x), axis=1 )
        index_val = index_val[['datetime','val_level']]
        res = []
        last_level = 'begin'
        dic = {}
        for i in index_val.itertuples():
            if i.val_level != last_level and not dic:
                dic.update({'start_date':i.datetime})
                dic.update({'val_level':i.val_level})
                last_level = i.val_level

            elif i.val_level != last_level and dic:
                dic.update({'end_date':last_date})
                last_level = i.val_level
                res.append(dic)
                dic = {}
                dic.update({'start_date':i.datetime})
                dic.update({'val_level':i.val_level})
            last_date = i.datetime
        if 'end_date' not in dic:
            dic.update({'end_date':last_date}) 
        res.append(dic)
        res = [i for i in res if i['val_level'] != 'median']
        return res

    @staticmethod
    def get_index_level_index_by_tag_method(index_id: str, tag_method: str):
        val_dict = {
            'PB百分位': IndexValuationLongTerm.pb_pct,
            'PE百分位': IndexValuationLongTerm.pe_pct,
            'PS百分位': IndexValuationLongTerm.ps_pct,
        }

        with DerivedDatabaseConnector().managed_session() as mn_session:
            query = mn_session.query(
                IndexValuationLongTerm.pe_ttm,
                IndexValuationLongTerm.datetime,
                val_dict.get(tag_method),
            ).filter(
                IndexValuationLongTerm.index_id.in_([index_id]),
            )
            index_val_df = pandas.read_sql(query.statement, query.session.bind)
        index_val_df['tag_method'] = tag_method
        if len(index_val_df) < 1:
            return []
        index_val_df['val_level'] = index_val_df.apply(lambda x: Calculator.get_val_level(x), axis=1)
        index_val = index_val_df[['datetime', 'val_level']]
        index_val = index_val.dropna(how='any')
        if len(index_val) < 1:
            return []
        res = []
        last_level = 'begin'
        dic = {}
        for i in index_val.itertuples():
            if i.val_level != last_level and not dic:
                dic.update({'start_date': i.datetime})
                dic.update({'val_level': i.val_level})
                last_level = i.val_level

            elif i.val_level != last_level and dic:
                dic.update({'end_date': last_date})
                last_level = i.val_level
                res.append(dic)
                dic = {}
                dic.update({'start_date': i.datetime})
                dic.update({'val_level': i.val_level})
            last_date = i.datetime
        if 'end_date' not in dic:
            dic.update({'end_date': last_date})
        res.append(dic)
        res = [i for i in res if i['val_level'] != 'median']
        return res

    @staticmethod
    def get_mdd_recover_result(mv_df:pandas.DataFrame):

        def _get_mdd_recover_result_df(df:pandas.DataFrame, date_column:str, value_column:str):
            dates = df[date_column].values
            values = df[value_column].values
            return _mdd_recover_analysis(values,dates)

        def _mdd_recover_analysis(values,dates):
            sr = pandas.Series(values, index=dates).sort_index()
            if sr.empty:
                mdd = 0
                mdd_date1 = None
                mdd_date2 = None
                mdd_lens = 0
                return mdd, mdd_date1, mdd_date2, mdd_lens
            mdd_part =  sr[:] / sr[:].rolling(window=sr.shape[0], min_periods=1).max()
            mdd = 1 - mdd_part.min()
            if mdd == 0:
                mdd_date1 = None
                mdd_date2 = None
                mdd_lens = 0
            else:
                mdd_date = mdd_part.idxmin()
                mdd_date1 = sr[:mdd_date].idxmax()
                sr_tmp = sr[mdd_date1:]
                recover_sr = sr_tmp[sr_tmp> sr[mdd_date1]]
                if recover_sr.empty:
                    mdd_date2 = sr_tmp.index[-1]
                else: 
                    mdd_date2 = sr_tmp[sr_tmp> sr[mdd_date1]].index[0]
                mdd_lens = sr.loc[mdd_date1:mdd_date2].shape[0]
            return mdd, mdd_date1, mdd_date2, mdd_lens

        mdd1, mdd_date1_1, mdd_date1_2, mdd_lens1 = _get_mdd_recover_result_df(mv_df.reset_index(),'date','mv')
        mv_df_1 = mv_df.loc[:mdd_date1_1].reset_index()
        mv_df_2 = mv_df.loc[mdd_date1_2:].reset_index()

        mdd2, mdd_date2_1, mdd_date2_2, mdd_lens2 = _get_mdd_recover_result_df(mv_df_1,'date','mv')
        mdd3, mdd_date3_1, mdd_date3_2, mdd_lens3 = _get_mdd_recover_result_df(mv_df_2,'date','mv')
        if mdd3 > mdd2:
            mdd2 = mdd3
            mdd_date2_1 = mdd_date3_1
            mdd_date2_2 = mdd_date3_2
            mdd_lens2 = mdd_lens3

        res = {
            'mdd1':mdd1,
            'mdd1_d1':mdd_date1_1,
            'mdd1_d2':mdd_date1_2,
            'mdd1_lens':mdd_lens1,
            'mdd2':mdd2,
            'mdd2_d1':mdd_date2_1,
            'mdd2_d2':mdd_date2_2,
            'mdd2_len':mdd_lens2
        }

        return res

    @staticmethod
    def get_mdd_result(mv_df:pandas.DataFrame):

        def _get_mdd_result_df(df:pandas.DataFrame, date_column:str, value_column:str):
            dates = df[date_column].values
            values = df[value_column].values
            return _mdd_analysis(values,dates)

        def _mdd_analysis(values,dates):
            sr = pandas.Series(values, index=dates).sort_index()
            if sr.empty:
                mdd = 0
                mdd_date1 = None
                mdd_date2 = None
                mdd_lens = 0
                return mdd, mdd_date1, mdd_date2, mdd_lens
            mdd_part =  sr[:] / sr[:].rolling(window=sr.shape[0], min_periods=1).max()
            mdd = 1 - mdd_part.min()
            if mdd == 0:
                mdd_date1 = None
                mdd_date2 = None
                mdd_lens = 0
            else:
                mdd_date2 = mdd_part.idxmin()
                mdd_date1 = sr[:mdd_date2].idxmax()
                mdd_lens = sr.loc[mdd_date1:mdd_date2].shape[0]
            return mdd, mdd_date1, mdd_date2, mdd_lens

        mdd1, mdd_date1_1, mdd_date1_2, mdd_lens1 = _get_mdd_result_df(mv_df.reset_index(),'date','mv')
        mv_df_1 = mv_df.loc[:mdd_date1_1].reset_index()
        mv_df_2 = mv_df.loc[mdd_date1_2:].reset_index()

        mdd2, mdd_date2_1, mdd_date2_2, mdd_lens2 = _get_mdd_result_df(mv_df_1,'date','mv')
        mdd3, mdd_date3_1, mdd_date3_2, mdd_lens3 = _get_mdd_result_df(mv_df_2,'date','mv')
        if mdd3 > mdd2:
            mdd2 = mdd3
            mdd_date2_1 = mdd_date3_1
            mdd_date2_2 = mdd_date3_2
            mdd_lens2 = mdd_lens3

        res = {
            'mdd1':mdd1,
            'mdd1_d1':mdd_date1_1,
            'mdd1_d2':mdd_date1_2,
            'mdd1_lens':mdd_lens1,
            'mdd2':mdd2,
            'mdd2_d1':mdd_date2_1,
            'mdd2_d2':mdd_date2_2,
            'mdd2_len':mdd_lens2
        }

        return res

    @staticmethod
    def get_asset_stats(df:pandas.DataFrame, asset_info: pandas.DataFrame):
        real_asset_dic = asset_info.set_index('real_name').to_dict()['asset_type']
        indicator_dics = {
            'last_unit_nav':'区间收益',
            'annualized_ret':'年化收益',
            'annualized_vol':'年化波动',
            'mdd':'最大回撤',
            'sharpe':'夏普比率',
            'ret_over_mdd':'卡玛比率',
            'downside_std':'下行风险',
        }
        result = []
        for asset in df:
            dates = df[asset].index
            values = df[asset].values
            dic = Calculator.get_stat_result(dates=dates,values=values).__dict__
            dic['具体指数'] = asset
            dic['类别'] = real_asset_dic[asset]
            result.append(dic)

        df = pandas.DataFrame(result)
        df = df[list(indicator_dics.keys())+['具体指数','类别']].rename(columns=indicator_dics)
        l = ['夏普比率','具体指数','类别']
        for col in df:
            if col not in l:
                df[col] = (df[col] * 100).round(2)
        df['夏普比率'] = df['夏普比率'].round(2)
        return df
        
    @staticmethod
    def get_product_stats(df:pandas.DataFrame, asset_info: pandas.DataFrame):
        df = Calculator.get_asset_stats(df, asset_info)
        df = df.rename(columns={'具体指数':'产品'}).drop(columns=['类别'])
        name_dic = {}
        for r in asset_info.itertuples():
            if '典型产品' == r.asset_type:
                name_dic[r.real_name] = r.asset_name
            else:
                name_dic[r.real_name] = r.asset_type
        df.loc[:,'策略类型'] = df.产品.map(name_dic)
        return df

    @staticmethod
    def get_asset_corr(df:pandas.DataFrame, period='week'):#'month'
        if period == 'week':
            rule = '1W'
        else:
            rule = '1M'
        df = df.set_axis(pandas.to_datetime(df.index), inplace=False).resample(rule).last()
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        df = df.pct_change(1).iloc[1:].corr().round(3)
        df = df.sort_values(df.columns[0], ascending=False)
        df.index.name = 'index_id'
        return df

if __name__ == "__main__":
    # get pct with select rank
    Calculator.get_index_pct_data_df()
    Calculator.get_index_pct_data_df(index_id='hs300',
                           index_val='roe',
                           windows=5*242,
                           min_periods=3*242,
                           pct_list=[0.15, 0.5, 0.6, 0.8])

    # get taa detail
    Calculator.get_taa_detail()
    Calculator.get_taa_detail(index_id='hs300',
                              index_val='pb_pct',
                              taa_param=TAAParam(),
                              )

    Calculator.get_index_level_index(index_id='hs300')