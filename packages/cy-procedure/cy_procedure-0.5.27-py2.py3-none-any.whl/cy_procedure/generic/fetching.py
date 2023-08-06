from enum import IntEnum
from datetime import datetime
from cy_components.helpers.formatter import DateFormatter
from cy_widgets.fetcher.exchange import *


class ExchangeFetchingType(IntEnum):
    HISTORICAL = 0,     # Historical candle data, from earliest date do backward fetching
    FILL_RECENTLY = 1,  # Fill data recently
    CHECK_MISSING = 2,  # NOT IMPLEMENTED. Check missing candle
    TRADING = 3,        # NOT IMPLEMENTED. For trading


class ExchangeFetchingConfiguration:
    """ 抓取过程需要的配置参数
    1. CoinPair;
    2. Operation Type;
    3. TimeFrame;
    4. Begin date;
    5. Fetching duration (Sleep after a fetching operation)
    6. fetching_by_ccxt
    """

    def __init__(self,
                 coin_pair=None,
                 time_frame=TimeFrame.Minute_5,
                 sleep_duration=5,
                 begin_date=datetime.now(),
                 op_type=ExchangeFetchingType.HISTORICAL,
                 fetching_by_ccxt=True,
                 debug=False):
        super().__init__()
        assert coin_pair is not None
        assert time_frame is not None
        assert sleep_duration >= 3

        self.coin_pair = coin_pair
        self.time_frame = time_frame
        self.begin_date = begin_date
        self.op_type = op_type
        self.sleep_duration = sleep_duration
        self.fetching_by_ccxt = fetching_by_ccxt
        self.debug = debug


class ExchangeFetchingProcedure:
    """抓取数据的一般流程"""

    batch_limit = 1000

    def __init__(self,
                 fetcher: ExchangeFetcher,
                 configuration: ExchangeFetchingConfiguration,
                 get_earliest_date,
                 get_latest_date,
                 save_df):
        """初始化

        Parameters
        ----------
        fetcher : ExchangeFetcher
            抓取K线对象
        configuration : ExchangeFetchingConfiguration
            抓取配置
        get_earliest_date : () -> Date
            获取最早K线的日期
        get_latest_date : () -> Date
            获取最近K线的日期
        save_df : (df) -> Bool
            保存K线数据，返回是否继续抓取
        """
        assert fetcher is not None
        assert configuration is not None
        assert get_earliest_date is not None
        assert get_latest_date is not None
        assert save_df is not None

        self.fetcher = fetcher
        self.configuration = configuration

        self.get_earliest_date = get_earliest_date
        self.get_latest_date = get_latest_date
        self.save_df = save_df

    # Data

    def __perform_fetching(self, since_ts):
        """fetching + saving"""
        # Fetch
        df = self.fetcher.fetch_historical_candle_data(
            self.configuration.coin_pair,
            self.configuration.time_frame,
            since_ts,
            self.batch_limit,
            by_ccxt=self.configuration.fetching_by_ccxt)
        return self.save_df(df)

    # Task

    def __fetch_historical_data(self):
        """获取历史记录"""
        while True:
            # 获取最早的日期
            earliest_date = self.get_earliest_date()
            # 转为时间戳
            earliest_ts = DateFormatter.convert_local_date_to_timestamp(earliest_date)
            # 确定抓取的起始时间戳
            since_ts = self.configuration.time_frame.timestamp_backward_offset(earliest_ts, self.batch_limit)
            # 需要继续的，暂停一会儿
            if self.__perform_fetching(since_ts):
                time.sleep(self.configuration.sleep_duration)
            else:
                print('Historical.finished')
                return

    def __fill_recently(self):
        """补齐最近的数据"""
        while True:
            # 获取已经保存的最新的日期
            recent_date = self.get_latest_date()
            # 转换到时间戳
            recent_ts = DateFormatter.convert_local_date_to_timestamp(recent_date)
            # 往前移动10个单位作为起始日期
            since_ts = self.configuration.time_frame.timestamp_backward_offset(recent_ts, 10)
            # 需要继续的，暂停一会儿
            if self.__perform_fetching(since_ts):
                time.sleep(self.configuration.sleep_duration)
            else:
                print('FillRecently.finished')
                return

    def run_task(self):
        """Dispatch task"""
        if self.configuration.op_type == ExchangeFetchingType.HISTORICAL:
            self.__fetch_historical_data()
        elif self.configuration.op_type == ExchangeFetchingType.FILL_RECENTLY:
            self.__fill_recently()
