import numpy as np
import pandas as pd
import math
from hbshare.rm_associated.util.verifier import verify_type
from hbshare.rm_associated.util.exception import InputParameterError, PreprocessError
from hbshare.rm_associated.util.logger import logger
from hbshare.rm_associated.util.data_loader import NavAttributionLoader
from hbshare.rm_associated.util.config import Q_MAP
from hbshare.rm_associated.util.regressions import Regression
from hbshare.rm_associated.util.nav_util import compute_annual_return_df, compute_annual_return
from hbshare.rm_associated.util.plot_util import draw_picture


class StyleAttributionOutputs:
    def __init__(self):
        self.attribution_df = None
        self.r_square = None

    def to_dict(self):
        return {
            "style_attribution": self.attribution_df.to_dict(orient='records'),
            "r_square": self.r_square
        }


class StyleAttribution:
    def __init__(self, fund_id, fund_type, start_date, end_date, factor_type, attribution_effort,
                 nav_frequency, annual_type, mode='online'):
        """
        :param fund_id: 基金代码
        :param fund_type: 基金类型, mutual：公募; private: 私募
        :param start_date: 归因的起始时间
        :param end_date: 归因的结束时间
        :param factor_type: 因子类型：分为风格配置/行业/风格三种
        :param attribution_effort: 归因的约束类型，对于风格配置的净值归因需要对暴露的范围进行约束： weak or hard
        :param nav_frequency: 基金的净值频率
        :param annual_type: 收益的年化方式
        :param mode: 是否使用本地数据计算, 'local':采用本地净值数据计算；'online':数据库数据
        """
        self.fund_id = fund_id
        self.fund_type = fund_type
        self.start_date = start_date
        self.end_date = end_date
        self.factor_type = factor_type
        self.attribution_effort = attribution_effort
        self.nav_frequency = nav_frequency
        self.annual_type = annual_type
        self.mode = mode
        self.calc_q = Q_MAP[self.nav_frequency]
        self._verify_input_param()
        self._load_data()
        self._init_style_attribution_data()

    def _verify_input_param(self):
        verify_type(self.fund_id, 'fund_id', str)
        verify_type(self.start_date, 'start_date', str)
        verify_type(self.end_date, 'end_date', str)
        if self.fund_type not in ['mutual', 'private']:
            msg = "fund_type not in ['mutual', 'private'], check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.factor_type not in ['style_allocation', 'industry', 'style']:
            msg = "factor_type not in ['style_allocation', 'industry', 'style']"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.attribution_effort not in ['weak', 'hard']:
            msg = "attribution_effort not in ['weak', 'hard']"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.nav_frequency not in ['day', 'week', 'month']:
            msg = "nav_frequency not supported, check your input"
            logger.error(msg)
            raise InputParameterError(message=msg)
        if self.annual_type not in ['arithmetic', 'linking', 'geometric']:
            msg = "annual_type not in ['arithmetic', 'linking', 'geometric']"
            logger.error(msg)
            raise InputParameterError(message=msg)

    def _load_data(self):
        data = NavAttributionLoader(
            self.fund_id, self.fund_type, self.start_date, self.end_date, self.factor_type).load()
        self.calendar_df = data['calendar_df']
        self.fund_adj_nav = data['fund_adj_nav']
        self.factor_data = data['factor_data']

        # 线下产品的example TODO
        if self.mode == 'local':
            adj_nav = pd.read_csv("D:\\kevin\\线下产品归因\\新方程泰暘净值.csv", index_col=0)
            adj_nav['tradeDate'] = adj_nav.index
            adj_nav['tradeDate'] = adj_nav['tradeDate'].map(str)
            self.fund_adj_nav = adj_nav.set_index('tradeDate')['nav'].loc[self.start_date: self.end_date]

    def get_trading_day_list(self):
        if self.nav_frequency == 'day':
            trading_day_list = sorted(list(self.calendar_df[self.calendar_df['isOpen'] == 1]['calendarDate']))
        elif self.nav_frequency == 'week':
            trading_day_list = sorted(list(self.calendar_df[self.calendar_df['isWeekEnd'] == 1]['calendarDate']))
        else:
            trading_day_list = sorted(list(self.calendar_df[self.calendar_df['isMonthEnd'] == 1]['calendarDate']))

        return trading_day_list

    def _init_style_attribution_data(self):
        all_date_list = sorted(list(self.calendar_df['calendarDate']))
        trading_day_list = self.get_trading_day_list()
        if not (self.fund_adj_nav.empty and self.factor_data.empty):
            try:
                self.portfolio_nav_series = self.fund_adj_nav.reindex(
                    all_date_list).interpolate().reindex(trading_day_list).dropna().sort_index()
                self.portfolio_nav_series = self.portfolio_nav_series / self.portfolio_nav_series[0]
                self.portfolio_return_series = self.portfolio_nav_series.pct_change().dropna()

                factor_nav_df = self.factor_data / self.factor_data.iloc[0]
                factor_nav_df = factor_nav_df.reindex(trading_day_list).fillna(method='ffill')
                self.factor_return_df = factor_nav_df.pct_change().dropna().reindex(
                    self.portfolio_return_series.index).fillna(0.)
                self.portfolio_return_series.sort_index(inplace=True)
                self.factor_return_df.sort_index(inplace=True)
            except Exception as e:
                raise PreprocessError(message=e.message)

    def __style_attribution(self):
        if self.portfolio_return_series.empty:
            return pd.Series(), np.nan

        if self.factor_return_df.empty:
            return pd.Series(), np.nan

        if self.factor_type == 'style_allocation':
            self.lower, self.upper = 0.0, 1.0
            self.strategy_method = 'ols'
        else:
            self.lower, self.upper = None, None
            self.strategy_method = 'ols'

        sr_obj = Regression(self.factor_return_df, self.portfolio_return_series,
                            upper=self.upper, lower=self.lower,
                            method=self.strategy_method, effort=self.attribution_effort)
        solve_dict = sr_obj.solve()
        factor_beta_series = solve_dict['solution']
        r_square = solve_dict['r_square']

        return factor_beta_series.dropna(), r_square

    @staticmethod
    def __process_attr_series_to_df(attr_series, type_name):
        attr_series.name = 'VALUE'
        attr_series.index.name = 'SECTOR_NAME'
        attr_df = attr_series.reset_index()
        attr_df.loc[:, 'ATTR_TYPE'] = type_name
        return attr_df

    def __perf_attr(self, account_return, factor_df, beta_series):
        calc_df = factor_df[beta_series.index.tolist()]

        idx = account_return.index.intersection(calc_df.index)
        calc_df = calc_df.loc[idx]
        account_return = account_return[idx]

        bm_annual_return = compute_annual_return_df(
            return_df_day_index=calc_df, calc_q=self.calc_q, annual_type=self.annual_type)

        bm_mean_ser = bm_annual_return
        bm_mean_ser.sort_index(inplace=True)
        beta_series.sort_index(inplace=True)

        perf_attr = beta_series.multiply(bm_mean_ser)
        common_factor_return = perf_attr.sum()

        account_annual_return = compute_annual_return(
            return_series=account_return, calc_q=self.calc_q, annual_type=self.annual_type)

        perf_attr.loc['SPECIFIC'] = account_annual_return - common_factor_return

        calc_trans = calc_df.T
        calc_trans.sort_index(inplace=True)
        calc_cov = np.cov(calc_trans.values)
        omega_arr = (np.matrix(calc_cov) * np.matrix(beta_series.values).T).A1

        var_attr = beta_series.values * omega_arr

        sigma = np.sqrt(np.sum(var_attr))

        risk_attr_arr = var_attr / sigma

        beta_risk = pd.Series(index=beta_series.index, data=risk_attr_arr)
        common_factor_risk = beta_risk.sum()
        beta_risk.loc['SPECIFIC'] = account_return.std() - common_factor_risk
        risk_annual_coef = math.sqrt(self.calc_q)
        beta_risk = beta_risk.multiply(risk_annual_coef)

        perf_df = self.__process_attr_series_to_df(perf_attr, 'annual_return')
        risk_df = self.__process_attr_series_to_df(beta_risk, 'annual_risk')
        exposure_df = self.__process_attr_series_to_df(beta_series, 'exposure')

        return pd.concat([perf_df, risk_df, exposure_df])

    def __compute_style_attribution(self):
        attribution_beta_series, r_square = self.__style_attribution()

        if attribution_beta_series.empty:
            logger.error('WARNING: %s' % "algorithm net value attribution warning: style beta is zero, "
                                         "maybe the y_data is vertical to x_data")
            return None, None

        attribution_account_df = self.__perf_attr(
            account_return=self.portfolio_return_series,
            factor_df=self.factor_return_df,
            beta_series=attribution_beta_series)

        return attribution_account_df, r_square

    def __style_analysis(self):
        if self.portfolio_return_series.empty:
            logger.warning("StyleAttribution self.portfolio_return_series is empty !")
            return pd.DataFrame(), np.nan

        if self.factor_return_df.empty:
            logger.warning("StyleAttribution self.factor_return_df is empty !")
            return pd.DataFrame(), np.nan

        attribution_df, r_square = self.__compute_style_attribution()

        return attribution_df, r_square

    def get_all(self, isPlot=False):
        output = StyleAttributionOutputs()

        attribution_df, r_square = self.__style_analysis()

        output.attribution_df = attribution_df.fillna(0.0)
        output.r_square = r_square

        if isPlot:
            df = pd.pivot_table(
                output.attribution_df, index='SECTOR_NAME', columns='ATTR_TYPE', values='VALUE').fillna(0.)
            df['annual_return'] *= 100

            df.to_csv("D:\\kevin\\线下产品归因\\泰暘_202004-202103.csv")

            bar = draw_picture(df, output.r_square)

            bar.render("D:\\kevin\\线下产品归因\\泰暘_202004-202103.html")

        return output.to_dict()


if __name__ == '__main__':
    # a = ['000311', '110011', '161005', '166002', '162605']

    # res = StyleAttribution(fund_id='110011', fund_type='mutual', start_date='20200101', end_date='20201231',
    #                        factor_type='style', attribution_effort='weak',
    #                        nav_frequency='day', annual_type='geometric').get_all()

    # fund_id_df = load_fund_id_from_db(0)
    #
    # from tqdm import tqdm
    #
    # for mutual_fund_id in tqdm(fund_id_df['JJDM'].unique().tolist()[:500]):
    #     res = StyleAttribution(fund_id=mutual_fund_id, fund_type='mutual', start_date='20200101', end_date='20201231',
    #                            factor_type='style', attribution_effort='weak',
    #                            nav_frequency='day', annual_type='geometric').get_all()
    #     print("基金名称: {}, 净值归因r2: {}".format(
    #         fund_id_df[fund_id_df['JJDM'] == mutual_fund_id]['JJMC'].values[0], res['r_square']))
    res = StyleAttribution(fund_id='P00107', fund_type='private', start_date='20200101', end_date='20210310',
                           factor_type='style', attribution_effort='weak',
                           nav_frequency='week', annual_type='geometric', mode='online').get_all()