
from typing import Dict, Any, Tuple, List

import numpy as np
import pandas as pd

from sqlalchemy.orm import sessionmaker

from ...util.singleton import Singleton
from ...constant import FOFTradeStatus, DividendCalcMethod
from ..view.derived_models import HedgeFundInvestorPurAndRedemp, HedgeFundInvestorDivAndCarry
from ..wrapper.mysql import DerivedDatabaseConnector
from ..api.derived import DerivedDataApi


class HedgeFundDataManager(metaclass=Singleton):

    def __init__(self):
        pass

    def _get_total_share(self, fof_id: str, investor_id: str = '', exclude1: List[int] = [], exclude2: List[str] = []) -> Tuple[float, pd.DataFrame]:
        part1 = DerivedDataApi().get_hedge_fund_investor_pur_redemp([fof_id])
        assert part1 is not None, '!!!!'
        part1 = part1[~part1.id.isin(exclude1)]
        part1_total_share = part1.share_changed.sum()
        if investor_id:
            part1 = part1.loc[part1.investor_id == investor_id, :]

        part2 = DerivedDataApi().get_hedge_fund_investor_div_carry([fof_id])
        part2 = part2[~part2.id.isin(exclude2)]
        assert part2 is not None, '!!!!'
        part2_total_share = part2.share_changed.sum()
        if investor_id:
            part2 = part2.loc[part2.investor_id == investor_id, :]

        total_share = part1_total_share + part2_total_share
        share_separate = part1[['investor_id', 'share_changed']].groupby(by='investor_id', sort=False).sum().add(part2[['investor_id', 'share_changed']].groupby(by='investor_id', sort=False).sum(), fill_value=0)
        return total_share, share_separate

    def _refresh_datas_after_updating(self, fof_id: str, investor_id: str, datetime):
        datetime: datetime.date = pd.to_datetime(datetime, infer_datetime_format=True).date()

        part1 = DerivedDataApi().get_hedge_fund_investor_pur_redemp([fof_id])
        assert part1 is not None, '!!!!'
        part1 = part1[part1.investor_id == investor_id].sort_values(by='datetime')
        last_valid_share: float = part1[part1.datetime <= datetime].iloc[-1, :].share_after_trans

        to_refresh = part1.loc[part1.datetime > datetime, :]
        to_refresh = to_refresh.set_index('id').share_changed.cumsum() + last_valid_share

        Session = sessionmaker(DerivedDatabaseConnector().get_engine())
        db_session = Session()
        for row in db_session.query(HedgeFundInvestorPurAndRedemp).filter(
            HedgeFundInvestorPurAndRedemp.fof_id == fof_id,
            HedgeFundInvestorPurAndRedemp.investor_id == investor_id,
            HedgeFundInvestorPurAndRedemp.datetime > datetime,
        ).all():
            row.share_after_trans = float(to_refresh.at[row.id])
        db_session.commit()
        db_session.close()

    def investor_pur_redemp_update(self, datas: Dict[str, Any]):
        '''
        申赎记录更新/添加

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                id : 如果是添加 则不需要该字段; 否则则需要
                fof_id : 产品ID
                datetime : 交易日期
                event_type : 交易类型(认购/申购/赎回)
                investor_id : 投资人ID
                net_asset_value : 单位净值
                acc_unit_value : 累计净值
                amount : 申购金额/认购金额
                raising_interest : 募集期利息
                redemp_share : 赎回份额
                redemp_fee : 赎回费

        Returns/Exceptions
        -------
        throw excepion if failed, or return id (an integer) if succeed
        '''

        event_type = datas['event_type']
        if event_type == FOFTradeStatus.PURCHASE:
            # 认购
            datas['purchase_amount'] = datas['amount']
            datas['share_changed'] = (datas['amount'] + datas['raising_interest']) / datas['net_asset_value']
        elif event_type == FOFTradeStatus.SUBSCRIBE:
            # 申购
            datas['purchase_amount'] = datas['amount']
            datas['share_changed'] = datas['amount'] / datas['net_asset_value']
        elif event_type == FOFTradeStatus.REDEEM:
            # 赎回
            datas['share_changed'] = -datas['redemp_share']
            datas['redemp_confirmed_amount'] = datas['redemp_share'] * datas['net_asset_value'] - datas['redemp_fee']
            # TODO: calc carry_amount
            datas['carry_amount'] = np.nan
        else:
            raise ValueError(f'invalid event_type {event_type}')

        _, share_separate = self._get_total_share(datas['fof_id'], datas['investor_id'], exclude1=[datas['id']] if 'id' in datas else [])
        try:
            datas['share_after_trans'] = float(share_separate.at[datas['investor_id'], 'share_changed']) + datas['share_changed']
        except KeyError:
            datas['share_after_trans'] = datas['share_changed']

        df = pd.Series(datas).drop(['amount', 'redemp_share'], errors='ignore').to_frame().T
        # TODO: 原子操作下面几步
        if 'id' in datas:
            DerivedDataApi().delete_hedge_fund_investor_pur_redemp(id_to_delete=datas['id'])
        print(df)
        df.to_sql(HedgeFundInvestorPurAndRedemp.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
        if 'id' in datas:
            self._refresh_datas_after_updating(datas['fof_id'], datas['investor_id'], datas['datetime'])

    def investor_pur_redemp_remove(self, id: int):
        '''
        申赎记录删除

        Parameters
        ----------
        id : int
            对应数据库中id

        Returns/Exceptions
        -------
        throw excepion if failed
        '''

        df = DerivedDataApi().get_hedge_fund_investor_pur_redemp_by_id(id)
        assert df is not None, f'failed to get hedge fund investor data by id {id}'
        assert df.shape[0] == 1, f'invalid id {id}'

        s = df.iloc[-1, :]
        DerivedDataApi().delete_hedge_fund_investor_pur_redemp(id_to_delete=id)
        self._refresh_datas_after_updating(s.fof_id, s.investor_id, s.datetime)

    def investor_div_carry_add(self, datas: Dict[str, Any]):
        '''
        分红/业绩计提记录添加

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                fof_id : 产品ID
                datetime : 分红/计提日期
                event_type : 交易类型(现金分红/红利再投/计提业绩报酬)
                investor_id : 投资人ID
                net_asset_value : 单位净值
                acc_unit_value : 累计净值
                total_dividend : 红利总额
                cash_dividend : 现金分红金额
                reinvest_amount : 再投资金额
                carry_amount : 业绩报酬金额
                share_changed : 份额变更
                share_after_trans : 分红/计提后份额

        Returns/Exceptions
        -------
        throw excepion if failed, or return id (an integer) if succeed
        '''

        event_type = datas['event_type']
        if event_type == FOFTradeStatus.DEDUCT_REWARD:
            # 计提业绩报酬
            return
        else:
            total_share, share_separate = self._get_total_share(datas['fof_id'], datas['investor_id'])
            share_separate = share_separate.share_changed.array[-1]
            div = datas['total_dividend'] * share_separate / total_share

            if event_type == FOFTradeStatus.DIVIDEND_CASH:
                # 现金分红
                datas['share_changed'] = 0
                datas['cash_dividend'] = div
            elif event_type == FOFTradeStatus.DIVIDEND_VOLUME:
                # 红利再投
                datas['share_changed'] = (div - (datas['carry_amount'] if not pd.isnull(datas['carry_amount']) else 0)) / datas['net_asset_value']
                datas['reinvest_amount'] = div
            else:
                raise ValueError(f'invalid event_type {event_type}')

            datas['share_after_trans'] = share_separate + datas['share_changed']

        for k in ('reinvest_amount', 'share_changed', 'cash_dividend', 'share_after_trans', 'carry_amount', 'total_dividend', 'net_asset_value', 'acc_unit_value'):
            datas[k] = float(datas[k])

        df = pd.Series(datas).to_frame().T
        # TODO: 原子操作下面两步
        if 'id' in datas:
            DerivedDataApi().delete_hedge_fund_investor_div_carry(id_to_delete=datas['id'])
        df.to_sql(HedgeFundInvestorDivAndCarry.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')

    def investor_div_carry_remove(self, id: int):
        '''
        分红/业绩计提记录删除

        Parameters
        ----------
        id : int
            对应数据库中id

        Returns/Exceptions
        -------
        throw excepion if failed
        '''

        DerivedDataApi().delete_hedge_fund_investor_div_carry(id_to_delete=id)

    def calc_dividend_event(self, datas: Dict[str, Any]) -> pd.DataFrame:
        '''
        计算分红事件

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                fof_id : 产品ID
                datetime : 分红日期
                event_type : 红利发放方式(现金分红/红利再投)
                net_asset_value : 单位净值
                acc_unit_value : 累计净值
                calc_method : 计算方法(红利总额/每单位红利)
                dividend_for_calc : 红利总额/每单位红利
                do_deduct_reward: 是否计提业绩报酬

        Returns/Exceptions
        -------
        throw excepion if failed, or return df if succeed
        '''

        total_share, share_separate = self._get_total_share(datas['fof_id'])
        share_separate = share_separate.share_changed
        weight = share_separate / total_share

        calc_method = datas['calc_method']
        if calc_method == DividendCalcMethod.BY_TOTAL_AMOUNT:
            # 红利总额
            dividend_amount = datas['dividend_for_calc']
        elif calc_method == DividendCalcMethod.BY_PER_UNIT:
            # 每单位红利
            dividend_amount = total_share * datas['dividend_for_calc']
        else:
            raise ValueError(f'invalid calc_method {calc_method}')

        s = dividend_amount * weight
        event_type = datas['event_type']
        if datas['event_type'] == FOFTradeStatus.DIVIDEND_CASH:
            # 现金分红
            df = s.to_frame('cash_dividend')
            df['share_changed'] = 0
            df['reinvest_amount'] = 0
        elif datas['event_type'] == FOFTradeStatus.DIVIDEND_VOLUME:
            # 红利再投
            df = s.to_frame('reinvest_amount')
            df['share_changed'] = df.reinvest_amount / datas['net_asset_value']
            df['cash_dividend'] = 0
        else:
            raise ValueError(f'invalid event_type {event_type}')
        df['share_after_trans'] = share_separate + df.share_changed

        if 'do_deduct_reward' in datas and datas['do_deduct_reward']:
            # TODO: calc carry_amount
            df['carry_amount'] = np.nan
        else:
            df['carry_amount'] = np.nan
        df['fof_id'] = datas['fof_id']
        df['datetime'] = datas['datetime']
        df['event_type'] = datas['event_type']
        df['total_dividend'] = dividend_amount
        return df.reset_index()

    def calc_carry_event(self, datas: Dict[str, Any]) -> pd.DataFrame:
        '''
        计算业绩计提事件

        Parameters
        ----------
        datas : Dict[str, Any]
            数据, keys:
                fof_id : 产品ID
                datetime : 计提日期
                net_asset_value : 单位净值
                acc_unit_value : 累计净值

        Returns/Exceptions
        -------
        throw excepion if failed, or return df if succeed
        '''
        pass
