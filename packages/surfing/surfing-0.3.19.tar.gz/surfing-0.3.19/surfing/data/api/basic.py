
from typing import Tuple, List

import datetime
from sqlalchemy import distinct
from sqlalchemy.sql import func
import pandas as pd
import numpy as np
from ...util.singleton import Singleton
from ..wrapper.mysql import BasicDatabaseConnector
from ..view.basic_models import *
from .raw import RawDataApi

class BasicDataApi(metaclass=Singleton):
    def get_trading_day_list(self, start_date='', end_date=''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        TradingDayList
                    )
                if start_date:
                    query = query.filter(
                        TradingDayList.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        TradingDayList.datetime <= end_date,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {TradingDayList.__tablename__}')

    def get_last_week_last_trade_dt(self):
        today = datetime.datetime.today().date()
        start_date = today - datetime.timedelta(days=15)
        df = self.get_trading_day_list(start_date=start_date)
        df.loc[:,'weekday'] = df.datetime.map(lambda x : x.weekday())
        td = pd.to_datetime(df.datetime)
        td = [_.week for _ in td]
        df.loc[:,'week_num'] = td
        last_week_num = df.week_num.values[-1]
        last_week_dt = df[df.week_num != last_week_num].datetime.values[-1]
        return last_week_dt

    def is_today_trading_date(self):
        today = datetime.datetime.now().date()
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        TradingDayList
                    ).filter(
                        TradingDayList.datetime >= today,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                con = today in tag_df.datetime.tolist()
                return con

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {TradingDayList.__tablename__}')

    def get_last_trading_day(self, dt=datetime.datetime.today()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query_result = db_session.query(
                    func.max(TradingDayList.datetime)
                ).filter(
                    TradingDayList.datetime < dt.date(),
                ).one_or_none()
                if query_result:
                    return query_result[0]
                else:
                    return None

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {TradingDayList.__tablename__}')

    def get_sector_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        SectorInfo
                    )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorInfo.__tablename__}')

    def get_sector_index_funds(self, index_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        SectorFunds
                ).filter(
                    SectorFunds.index_id == index_id,
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorFunds.__tablename__}')

    def get_sector_index_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        SectorFunds
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorFunds.__tablename__}')

    def get_sector_main_index_id(self, sector_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    SectorInfo.main_index_id
                ).filter(
                    SectorInfo.sector_id == sector_id
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorInfo.__tablename__}')

    def get_sector_indices(self, sector_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    distinct(SectorFunds.index_id).label("index_id")
                ).filter(
                    SectorFunds.sector_id == sector_id
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorFunds.__tablename__}')

    def get_fund_info(self, fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo
                    )
                if fund_list:
                    query = query.filter(
                        FundInfo.fund_id.in_(fund_list),
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_benchmark(self, fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundBenchmark
                )
                if fund_list:
                    query = query.filter(
                        FundBenchmark.em_id.in_(fund_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundBenchmark.__tablename__}')

    def get_index_info(self, index_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexInfo
                    )
                if index_list:
                    query = query.filter(
                        IndexInfo.index_id.in_(index_list)
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexInfo.__tablename__}')

    def get_index_info_by_em_id(self, em_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexInfo
                    )
                if em_id_list:
                    query = query.filter(
                        IndexInfo.em_id.in_(em_id_list)
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexInfo.__tablename__}')

    def get_index_component(self, index_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    IndexComponent
                )
                if index_list:
                    query = query.filter(
                        IndexComponent.index_id.in_(index_list)
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexComponent.__tablename__}')
                return None

    def get_stock_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        StockInfo
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {StockInfo.__tablename__}')

    def get_fund_nav(self, fund_list=None, dt=None):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundNav
                )
                if fund_list:
                    query = query.filter(
                        FundNav.fund_id.in_(fund_list),
                    )
                if dt:
                    query = query.filter(
                        FundNav.datetime == dt,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundNav.__tablename__}')

    def delete_fund_nav(self, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundNav
                ).filter(
                    FundNav.datetime >= start_date,
                    FundNav.datetime <= end_date,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundNav.__tablename__}')
                return None

    def get_fund_nav_with_date(self, start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundNav.fund_id,
                    FundNav.adjusted_net_value,
                    FundNav.datetime
                )
                if fund_list:
                    query = query.filter(FundNav.fund_id.in_(fund_list))
                if start_date:
                    query = query.filter(
                        FundNav.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        FundNav.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundNav.__tablename__}')

    def get_stock_price(self, stock_list, begin_date: str = '', end_date: str = ''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        StockPrice
                ).filter(
                    # We could query all fund_ids at one time
                    StockPrice.stock_id.in_(stock_list),
                )
                if begin_date:
                    query = query.filter(StockPrice.datetime >= begin_date)
                if end_date:
                    query = query.filter(StockPrice.datetime <= end_date)

                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {StockPrice.__tablename__}')

    def get_fund_ret(self, fund_list):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundRet
                ).filter(
                        # We could query all fund_ids at one time
                        FundRet.fund_id.in_(fund_list),
                    )

                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundRet.__tablename__}')

    def get_index_price(self, index_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexPrice
                )
                if index_list:
                    query = query.filter(
                        # We could query all fund_ids at one time
                        IndexPrice.index_id.in_(index_list),
                    )

                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexPrice.__tablename__}')

    def get_index_price_dt(self, start_date: str = '', end_date: str = '', index_list: Tuple[str] = (), columns: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if columns:
                    query = db_session.query(
                        IndexPrice.index_id,
                        IndexPrice.datetime,
                    ).add_columns(*columns)
                else:
                    query = db_session.query(
                        IndexPrice
                    )
                if index_list:
                    query = query.filter(
                        IndexPrice.index_id.in_(index_list),
                    )
                if start_date:
                    query = query.filter(
                        IndexPrice.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        IndexPrice.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexPrice.__tablename__}')

    def delete_index_price(self, index_id_list, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    IndexPrice
                ).filter(
                    IndexPrice.index_id.in_(index_id_list),
                    IndexPrice.datetime >= start_date,
                    IndexPrice.datetime <= end_date,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {IndexPrice.__tablename__}')
                return None

    def get_fund_nav_with_date_range(self, fund_list, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundNav
                ).filter(
                        FundNav.fund_id.in_(fund_list),
                        FundNav.datetime >= start_date,
                        FundNav.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundNav.__tablename__}')

    def get_fund_list(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_fee(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.manage_fee,
                        FundInfo.trustee_fee,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_asset(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.asset_type,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_id_mapping(self):
        fund_id_mapping = {}
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query_results = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.order_book_id,
                        FundInfo.start_date,
                        FundInfo.end_date
                    ).all()

                for fund_id, order_book_id, start_date, end_date in query_results:
                    if order_book_id not in fund_id_mapping:
                        fund_id_mapping[order_book_id] = []
                    fund_id_mapping[order_book_id].append(
                        {'fund_id': fund_id, 'start_date':start_date, 'end_date': end_date})

            except Exception as e:
                print(f'Failed to get fund id mapping <err_msg> {e} from {FundInfo.__tablename__}')
                return None

        return fund_id_mapping

    def get_fund_size(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundSize,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundSize.__tablename__}')

    def get_fund_open_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundOpenInfo,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundOpenInfo.__tablename__}')


    def get_fund_status(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundStatusLatest,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundStatusLatest.__tablename__}')

    def get_inside_market_funds(self):
        fund_status_latest = self.get_fund_status()
        in_market_fund_list = fund_status_latest[(~fund_status_latest['trade_status'].isnull()) & (fund_status_latest.trade_status != '终止上市')].fund_id.tolist()
        fund_info = self.get_fund_info()
        return fund_info[fund_info.fund_id.isin(in_market_fund_list)]

    def get_outside_market_funds(self):
        fund_status_latest = self.get_fund_status()
        in_market_fund_list = fund_status_latest[(~fund_status_latest['trade_status'].isnull()) & (fund_status_latest.trade_status != '终止上市')].fund_id.tolist()
        fund_info = self.get_fund_info()
        return fund_info[~fund_info.fund_id.isin(in_market_fund_list)]

    def get_fund_conv_stats(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundConvStats,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e}')

    @staticmethod
    def get_history_fund_size(fund_id: str = '', start_date=None, end_date=None):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate,
                )
                if fund_id:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id == fund_id
                    )
                if start_date is not None:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime >= start_date,
                    )
                if end_date is not None:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    def delete_fund_size_hold_rate(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    Fund_size_and_hold_rate
                ).filter(
                    Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    Fund_size_and_hold_rate.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return False

    @staticmethod
    def get_fund_size_range(start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate.fund_id,
                    Fund_size_and_hold_rate.datetime,
                    Fund_size_and_hold_rate.size,
                )
                if fund_list:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    )
                if start_date:
                    query = query.filter(
                        # 按报告日多选取3个月，保证初值可以fill出来
                        Fund_size_and_hold_rate.datetime >= (pd.to_datetime(start_date) - datetime.timedelta(days=100)).strftime('%Y%m%d'),
                    )
                if end_date:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_company_hold(start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate.fund_id,
                    Fund_size_and_hold_rate.datetime,
                    Fund_size_and_hold_rate.institution_holds,
                )
                if fund_list:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    )
                if start_date:
                    query = query.filter(
                        # 按报告日多选取3个月，保证初值可以fill出来
                        Fund_size_and_hold_rate.datetime >= (pd.to_datetime(start_date) - datetime.timedelta(days=100)).strftime('%Y%m%d'),
                    )
                if end_date:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_persional_hold(start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate.fund_id,
                    Fund_size_and_hold_rate.datetime,
                    Fund_size_and_hold_rate.personal_holds,
                )
                if fund_list:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    )
                if start_date:
                    query = query.filter(
                        # 按报告日多选取3个月，保证初值可以fill出来
                        Fund_size_and_hold_rate.datetime >= (pd.to_datetime(start_date) - datetime.timedelta(days=100)).strftime('%Y%m%d'),
                    )
                if end_date:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_size_all_data():
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_history_fund_rating(fund_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundRate,
                ).filter(
                    FundRate.fund_id == fund_id
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundRate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_hold_asset_by_id(fund_id: str = '', start_date=None, end_date=None):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldAsset,
                )
                if fund_id:
                    query = query.filter(
                        FundHoldAsset.fund_id == fund_id,
                    )
                if start_date is not None:
                    query = query.filter(
                        FundHoldAsset.datetime >= start_date,
                    )
                if end_date is not None:
                    query = query.filter(
                        FundHoldAsset.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return pd.DataFrame([])

    def delete_fund_hold_asset(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldAsset
                ).filter(
                    FundHoldAsset.fund_id.in_(fund_list),
                    FundHoldAsset.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return False

    @staticmethod
    def get_fund_hold_industry_by_id(fund_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldIndustry,
                ).filter(
                    FundHoldIndustry.fund_id == fund_id,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldIndustry.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_hold_stock_by_id(fund_id: str = ''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldStock,
                )
                if fund_id:
                    query = query.filter(
                        FundHoldStock.fund_id == fund_id,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_hold_bond_by_id(fund_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldBond,
                ).filter(
                    FundHoldBond.fund_id == fund_id,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return pd.DataFrame([])

    def get_style_analysis_data(self, start_date: str, end_date: str, stock_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    StyleAnalysisStockFactor
                )
                if stock_list:
                    query = query.filter(
                        StyleAnalysisStockFactor.stock_id.in_(stock_list)
                    )
                query = query.filter(
                    StyleAnalysisStockFactor.datetime >= start_date,
                    StyleAnalysisStockFactor.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {StyleAnalysisStockFactor.__tablename__}')
                return

    def get_style_analysis_time_range(self) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    func.max(StyleAnalysisStockFactor.datetime).label('end_date'),
                    func.min(StyleAnalysisStockFactor.datetime).label('start_date'),
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {StyleAnalysisStockFactor.__tablename__}')
                return

    def get_barra_cne5_risk_factor(self, start_date: str, end_date: str, stock_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    BarraCNE5RiskFactor
                )
                if stock_list:
                    query = query.filter(
                        BarraCNE5RiskFactor.stock_id.in_(stock_list)
                    )
                query = query.filter(
                    BarraCNE5RiskFactor.datetime >= start_date,
                    BarraCNE5RiskFactor.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {BarraCNE5RiskFactor.__tablename__}')
                return

    def get_fund_hold_asset(self, dt) -> pd.DataFrame:
       with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundHoldAsset
                        ).filter(
                            FundHoldAsset.datetime == dt
                        )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return

    def get_fund_hold_industry(self, dt) -> pd.DataFrame:
       with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundHoldIndustry
                        ).filter(
                            FundHoldIndustry.datetime == dt
                        )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldIndustry.__tablename__}')
                return

    def delete_fund_hold_industry(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldIndustry
                ).filter(
                    FundHoldIndustry.fund_id.in_(fund_list),
                    FundHoldIndustry.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldIndustry.__tablename__}')
                return False

    def get_fund_hold_stock(self, dt=None) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldStock
                )
                if dt:
                    query = query.filter(
                        FundHoldStock.datetime == dt
                    )
                else:
                    query = query.filter(
                        FundHoldStock.datetime > datetime.datetime.now() - datetime.timedelta(days=180)
                    )

                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return

    def get_fund_hold_stock_latest(self, dt=None, fund_list =[]) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if not dt:
                    dt = db_session.query(
                        func.max(FundHoldStock.datetime)
                    ).filter(
                    FundHoldStock.fund_id.in_(fund_list),
                ).one_or_none()
                    if dt:
                        dt = dt[0]

                query = db_session.query(
                    FundHoldStock
                ).filter(
                    FundHoldStock.datetime == dt,
                    FundHoldStock.fund_id.in_(fund_list),
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return

    def get_fund_hold_bond_latest(self, dt=None, fund_list =[]) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if not dt:
                    dt = db_session.query(
                        func.max(FundHoldBond.datetime)
                    ).filter(
                    FundHoldBond.fund_id.in_(fund_list),
                ).one_or_none()
                    if dt:
                        dt = dt[0]
                query = db_session.query(
                    FundHoldBond
                ).filter(
                    FundHoldBond.datetime == dt,
                    FundHoldBond.fund_id.in_(fund_list),
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return

    def get_fund_hold_asset_latest(self, dt=None, fund_list = []) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if not dt:
                    dt = db_session.query(
                        func.max(FundHoldAsset.datetime)
                    ).filter(
                    FundHoldAsset.fund_id.in_(fund_list),
                ).one_or_none()
                    if dt:
                        dt = dt[0]

                query = db_session.query(
                        FundHoldAsset
                        ).filter(
                            FundHoldAsset.datetime == dt,
                            FundHoldAsset.fund_id.in_(fund_list),
                        )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return

    def delete_fund_hold_stock(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldStock
                ).filter(
                    FundHoldStock.fund_id.in_(fund_list),
                    FundHoldStock.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return False

    def get_fund_hold_bond(self, dt: str = '') -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldBond
                )
                if dt:
                    query = query.filter(
                        FundHoldBond.datetime == dt
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return

    def get_fund_ipo_stats(self, dt: str = '') -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundIPOStats
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundIPOStats.__tablename__}')
                return

    def delete_fund_hold_bond(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldBond
                ).filter(
                    FundHoldBond.fund_id.in_(fund_list),
                    FundHoldBond.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return False

    def get_fund_stock_portfolio(self, dt: str = ''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundStockPortfolio
                )
                if dt:
                    query = query.filter(
                        FundStockPortfolio.datetime == dt
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundStockPortfolio.__tablename__}')
                return

    def get_fund_stock_concept(self, tag_group_id_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    StockTag
                )
                if tag_group_id_list:
                    query = query.filter(
                        StockTag.tag_group_id.in_(tag_group_id_list)
                    )
                return pd.read_sql(query.statement, query.session.bind).drop(columns=['_update_time'])
            except Exception as e:
                print(f'Failed to get_fund_stock_concept <err_msg> {e} from {StockTag.__tablename__}')
                return

    def delete_fund_rate(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundRate
                ).filter(
                    FundRate.fund_id.in_(fund_list),
                    FundRate.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundRate.__tablename__}')

    @staticmethod
    def get_model_data(model: Base, *params):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        *(getattr(model, k) for k in params if hasattr(model, k))
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {model.__tablename__}')

    @classmethod
    def get_fund_info_data(cls, *params):
        return cls.get_model_data(FundInfo, *params)


    def get_hedge_fund_info(self, fund_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    HedgeFundInfo,
                )
                if fund_id_list:
                    query = query.filter(
                        HedgeFundInfo.fund_id.in_(fund_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_hedge_fund_info <err_msg> {e} from {HedgeFundInfo.__tablename__}')


    def get_hedge_fund_nav(self, fund_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    HedgeFundNAV,
                )
                if fund_id_list:
                    query = query.filter(
                        HedgeFundNAV.fund_id.in_(fund_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_hedge_fund_nav <err_msg> {e} from {HedgeFundNAV.__tablename__}')


    def delete_hedge_fund_nav(self, fund_id_to_delete: str, *, date_list: Tuple[datetime.date] = (), start_date: str = '', end_date: str = '') -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    HedgeFundNAV
                ).filter(
                    HedgeFundNAV.fund_id == fund_id_to_delete,
                )
                if date_list:
                    query = query.filter(
                        HedgeFundNAV.datetime.in_(date_list),
                    )
                if start_date:
                    query = query.filter(
                        HedgeFundNAV.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        HedgeFundNAV.datetime <= end_date,
                    )
                query.delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {HedgeFundNAV.__tablename__}')
                return False


    def get_fof_info(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFInfo,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFInfo.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_info <err_msg> {e} from {FOFInfo.__tablename__}')


    def get_fof_asset_allocation(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFAssetAllocation,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFAssetAllocation.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_asset_allocation <err_msg> {e} from {FOFAssetAllocation.__tablename__}')


    def get_fof_scale_alteration(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFScaleAlteration,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFScaleAlteration.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_scale_alteration <err_msg> {e} from {FOFScaleAlteration.__tablename__}')


    def get_fof_manually(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFManually,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFManually.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_manually <err_msg> {e} from {FOFManually.__tablename__}')

    def get_fof_other_record(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFOtherRecord,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFOtherRecord.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_manually <err_msg> {e} from {FOFOtherRecord.__tablename__}')

    def get_fof_account_statement(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFAccountStatement,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFAccountStatement.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_account_statement <err_msg> {e} from {FOFAccountStatement.__tablename__}')

    def delete_fof_account_statement(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFAccountStatement
                ).filter(
                    FOFAccountStatement.fof_id.in_(fof_id_list),
                    FOFAccountStatement.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFAccountStatement.__tablename__}')
                return False

    def get_fof_incidental_statement(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFIncidentalStatement,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFIncidentalStatement.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_incidental_statement <err_msg> {e} from {FOFIncidentalStatement.__tablename__}')

    def get_fof_investor_position(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFInvestorPosition,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFInvestorPosition.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_manually <err_msg> {e} from {FOFInvestorPosition.__tablename__}')

    def delete_fof_investor_position(self, fof_id_to_delete: datetime.date, investor_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFInvestorPosition
                ).filter(
                    FOFInvestorPosition.investor_id.in_(investor_id_list),
                    FOFInvestorPosition.fof_id == fof_id_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFInvestorPosition.__tablename__}')
                return False

    def get_fof_investor_position_summary(self, investor_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFInvestorPositionSummary,
                )
                if investor_id_list:
                    query = query.filter(
                        FOFInvestorPositionSummary.investor_id.in_(investor_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_investor_position_summary <err_msg> {e} from {FOFInvestorPositionSummary.__tablename__}')

    def delete_fof_investor_position_summary(self, investor_id_to_delete: str, datetime_list: List[datetime.date]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFInvestorPositionSummary
                ).filter(
                    FOFInvestorPositionSummary.datetime.in_(datetime_list),
                    FOFInvestorPositionSummary.investor_id == investor_id_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFInvestorPositionSummary.__tablename__}')

    def get_fof_estimate_fee(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFEstimateFee,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFEstimateFee.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_estimate_fee <err_msg> {e} from {FOFEstimateFee.__tablename__}')

    def delete_fof_estimate_fee(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFEstimateFee
                ).filter(
                    FOFEstimateFee.fof_id.in_(fof_id_list),
                    FOFEstimateFee.date == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFEstimateFee.__tablename__}')
                return False

    def get_fof_estimate_interest(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFEstimateInterest,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFEstimateInterest.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_estimate_interest <err_msg> {e} from {FOFEstimateInterest.__tablename__}')

    def delete_fof_estimate_interest(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFEstimateInterest
                ).filter(
                    FOFEstimateInterest.fof_id.in_(fof_id_list),
                    FOFEstimateInterest.date == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFEstimateInterest.__tablename__}')
                return False

    def get_fof_transit_money(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFTransitMoney,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFTransitMoney.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_transit_money <err_msg> {e} from {FOFTransitMoney.__tablename__}')

    def delete_fof_transit_money(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFTransitMoney
                ).filter(
                    FOFTransitMoney.fof_id.in_(fof_id_list),
                    FOFTransitMoney.confirmed_datetime == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFTransitMoney.__tablename__}')
                return False

    def get_asset_info(self, asset_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    AssetInfo,
                )
                if asset_id_list:
                    query = query.filter(
                        AssetInfo.asset_id.in_(asset_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_transit_money <err_msg> {e} from {AssetInfo.__tablename__}')

    def get_asset_info_real(self, real_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    AssetInfo,
                )
                if real_id_list:
                    query = query.filter(
                        AssetInfo.real_id.in_(real_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_transit_money <err_msg> {e} from {AssetInfo.__tablename__}')

    def get_asset_details(self):
        try:
            df = self.get_asset_info()
            asset_list = df.asset_type.unique().tolist()
            result = {}
            for asset_id in asset_list:
                result[asset_id] = []
                _df = df[df.asset_type == asset_id].drop_duplicates(subset=['asset_name'])
                for r in _df.itertuples():
                    result[asset_id].append([r.asset_id, r.asset_name])
            return result
        except Exception as e:
            print(f'failed to get_fof_transit_money <err_msg> {e} from {AssetInfo.__tablename__}')

    def get_product_details(self):
        try:
            df = self.get_asset_info()
            df1 = df[(df['asset_type'] == '典型产品')]
            asset_list = df1.asset_name.unique().tolist()
            result = {}
            for asset_id in asset_list:
                result[asset_id] = []
                _df = df1[df1.asset_name == asset_id]
                for r in _df.itertuples():
                    result[asset_id].append([r.real_id, r.real_name])
            df2 = df[df['asset_name'].isin(['商品','大盘股'])]
            asset_list = df2.asset_name.unique().tolist()
            dic = {'商品CFCI':'商品期货指数'}
            asset = '指数'
            result[asset] = []
            for r in df2.itertuples():
                result[asset].append([r.real_id, dic.get(r.real_name,r.real_name)])
            return result
        except Exception as e:
            print(f'failed to get_fof_transit_money <err_msg> {e} from {AssetInfo.__tablename__}')

    def get_asset_price(self, begin_date, end_date, time_para, asset_list: Tuple[str] = ()):
        try:
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            raw = RawDataApi()
            asset_info = self.get_asset_info(asset_id_list=asset_list)
            asset_list = asset_info.asset_id.tolist()
            _asset_list = [i for i in asset_list if i.split('-')[0] == 'fund']
            _res = []
            for r in asset_info.itertuples():
                if r.asset_id in _asset_list:
                    _res.append(r.real_name)
                else:
                    _res.append(r.asset_name)
            asset_info.loc[:,'show_name'] = _res
            inputs_asset_list = asset_info.asset_id.tolist()
            asset_dic = asset_info.set_index('asset_id').to_dict()['real_id']
            asset_list_0 = ['asset-dollar']
            asset_list_1 = ['asset-btc']
            asset_list_2 = ['asset-usdebt']
            _asset_list_0 = [i for i in inputs_asset_list if i in asset_list_0]
            _asset_list_1 = [i for i in inputs_asset_list if i in asset_list_1]
            _asset_list_2 = [i for i in inputs_asset_list if i in asset_list_2]
            _asset_list_3 = [i for i in inputs_asset_list if i.split('-')[0] == 'fund']
            _asset_list_4 = [i for i in inputs_asset_list if i.split('-')[0] == 'stgindex']
            _asset_sum = _asset_list_0 + _asset_list_1 + _asset_list_2 + _asset_list_3 + _asset_list_4
            _asset_list_5 = [i for i in inputs_asset_list if i not in _asset_sum]

            result = []
            if len(_asset_list_0) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_0]
                _df = raw.get_em_macroeconomic_daily(codes=real_ids,start_date=begin_date,end_date=end_date).pivot_table(index='datetime',columns='codes',values='value')
                result.append(_df)
            if len(_asset_list_1) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_1]
                _df = raw.get_btc(asset_ids=real_ids,start_date=begin_date,end_date=end_date).pivot_table(index='date',columns='codes',values='close')
                result.append(_df)
            if len(_asset_list_2) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_2]
                _df = raw.get_em_future_price(future_ids=real_ids,start_date=begin_date,end_date=end_date).pivot_table(index='datetime',columns='future_id',values='close')
                result.append(_df)
            if len(_asset_list_3) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_3]
                _df = raw.get_hf_fund_nav(fund_ids=real_ids,start_date=begin_date,end_date=end_date).pivot_table(index='datetime',columns='fund_id',values='nav')
                result.append(_df)
            if len(_asset_list_4) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_4]
                _df = raw.get_hf_index_price(index_ids=real_ids,start_date=begin_date,end_date=end_date).pivot_table(index='index_date',columns='index_id',values='close')
                result.append(_df)
            if len(_asset_list_5) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_5]
                _df = self.get_index_price_dt(index_list=real_ids,start_date=begin_date,end_date=end_date).pivot_table(index='datetime',columns='index_id',values='close')
                result.append(_df)

            df_result = pd.concat(result,axis=1).sort_index().ffill().dropna()
            df_result = df_result / df_result.iloc[0]
            df_result_show = df_result.rename(columns=asset_info.set_index('real_id').to_dict()['show_name'])
            df_result_real = df_result.rename(columns=asset_info.set_index('real_id').to_dict()['real_name'])
            asset_info = asset_info.drop_duplicates(subset=['real_id'])
            dic = {'data':df_result_show,'_input_asset_nav':df_result_real,'_input_asset_info':asset_info}
            return dic
        
        except Exception as e:
                print(f'failed to asset price <err_msg> {e} from basic.get_asset_price')

    def get_product_price(self, begin_date, end_date, time_para, product_list: Tuple[str] = (),):
        try:
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            raw = RawDataApi()
            asset_info = self.get_asset_info_real(real_id_list=product_list)
            asset_info = asset_info.drop_duplicates('real_id')
            asset_id_list = asset_info.asset_type.unique().tolist()
            name_dic = asset_info.set_index('real_id').to_dict()['real_name']
            asset_dic = {}
            for asset_id in asset_id_list:
                _df = asset_info[asset_info.asset_type == asset_id]
                asset_dic[asset_id] = _df.real_id.tolist()
            result = []
            if len(asset_dic['典型产品']) > 0:
                real_ids = asset_dic['典型产品']
                _df = raw.get_hf_fund_nav(fund_ids=real_ids,start_date=begin_date,end_date=end_date).pivot_table(index='datetime',columns='fund_id',values='nav')
                result.append(_df)
            if '大类资产' in asset_dic.keys():
                real_ids = asset_dic['大类资产']
                if len(real_ids) > 0:
                    _df = self.get_index_price_dt(start_date=begin_date,end_date=end_date,index_list=real_ids).pivot_table(index='datetime',columns='index_id',values='close')
                    result.append(_df)
                
            df_result = pd.concat(result,axis=1).sort_index().ffill().dropna()
            df_result = df_result / df_result.iloc[0]
            df_result = df_result.rename(columns=name_dic)
            dic = {'data':df_result,'_input_asset_nav':df_result,'_input_asset_info':asset_info}
            return dic
        
        except Exception as e:
                print(f'failed to asset price <err_msg> {e} from basic.get_product_price')

    def product_recent_rate(self, product_list, year:int=None):
        try:
            raw = RawDataApi()
            asset_info = self.get_asset_info_real(real_id_list=product_list)
            asset_info = asset_info.drop_duplicates('real_id')
            asset_id_list = asset_info.asset_type.unique().tolist()
            name_dic = asset_info.set_index('real_id').to_dict()['real_name']
            asset_dic = {}
            for asset_id in asset_id_list:
                _df = asset_info[asset_info.asset_type == asset_id]
                asset_dic[asset_id] = _df.real_id.tolist()
            result = []
            if len(asset_dic['典型产品']) > 0:
                real_ids = asset_dic['典型产品']
                _df = raw.get_hf_fund_nav(fund_ids=real_ids,start_date='20091231').pivot_table(index='datetime',columns='fund_id',values='nav')
                result.append(_df)
            if '大类资产' in asset_dic.keys():
                real_ids = asset_dic['大类资产']
                if len(real_ids) > 0:
                    _df = self.get_index_price_dt(start_date='20091231',index_list=real_ids).pivot_table(index='datetime',columns='index_id',values='close')
                    result.append(_df)
            index_price = pd.concat(result,axis=1).sort_index().ffill().dropna()
            if year is None:
                # 年度
                index_price_y = self.data_resample_monthly_nav(index_price.bfill(),rule='12M')
                index_ret_year = index_price_y.pct_change(1).dropna()
                td = index_ret_year.index
                td = [str(i.year) for i in td]
                index_ret = index_ret_year.copy()
            else:
                index_price_m = index_price.loc[datetime.date(year-1,12,31):datetime.date(year,12,31)]
                index_price_m = self.data_resample_monthly_nav(index_price_m,rule='1M').bfill()
                index_ret_m = index_price_m.pct_change(1).dropna()
                td = index_ret_m.index
                td = [str(i.year) + str(i.month).zfill(2) for i in td ]
                index_ret = index_ret_m.copy()
            index_ret.index = td
            index_ret.loc['均值',:] = index_ret.mean()
            index_ret = index_ret.round(4)*100
            index_ret = index_ret.rename(columns=name_dic)
            index_ret = index_ret.T
            index_ret.index.name = 'index_id'
            return index_ret
        except Exception as e:
                print(f'failed to asset price <err_msg> {e} from basic.get_product_recent_price')

    def data_resample_monthly_nav(self, df, rule='1M'):
        df = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule).last()
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        return df

    def asset_recent_rate(self, asset_list, year:int=None):
        #如果year为空 返回年度收益
        #如果year为整数 返回当年月度收益 year从2010开始
        try:
            raw = RawDataApi()
            asset_info = self.get_asset_info(asset_id_list=asset_list)
            asset_list = asset_info.asset_id.tolist()
            _asset_list = [i for i in asset_list if i.split('-')[0] == 'fund']
            _res = []
            for r in asset_info.itertuples():
                if r.asset_id in _asset_list:
                    _res.append(r.real_name)
                else:
                    _res.append(r.asset_name)
            asset_info.loc[:,'show_name'] = _res
            inputs_asset_list = asset_info.asset_id.tolist()
            asset_dic = asset_info.set_index('asset_id').to_dict()['real_id']
            name_dic = asset_info.set_index('real_id').to_dict()['real_name']
            name_dic = {k : v.replace('CFCI','指数')for k, v in name_dic.items()}
            asset_list_0 = ['asset-dollar']
            asset_list_1 = ['asset-btc']
            asset_list_2 = ['asset-usdebt']
            _asset_list_0 = [i for i in inputs_asset_list if i in asset_list_0]
            _asset_list_1 = [i for i in inputs_asset_list if i in asset_list_1]
            _asset_list_2 = [i for i in inputs_asset_list if i in asset_list_2]
            _asset_list_3 = [i for i in inputs_asset_list if i.split('-')[0] == 'fund']
            _asset_list_4 = [i for i in inputs_asset_list if i.split('-')[0] == 'stgindex']
            _asset_sum = _asset_list_0 + _asset_list_1 + _asset_list_2 + _asset_list_3 + _asset_list_4
            _asset_list_5 = [i for i in inputs_asset_list if i not in _asset_sum]

            result = []
            if len(_asset_list_0) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_0]
                _df = raw.get_em_macroeconomic_daily(codes=real_ids,start_date='20091231').pivot_table(index='datetime',columns='codes',values='value')
                result.append(_df)
            if len(_asset_list_1) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_1]
                _df = raw.get_btc(asset_ids=real_ids,start_date='20091231').pivot_table(index='date',columns='codes',values='close')
                result.append(_df)
            if len(_asset_list_2) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_2]
                _df = raw.get_em_future_price(future_ids=real_ids,start_date='20091231').pivot_table(index='datetime',columns='future_id',values='close')
                result.append(_df)
            if len(_asset_list_3) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_3]
                _df = raw.get_hf_fund_nav(fund_ids=real_ids,start_date='20091231').pivot_table(index='datetime',columns='fund_id',values='nav')
                result.append(_df)
            if len(_asset_list_4) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_4]
                _df = raw.get_hf_index_price(index_ids=real_ids,start_date='20091231').pivot_table(index='index_date',columns='index_id',values='close')
                result.append(_df)
            if len(_asset_list_5) > 0:
                real_ids = [asset_dic[i] for i in _asset_list_5]
                _df = self.get_index_price_dt(index_list=real_ids,start_date='20091231').pivot_table(index='datetime',columns='index_id',values='close')
                result.append(_df)

            index_price = pd.concat(result,axis=1).sort_index().ffill().dropna().rename(columns=name_dic)
            if year is None:
                # 年度
                index_price_y = self.data_resample_monthly_nav(index_price.bfill(),rule='12M')
                index_ret_year = index_price_y.pct_change(1).dropna()
                td = index_ret_year.index
                td = [str(i.year) for i in td]
                index_ret = index_ret_year.copy()
            else:
                index_price_m = index_price.loc[datetime.date(year-1,12,31):datetime.date(year,12,31)]
                index_price_m = self.data_resample_monthly_nav(index_price_m,rule='1M').bfill()
                index_ret_m = index_price_m.pct_change(1).dropna()
                td = index_ret_m.index
                td = [str(i.year) + str(i.month).zfill(2) for i in td ]
                index_ret = index_ret_m.copy()
            index_ret.index = td
            index_ret.loc['均值',:] = index_ret.mean()
            index_ret = index_ret.round(4)*100
            #index_ret = index_ret.rename(columns=desc_name_dic)
            index_ret = index_ret.T
            index_ret.index.name = 'index_id'
            return index_ret

        except Exception as e:
                print(f'failed to asset price <err_msg> {e} from basic.asset_recent_rate')
            
    def market_size_df(self,begin_date, end_date, time_para, codes=['cninfo_smallcap','cni_largec','cni_midcap']):
        try:
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            index_price = self.get_index_price_dt(start_date=begin_date,end_date=end_date,index_list=codes)
            index_info = self.get_index_info(codes)
            index_price = index_price.pivot_table(index='datetime',columns='index_id',values='close').dropna()
            dic = index_info.set_index('index_id').to_dict()['desc_name']
            index_price = index_price / index_price.iloc[0] - 1
            index_price = index_price.rename(columns=dic)
            index_price.index.name = 'datetime'
            return index_price

        except Exception as e:
                print(f'failed to asset price <err_msg> {e} from basic.market_size_df')

    def get_main_index_future_diff_yearly(self, begin_date, end_date, time_para, codes=['EMM00597141','EMM00597142','EMM00597143']):
        try:
            
            def is_third_friday(d):
                return d.weekday() == 4 and 15 <= d.day <= 21
            # 当月连续合约换仓天数
            def this_months_ex(x):
                return exchange_dts[exchange_dts >= x][0]
            # 下月连续合约换仓天数
            def next_months_ex(x):
                return exchange_dts[exchange_dts >= datetime.date(year=x.year,month=x.month,day=28)][0]
            # 下季度连续合约换仓天数
            def this_season_ex(x):
                return exchange_dts[(exchange_dts >= x) & ([i.month in [3,6,9,12] for i in exchange_dts])][1]

            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)

            # begin_date = max(begin_date, datetime.date(2020,1,1))
            codes = ['EMM00597141','EMM00597142','EMM00597143']
            df = RawDataApi().get_stock_index_future_diff_base(begin_date,end_date,codes)
            index_price = self.get_index_price_dt(start_date=begin_date,index_list=['csi500'])
            index_price = index_price.pivot_table(columns='index_id',values='close',index='datetime')
            df = df.join(index_price)
            for code_i in codes:
                df[code_i] = df[code_i] / df.csi500

            dt1 = [i for i in df.index if is_third_friday(i)]
            dt2 = []
            for i in range(200):
                _d = df.index.values[-1] + datetime.timedelta(i)
                if is_third_friday(_d):
                    dt2.append(_d)
            exchange_dts = np.array(dt1 + dt2)
            exchange_dts = np.array([i - datetime.timedelta(days=4) for i in exchange_dts])    
                
            df.loc[:,'当月连续剩余交易日'] = df.index.map(lambda x: (this_months_ex(x) - x).days + 4)
            df.loc[:,'下月连续剩余交易日'] = df.index.map(lambda x: (next_months_ex(x) - x).days + 4)
            df.loc[:,'下季连续剩余交易日'] = df.index.map(lambda x: (this_season_ex(x) - x).days + 4)

            df['EMM00597141'] = df['EMM00597141'] * 250 / df['当月连续剩余交易日']
            df['EMM00597142'] = df['EMM00597142'] * 250 / df['下月连续剩余交易日']
            df['EMM00597143'] = df['EMM00597143'] * 250 / df['下季连续剩余交易日']

            dic = {
                        'EMM00597141':'IC当月连续年化贴水率',
                        'EMM00597142':'IC下月连续年化贴水率',
                        'EMM00597143':'IC下季连续年化贴水率',
                    }
            df = df[codes].rename(columns=dic)
            df.index.name = 'datetime'
            return df

        except Exception as e:
                print(f'failed to asset price <err_msg> {e} from basic.get_main_index_future_diff_yearly')
    
    def get_industry_list(self):
        try:
            df = RawDataApi().get_em_industry_info(ind_class_type=1)[['em_id','ind_name']]
            em_id_list = df.em_id.to_list()
            df = self.get_index_info_by_em_id(em_id_list)
            info_list = [(r.index_id,r.desc_name.replace('(申万)','')) for r in df.itertuples()]
            return info_list
        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from get_em_industry_info')
            return []

    def get_industry_price(self, begin_date, end_date, time_para, industry_list):
        try:
            begin_date, end_date = RawDataApi().get_date_range(time_para, begin_date, end_date)
            df_info = self.get_index_info(industry_list)
            info_dic = {r.index_id : r.desc_name.replace('(申万)','') for r in df_info.itertuples()}
            df = self.get_index_price_dt(start_date=begin_date,end_date=end_date,index_list=industry_list)
            df = df.pivot_table(columns='index_id',values='close',index='datetime')
            df = df / df.iloc[0]
            df = df.rename(columns=info_dic)
            return df

        except Exception as e:
            print(f'Failed to get data <err_msg> {e} from get_industry_price')
            return pd.DataFrame([])

    def industry_recent_rate(self, industry_list, year:int=None):
        try:
            df_info = self.get_index_info(industry_list)
            desc_name_dic = {r.index_id : r.desc_name.replace('(申万)','') for r in df_info.itertuples()}
            index_price = self.get_index_price_dt(start_date='20091231',index_list=industry_list).pivot_table(index='datetime',columns='index_id',values='close')
            if year is None:
                # 年度
                index_price_y = self.data_resample_monthly_nav(index_price.bfill(),rule='12M')
                index_ret_year = index_price_y.pct_change(1).dropna()
                td = index_ret_year.index
                td = [str(i.year) for i in td]
                index_ret = index_ret_year.copy()
            else:
                index_price_m = index_price.loc[datetime.date(year-1,12,31):datetime.date(year,12,31)]
                index_price_m = self.data_resample_monthly_nav(index_price_m,rule='1M').bfill()
                index_ret_m = index_price_m.pct_change(1).dropna()
                td = index_ret_m.index
                td = [str(i.year) + str(i.month).zfill(2) for i in td ]
                index_ret = index_ret_m.copy()
            index_ret.index = td
            index_ret.loc['均值',:] = index_ret.mean()
            index_ret = index_ret.round(4)*100
            index_ret = index_ret.rename(columns=desc_name_dic)
            return index_ret.T
        except Exception as e:
                print(f'failed to asset price <err_msg> {e} from basic.get_industry_recent_ret')