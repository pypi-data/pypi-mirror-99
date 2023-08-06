

from typing import Optional, List
import re
import datetime
import os
import traceback
import time

import pandas as pd

from ...util.mail_retriever import MailAttachmentRetriever, IMAP_SPType, UID_FILE_NAME
from ...util.wechat_bot import WechatBot
from ..wrapper.mysql import BasicDatabaseConnector
from ..view.basic_models import HedgeFundNAV
from ..api.basic import BasicDataApi


class HedgeFundNAVReader:

    COLUMNS_DICT = {
        '基金代码': 'fund_id',
        '产品代码': 'fund_id',
        '基金名称': 'fund_name',
        '产品名称': 'fund_name',
        '基金份额净值': 'net_asset_value',
        '单位净值': 'net_asset_value',
        '计提前单位净值': 'net_asset_value',
        '基金份额累计净值': 'acc_unit_value',
        '累计单位净值': 'acc_unit_value',
        '累计净值': 'acc_unit_value',
        '虚拟后净值': 'v_net_value',
        '虚拟净值': 'v_net_value',
        '计提后单位净值': 'v_net_value',
        '虚拟计提净值': 'v_net_value',
        '虚拟后单位净值': 'v_net_value',
        '复权累计净值': 'adjusted_net_value',
        '复权净值': 'adjusted_net_value',
        '净值(分红再投)': 'adjusted_net_value',
        '日期': 'datetime',
        '净值日期': 'datetime',
        '业务日期': 'datetime',
        '计算日期': 'calc_date',
    }

    def __init__(self, read_dir: str, user_name: str, password: str):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        self._read_dir = read_dir
        assert os.path.isdir(self._read_dir), f'arg dump_dir should be a directory (now){self._read_dir}'

        self._user_name = user_name
        self._password = password
        self._wechat_bot = WechatBot()

    @staticmethod
    def _read_for_HuaChengZhiYuanNo3WithoutV(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path, header=None)
        df.iloc[:, 0] = df.iloc[:, 0].map(lambda x: x.split('：')[0])
        df = df.set_index(df.columns[0])
        pat = r'\d+'
        date = re.findall(pat, df.index.array[2])
        df = df.T.loc[:, ['基金代码', '基金名称', '基金份额净值', '基金份额累计净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT).assign(datetime=pd.to_datetime('-'.join(date), infer_datetime_format=True).date())
        return df

    @staticmethod
    def _read_for_HuaChengZhiYuanNo3(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品代码', '产品名称', '业务日期', '单位净值', '累计单位净值', '虚拟后净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        df['datetime'] = pd.to_datetime(df.datetime.astype(str), infer_datetime_format=True).dt.date
        return df

    @staticmethod
    def _read_for_TianYanGuangQuanWithoutV(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '净值日期', '单位净值', '累计单位净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_TianYanGuangQuan(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path, skipfooter=1)
        df = df.loc[:, ['基金名称', '基金代码', '净值日期', '计算日期', '单位净值', '累计单位净值', '虚拟净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_AnXianHuaMuChangSheng(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '日期', '单位净值', '累计单位净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        df = df.replace({'S3ZS26': 'SJE335'})
        df['datetime'] = df.datetime.transform(lambda x: pd.to_datetime(str(x), infer_datetime_format=True).date())
        return df

    @staticmethod
    def _read_for_WuZhiCTA1(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '净值日期', '计提前单位净值', '累计单位净值', '计提后单位净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_WuZhiCTA1WithoutV(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '日期', '单位净值', '累计单位净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_XinPu10(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '业务日期', '单位净值', '累计单位净值', '虚拟后净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        df['datetime'] = df.datetime.transform(lambda x: pd.to_datetime(str(x), infer_datetime_format=True).date())
        return df

    @staticmethod
    def _read_for_TaiChuangXiShuoCTA(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path, index_col=0, skiprows=3, usecols=[0, 1])
        dates_data = df.index.name.split('：')
        assert (len(dates_data) >= 2) and (dates_data[0] == '日期'), 'invalid format from TaiChuangXiShuoCTA'
        df = df.loc[['单位净值', '累计单位净值'], :].T
        df['datetime'] = pd.to_datetime(str(dates_data[1]), infer_datetime_format=True).date()
        df['fund_id'] = 'SNH765'
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_TaiChuangXiShuoCTANormalWithPrism(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '业务日期', '单位净值', '累计单位净值', '虚拟后净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        df['datetime'] = df.datetime.transform(lambda x: pd.to_datetime(str(x), infer_datetime_format=True).date())
        return df

    @staticmethod
    def _read_for_TaiChuangXiShuoCTANormal(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '业务日期', '单位净值', '累计单位净值', '虚拟计提净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        df['datetime'] = df.datetime.transform(lambda x: pd.to_datetime(str(x), infer_datetime_format=True).date())
        return df

    @staticmethod
    def _read_for_BoPu6(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '业务日期', '单位净值', '累计单位净值', '虚拟后净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        df['datetime'] = df.datetime.transform(lambda x: pd.to_datetime(str(x), infer_datetime_format=True).date())
        return df

    @staticmethod
    def _read_for_BoPu6WithoutV(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path, header=None)
        df.iloc[:, 0] = df.iloc[:, 0].map(lambda x: x.split('：')[0])
        df = df.set_index(df.columns[0])
        pat = r'\d+'
        date = re.findall(pat, df.index.array[2])
        df = df.T.loc[:, ['基金代码', '基金名称', '基金份额净值', '基金份额累计净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT).assign(datetime=pd.to_datetime('-'.join(date), infer_datetime_format=True).date())
        return df

    @staticmethod
    def _read_for_YuanHui1(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '业务日期', '单位净值', '累计单位净值', '虚拟后单位净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        return df

    @staticmethod
    def _read_for_ZhuoShiJiaXin(file_path: str) -> pd.DataFrame:
        df = pd.read_excel(file_path)
        df = df.loc[:, ['产品名称', '产品代码', '业务日期', '单位净值', '累计单位净值', '虚拟后净值']]
        df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
        df['datetime'] = df.datetime.transform(lambda x: pd.to_datetime(str(x), infer_datetime_format=True).date())
        return df

    def _notify_error_event(self, err_msg: str):
        print(f'[read_navs_and_dump_to_db] {err_msg}')
        self._wechat_bot.send_hedge_fund_nav_update_failed(err_msg)

    def read_navs_and_dump_to_db(self):
        try:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'rb') as f:
                uid_last = f.read()
                if not uid_last:
                    uid_last = None
        except Exception as e:
            self._notify_error_event(f'read uid file failed (e){e}, use None instead(read all emails)')
            uid_last = None

        try:
            mar = MailAttachmentRetriever(self._read_dir)
            data = mar.get_excels(IMAP_SPType.IMAP_QQ, self._user_name, self._password, uid_last)
        except Exception as e:
            self._notify_error_event(f'FATAL ERROR!! get new data of hedge fund nav failed (e){e}')
            return

        uid_last_succeed: Optional[bytes] = None
        df_list: List[pd.DataFrame] = []
        for name, comp_date in data.items():
            uid, file_path = comp_date
            if '.xls' not in name and '.xlsx' not in name:
                self._notify_error_event(f'not a valid file, do not process it (name){name} (file_path){file_path}')
                continue

            try:
                if 'SGM473' in name:
                    df = HedgeFundNAVReader._read_for_HuaChengZhiYuanNo3WithoutV(file_path)
                elif '华澄致远三号' in name:
                    df = HedgeFundNAVReader._read_for_HuaChengZhiYuanNo3(file_path)
                elif 'SLC213_天演广全' in name:
                    df = HedgeFundNAVReader._read_for_TianYanGuangQuanWithoutV(file_path)
                elif '天演广全' in name:
                    df = HedgeFundNAVReader._read_for_TianYanGuangQuan(file_path)
                elif '安贤花木长盛' in name:
                    df = HedgeFundNAVReader._read_for_AnXianHuaMuChangSheng(file_path)
                elif '吾执CTA一号' in name:
                    df = HedgeFundNAVReader._read_for_WuZhiCTA1(file_path)
                elif '产品净值情况' in name:
                    df = HedgeFundNAVReader._read_for_WuZhiCTA1WithoutV(file_path)
                elif '信朴10号私募基金' in name:
                    df = HedgeFundNAVReader._read_for_XinPu10(file_path)
                elif 'SNH765泰创-羲朔CTA' in name:
                    df = HedgeFundNAVReader._read_for_TaiChuangXiShuoCTA(file_path)
                elif '泰创-羲朔CTA' in name:
                    if '棱镜' in name:
                        df = HedgeFundNAVReader._read_for_TaiChuangXiShuoCTANormalWithPrism(file_path)
                    else:
                        df = HedgeFundNAVReader._read_for_TaiChuangXiShuoCTANormal(file_path)
                elif '博普量化对冲6号' in name:
                    df = HedgeFundNAVReader._read_for_BoPu6(file_path)
                elif 'SEE891-发送每日净值' in name:
                    df = HedgeFundNAVReader._read_for_BoPu6WithoutV(file_path)
                elif '源晖量化一号' in name:
                    df = HedgeFundNAVReader._read_for_YuanHui1(file_path)
                elif '卓识佳鑫' in name:
                    df = HedgeFundNAVReader._read_for_ZhuoShiJiaXin(file_path)
                else:
                    raise NotImplementedError('unknown hedge fund nav file from attachment')
            except Exception as e:
                self._notify_error_event(f'{e} (parse) (name){name} (file_path){file_path}')
                continue

            try:
                df = df.drop(columns=['fund_name'], errors='ignore')
                df['insert_time'] = datetime.datetime.now()
                df = self._dump_to_db(df)
                if df is not None:
                    df_list.append(df)
                else:
                    print(f'[read_navs_and_dump_to_db] duplicated data, do not process it (name){name}')
                # 走到这里都认为是已经处理完了这条数据
                uid_last_succeed = uid
                time.sleep(1)
            except Exception as e:
                traceback.print_exc()
                self._notify_error_event(f'{e} (dump) (name){name} (file_path){file_path}')
                continue

        if df_list:
            try:
                whole_df = pd.concat(df_list).set_index('fund_id')
                print(whole_df)
            except Exception as e:
                self._notify_error_event(f'{e} (concat)')
                return
            else:
                # self._wechat_bot.send_hedge_fund_nav_update(whole_df)
                print(f'[read_navs_and_dump_to_db] done (uid_last){uid_last_succeed} (df){whole_df}')
        else:
            whole_df = None
            print(f'[read_navs_and_dump_to_db] no new data this time, done (uid_last){uid_last_succeed}')
        # 记录下成功的最后一个uid
        if uid_last_succeed is not None:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'wb') as f:
                f.write(uid_last_succeed)
            return whole_df
        return

    def _dump_to_db(self, df: pd.DataFrame):
        def _check_after_merged(x: pd.Series, now_df: pd.DataFrame):
            try:
                now_data = now_df[(now_df.fund_id == x.fund_id) & (now_df.datetime == x.datetime)]
                if now_data[['net_asset_value', 'acc_unit_value', 'v_net_value']].iloc[0].astype('float64').equals(x[['net_asset_value', 'acc_unit_value', 'v_net_value']].astype('float64')):
                    return pd.Series(dtype='object')
                else:
                    return x
            except (KeyError, IndexError):
                return x

        assert df.datetime.nunique() == 1, 'should have single datetime'
        now_df = BasicDataApi().get_hedge_fund_nav(fund_id_list=list(df.fund_id.unique()))
        if now_df is not None and not now_df.empty:
            # 同产品同日期的净值如果已经存在了且没有变化，就不写DB了
            now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted', 'change_rate']).sort_values(by=['fund_id', 'datetime']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')
            now_df = now_df.astype({'net_asset_value': 'float64', 'acc_unit_value': 'float64', 'v_net_value': 'float64'})
            df = df.reindex(columns=now_df.columns).astype(now_df.dtypes.to_dict())
            df = df.merge(now_df, how='left', on=['fund_id', 'datetime', 'net_asset_value', 'acc_unit_value', 'v_net_value'], indicator=True, validate='one_to_one')
            df = df[df._merge == 'left_only'].drop(columns=['_merge', 'insert_time_y', 'calc_date_y', 'adjusted_net_value_y', 'ta_factor_y']).rename(columns={'insert_time_x': 'insert_time', 'calc_date_x': 'calc_date', 'adjusted_net_value_x': 'adjusted_net_value', 'ta_factor_x': 'ta_factor'})
            if df.empty:
                return
            # FIXME 没想到特别好的方法 遍历每一行再check一下
            df['datetime'] = pd.to_datetime(df.datetime, infer_datetime_format=True).dt.date
            df = df.apply(_check_after_merged, axis=1, now_df=now_df)
            if df.empty:
                return
            df['insert_time'] = df.insert_time.map(lambda x: x.to_pydatetime())
            print(df)
            df.update(now_df, overwrite=False)
            print(df)
            # 先删后添
            for fund_id in df.fund_id.unique():
                BasicDataApi().delete_hedge_fund_nav(fund_id_to_delete=fund_id, date_list=df[df.fund_id == fund_id].datetime.to_list())
        df.to_sql(HedgeFundNAV.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
        return df


if __name__ == '__main__':
    try:
        email_data_dir = os.environ['SURFING_EMAIL_DATA_DIR']
        user_name = os.environ['SURFING_EMAIL_USER_NAME']
        password = os.environ['SURFING_EMAIL_PASSWORD']
    except KeyError as e:
        import sys
        sys.exit(f'can not found enough params in env (e){e}')

    hf_nav_r = HedgeFundNAVReader(email_data_dir, user_name, password)
    hf_nav_r.read_navs_and_dump_to_db()
