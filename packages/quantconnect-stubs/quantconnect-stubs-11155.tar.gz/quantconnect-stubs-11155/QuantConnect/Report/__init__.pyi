import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm
import QuantConnect.Data
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.DataFeeds
import QuantConnect.Lean.Engine.Results
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Report
import QuantConnect.Securities
import System
import System.Collections.Generic

JsonConverter = typing.Any

QuantConnect_Report_NullResultValueTypeJsonConverter_T = typing.TypeVar("QuantConnect_Report_NullResultValueTypeJsonConverter_T")


class Report(System.Object):
    """Report class"""

    StatisticsFileName: str = "report-statistics.json"
    """File name for statistics"""

    def __init__(self, name: str, description: str, version: str, backtest: QuantConnect.Packets.BacktestResult, live: QuantConnect.Packets.LiveResult, pointInTimePortfolioDestination: str = None) -> None:
        """
        Create beautiful HTML and PDF Reports based on backtest and live data.
        
        :param name: Name of the strategy
        :param description: Description of the strategy
        :param version: Version number of the strategy
        :param backtest: Backtest result object
        :param live: Live result object
        :param pointInTimePortfolioDestination: Point in time portfolio json output base filename
        """
        ...

    def Compile(self, html: str, reportStatistics: str) -> None:
        """Compile the backtest data into a report"""
        ...


class DeedleUtil(System.Object):
    """Utility extension methods for Deedle series/frames"""

    @staticmethod
    def CumulativeSum(input: typing.Any) -> typing.Any:
        """
        Calculates the cumulative sum for the given series
        
        :param input: Series to calculate cumulative sum for
        :returns: Cumulative sum in series form.
        """
        ...

    @staticmethod
    def CumulativeProduct(input: typing.Any) -> typing.Any:
        """
        Calculates the cumulative product of the series. This is equal to the python pandas method: `df.cumprod()`
        
        :param input: Input series
        :returns: Cumulative product.
        """
        ...

    @staticmethod
    def CumulativeMax(input: typing.Any) -> typing.Any:
        """Calculates the cumulative max of the series. This is equal to the python pandas method: `df.cummax()`."""
        ...

    @staticmethod
    def PercentChange(input: typing.Any) -> typing.Any:
        """
        Calculates the percentage change from the previous value to the current
        
        :param input: Series to calculate percentage change for
        :returns: Percentage change in series form.
        """
        ...

    @staticmethod
    def CumulativeReturns(input: typing.Any) -> typing.Any:
        """
        Calculates the cumulative returns series of the given input equity curve
        
        :param input: Equity curve series
        :returns: Cumulative returns over time.
        """
        ...

    @staticmethod
    def TotalReturns(input: typing.Any) -> float:
        """
        Calculates the total returns over a period of time for the given input
        
        :param input: Equity curve series
        :returns: Total returns over time.
        """
        ...

    @staticmethod
    def DropSparseColumnsAll(frame: typing.Any) -> typing.Any:
        """
        Drops sparse columns only if every value is `missing` in the column
        
        :param frame: Data Frame
        :returns: new Frame with sparse columns dropped.
        """
        ...

    @staticmethod
    def DropSparseRowsAll(frame: typing.Any) -> typing.Any:
        """
        Drops sparse rows if and only if every value is `missing` in the Frame
        
        :param frame: Data Frame
        :returns: new Frame with sparse rows dropped.
        """
        ...


class CrisisEvent(System.Enum):
    """Crisis Events"""

    DotCom = 0
    """DotCom bubble - https://en.wikipedia.org/wiki/Dot-com_bubble"""

    SeptemberEleventh = 1
    """September 11, 2001 attacks - https://en.wikipedia.org/wiki/September_11_attacks"""

    USHousingBubble2003 = 2
    """United States housing bubble - https://en.wikipedia.org/wiki/United_States_housing_bubble"""

    GlobalFinancialCrisis = 3
    """https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%9308"""

    FlashCrash = 4
    """The flash crash of 2010 - https://en.wikipedia.org/wiki/2010_Flash_Crash"""

    FukushimaMeltdown = 5
    """Fukushima nuclear power plant meltdown - https://en.wikipedia.org/wiki/Fukushima_Daiichi_nuclear_disaster"""

    USDowngradeEuropeanDebt = 6
    """
    United States credit rating downgrade - https://en.wikipedia.org/wiki/United_States_federal_government_credit-rating_downgrades
    European debt crisis - https://en.wikipedia.org/wiki/European_debt_crisis
    """

    EurozoneSeptember2012 = 7
    """European debt crisis - https://en.wikipedia.org/wiki/European_debt_crisis"""

    EurozoneOctober2014 = 8
    """European debt crisis - https://en.wikipedia.org/wiki/European_debt_crisis"""

    MarketSellOff2015 = 9
    """2015-2016 market sell off https://en.wikipedia.org/wiki/2015%E2%80%9316_stock_market_selloff"""

    Recovery = 10
    """Crisis recovery (2010 - 2012)"""

    NewNormal = 11
    """2014 - 2019 market performance"""

    COVID19 = 12
    """COVID-19 pandemic market crash"""


class Crisis(System.Object):
    """Crisis events utility class"""

    Events: System.Collections.Generic.Dictionary[QuantConnect.Report.CrisisEvent, QuantConnect.Report.Crisis] = ...
    """Crisis events and pre-defined values"""

    @property
    def Start(self) -> datetime.datetime:
        """Start of the crisis event"""
        ...

    @property
    def End(self) -> datetime.datetime:
        """End of the crisis event"""
        ...

    @property
    def Name(self) -> str:
        """Name of the crisis"""
        ...

    def __init__(self, name: str, start: datetime.datetime, end: datetime.datetime) -> None:
        """
        Creates a new crisis instance with the given name and start/end date.
        
        :param name: Name of the crisis
        :param start: Start date of the crisis
        :param end: End date of the crisis
        """
        ...

    @staticmethod
    def FromCrisis(crisisEvent: QuantConnect.Report.CrisisEvent) -> QuantConnect.Report.Crisis:
        """
        Returns a pre-defined crisis event
        
        :param crisisEvent: Crisis Event
        :returns: Pre-defined crisis event.
        """
        ...

    @typing.overload
    def ToString(self) -> str:
        """Converts instance to string using the dates in the instance as start/end dates"""
        ...

    @typing.overload
    def ToString(self, start: datetime.datetime, end: datetime.datetime) -> str:
        """
        Converts instance to string using the provided dates
        
        :param start: Start date
        :param end: End date
        """
        ...


class Program(System.Object):
    """Lean Report creates a PDF strategy summary from the backtest and live json objects."""

    @staticmethod
    def Main(args: typing.List[str]) -> None:
        ...


class ResultsUtil(System.Object):
    """Utility methods for dealing with the Result objects"""

    @staticmethod
    def EquityPoints(result: QuantConnect.Result) -> System.Collections.Generic.SortedList[datetime.datetime, float]:
        """
        Get the equity chart points
        
        :param result: Result object to extract the chart points
        """
        ...

    @staticmethod
    def BenchmarkPoints(result: QuantConnect.Result) -> System.Collections.Generic.SortedList[datetime.datetime, float]:
        """
        Gets the points of the benchmark
        
        :param result: Backtesting or live results
        :returns: Sorted list keyed by date and value.
        """
        ...


class Rolling(System.Object):
    """Rolling window functions"""

    @staticmethod
    def Beta(equityCurve: typing.Any, benchmarkSeries: typing.Any, windowSize: int = 132) -> typing.Any:
        """
        Calculate the rolling beta with the given window size (in days)
        
        :param equityCurve: The equity curve you want to measure beta for
        :param benchmarkSeries: The benchmark/series you want to calculate beta with
        :param windowSize: Days/window to lookback
        :returns: Rolling beta.
        """
        ...

    @staticmethod
    def Sharpe(equityCurve: typing.Any, months: int, riskFreeRate: float = 0.0) -> typing.Any:
        """
        Get the rolling sharpe of the given series with a lookback of . The risk free rate is adjustable
        
        :param equityCurve: Equity curve to calculate rolling sharpe for
        :param months: Number of months to calculate the rolling period for
        :param riskFreeRate: Risk free rate
        :returns: Rolling sharpe ratio.
        """
        ...


class DrawdownPeriod(System.Object):
    """Represents a period of time where the drawdown ranks amongst the top N drawdowns."""

    @property
    def Start(self) -> datetime.datetime:
        """Start of the drawdown period"""
        ...

    @property
    def End(self) -> datetime.datetime:
        """End of the drawdown period"""
        ...

    @property
    def PeakToTrough(self) -> float:
        """Loss in percent from peak to trough"""
        ...

    @property
    def Drawdown(self) -> float:
        """Loss in percent from peak to trough - Alias for PeakToTrough"""
        ...

    def __init__(self, start: datetime.datetime, end: datetime.datetime, drawdown: float) -> None:
        """
        Creates an instance with the given start, end, and drawdown
        
        :param start: Start of the drawdown period
        :param end: End of the drawdown period
        :param drawdown: Max drawdown of the period
        """
        ...


class PointInTimePortfolio(System.Object):
    """Lightweight portfolio at a point in time"""

    class PointInTimeHolding(System.Object):
        """Holding of an asset at a point in time"""

        @property
        def Symbol(self) -> QuantConnect.Symbol:
            """Symbol of the holding"""
            ...

        @Symbol.setter
        def Symbol(self, value: QuantConnect.Symbol):
            """Symbol of the holding"""
            ...

        @property
        def HoldingsValue(self) -> float:
            """Value of the holdings of the asset. Can be negative if shorting an asset"""
            ...

        @HoldingsValue.setter
        def HoldingsValue(self, value: float):
            """Value of the holdings of the asset. Can be negative if shorting an asset"""
            ...

        @property
        def Quantity(self) -> float:
            """Quantity of the asset. Can be negative if shorting an asset"""
            ...

        @Quantity.setter
        def Quantity(self, value: float):
            """Quantity of the asset. Can be negative if shorting an asset"""
            ...

        @property
        def AbsoluteHoldingsValue(self) -> float:
            """Absolute value of the holdings."""
            ...

        @property
        def AbsoluteHoldingsQuantity(self) -> float:
            """Absolute value of the quantity"""
            ...

        def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], holdingsValue: float, holdingsQuantity: float) -> None:
            """
            Creates an instance of PointInTimeHolding, representing a holding at a given point in time
            
            :param symbol: Symbol of the holding
            :param holdingsValue: Value of the holding
            :param holdingsQuantity: Quantity of the holding
            """
            ...

    @property
    def Time(self) -> datetime.datetime:
        """Time that this point in time portfolio is for"""
        ...

    @Time.setter
    def Time(self, value: datetime.datetime):
        """Time that this point in time portfolio is for"""
        ...

    @property
    def TotalPortfolioValue(self) -> float:
        """The total value of the portfolio. This is cash + absolute value of holdings"""
        ...

    @TotalPortfolioValue.setter
    def TotalPortfolioValue(self, value: float):
        """The total value of the portfolio. This is cash + absolute value of holdings"""
        ...

    @property
    def Cash(self) -> float:
        """The cash the portfolio has"""
        ...

    @Cash.setter
    def Cash(self, value: float):
        """The cash the portfolio has"""
        ...

    @property
    def Order(self) -> QuantConnect.Orders.Order:
        """The order we just processed"""
        ...

    @Order.setter
    def Order(self, value: QuantConnect.Orders.Order):
        """The order we just processed"""
        ...

    @property
    def Holdings(self) -> System.Collections.Generic.List[QuantConnect.Report.PointInTimePortfolio.PointInTimeHolding]:
        """A list of holdings at the current moment in time"""
        ...

    @Holdings.setter
    def Holdings(self, value: System.Collections.Generic.List[QuantConnect.Report.PointInTimePortfolio.PointInTimeHolding]):
        """A list of holdings at the current moment in time"""
        ...

    @property
    def Leverage(self) -> float:
        """Portfolio leverage - provided for convenience"""
        ...

    @Leverage.setter
    def Leverage(self, value: float):
        """Portfolio leverage - provided for convenience"""
        ...

    @typing.overload
    def __init__(self, order: QuantConnect.Orders.Order, portfolio: QuantConnect.Securities.SecurityPortfolioManager) -> None:
        """
        Creates an instance of the PointInTimePortfolio object
        
        :param order: Order applied to the portfolio
        :param portfolio: Algorithm portfolio at a point in time
        """
        ...

    @typing.overload
    def __init__(self, portfolio: QuantConnect.Report.PointInTimePortfolio, time: datetime.datetime) -> None:
        """
        Clones the provided portfolio
        
        :param portfolio: Portfolio
        :param time: Time
        """
        ...

    def NoEmptyHoldings(self) -> QuantConnect.Report.PointInTimePortfolio:
        """
        Filters out any empty holdings from the current Holdings
        
        :returns: Current object, but without empty holdings.
        """
        ...


class Metrics(System.Object):
    """Strategy metrics collection such as usage of funds and asset allocations"""

    @staticmethod
    @typing.overload
    def LeverageUtilization(equityCurve: typing.Any, orders: System.Collections.Generic.List[QuantConnect.Orders.Order]) -> typing.Any:
        """
        Calculates the leverage used from trades. The series used to call this extension function should
        be the equity curve with the associated Order objects that go along with it.
        
        :param equityCurve: Equity curve series
        :param orders: Orders associated with the equity curve
        :returns: Leverage utilization over time.
        """
        ...

    @staticmethod
    @typing.overload
    def LeverageUtilization(portfolios: System.Collections.Generic.List[QuantConnect.Report.PointInTimePortfolio]) -> typing.Any:
        """
        Gets the leverage utilization from a list of PointInTimePortfolio
        
        :param portfolios: Point in time portfolios
        :returns: Series of leverage utilization.
        """
        ...

    @staticmethod
    @typing.overload
    def AssetAllocations(equityCurve: typing.Any, orders: System.Collections.Generic.List[QuantConnect.Orders.Order]) -> typing.Any:
        """
        Calculates the portfolio's asset allocation percentage over time. The series used to call this extension function should
        be the equity curve with the associated Order objects that go along with it.
        
        :param equityCurve: Equity curve series
        :param orders: Orders associated with the equity curve
        """
        ...

    @staticmethod
    @typing.overload
    def AssetAllocations(portfolios: System.Collections.Generic.List[QuantConnect.Report.PointInTimePortfolio]) -> typing.Any:
        """
        Calculates the asset allocation percentage over time.
        
        :param portfolios: Point in time portfolios
        :returns: Series keyed by Symbol containing the percentage allocated to that asset over time.
        """
        ...

    @staticmethod
    @typing.overload
    def Exposure(equityCurve: typing.Any, orders: System.Collections.Generic.List[QuantConnect.Orders.Order], direction: QuantConnect.Orders.OrderDirection) -> typing.Any:
        """
        Strategy long/short exposure by asset class
        
        :param equityCurve: Equity curve
        :param orders: Orders of the strategy
        :param direction: Long or short
        :returns: Frame keyed by SecurityType and OrderDirection. Returns a Frame of exposure per asset per direction over time.
        """
        ...

    @staticmethod
    @typing.overload
    def Exposure(portfolios: System.Collections.Generic.List[QuantConnect.Report.PointInTimePortfolio], direction: QuantConnect.Orders.OrderDirection) -> typing.Any:
        """
        Strategy long/short exposure by asset class
        
        :param portfolios: Point in time portfolios
        :param direction: Long or short
        :returns: Frame keyed by SecurityType and OrderDirection. Returns a Frame of exposure per asset per direction over time.
        """
        ...


class NullResultValueTypeJsonConverter(typing.Generic[QuantConnect_Report_NullResultValueTypeJsonConverter_T], JsonConverter):
    """
    Removes null values in the Result object's x,y values so that
    deserialization can occur without exceptions.
    """

    def __init__(self) -> None:
        """Initialize a new instance of NullResultValueTypeJsonConverter{T}"""
        ...

    def CanConvert(self, objectType: typing.Type) -> bool:
        """
        Determine if this converter can convert a given type
        
        :param objectType: Object type to convert
        :returns: Always true.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: typing.Type, existingValue: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Read Json for conversion
        
        :returns: Resulting object.
        """
        ...

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """Write Json; Not implemented"""
        ...


class OrderTypeNormalizingJsonConverter(JsonConverter):
    """
    Normalizes the "Type" field to a value that will allow for
    successful deserialization in the OrderJsonConverter class.
    """

    def CanConvert(self, objectType: typing.Type) -> bool:
        """
        Determine if this Converter can convert a given object type
        
        :param objectType: Object type to convert
        :returns: True if assignable from Order.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: typing.Type, existingValue: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Read Json and convert
        
        :returns: Resulting Order.
        """
        ...

    def WriteJson(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """Write Json; Not implemented"""
        ...


class DrawdownCollection(System.Object):
    """Collection of drawdowns for the given period marked by start and end date"""

    @property
    def Start(self) -> datetime.datetime:
        """Starting time of the drawdown collection"""
        ...

    @Start.setter
    def Start(self, value: datetime.datetime):
        """Starting time of the drawdown collection"""
        ...

    @property
    def End(self) -> datetime.datetime:
        """Ending time of the drawdown collection"""
        ...

    @End.setter
    def End(self, value: datetime.datetime):
        """Ending time of the drawdown collection"""
        ...

    @property
    def Periods(self) -> int:
        """
        Number of periods to take into consideration for the top N drawdown periods.
        This will be the number of items contained in the Drawdowns collection.
        """
        ...

    @Periods.setter
    def Periods(self, value: int):
        """
        Number of periods to take into consideration for the top N drawdown periods.
        This will be the number of items contained in the Drawdowns collection.
        """
        ...

    @property
    def Drawdowns(self) -> System.Collections.Generic.List[QuantConnect.Report.DrawdownPeriod]:
        """Worst drawdowns encountered"""
        ...

    @Drawdowns.setter
    def Drawdowns(self, value: System.Collections.Generic.List[QuantConnect.Report.DrawdownPeriod]):
        """Worst drawdowns encountered"""
        ...

    @typing.overload
    def __init__(self, periods: int) -> None:
        """Creates an instance with a default collection (no items) and the top N worst drawdowns"""
        ...

    @typing.overload
    def __init__(self, strategySeries: typing.Any, periods: int) -> None:
        """
        Creates an instance from the given drawdowns and the top N worst drawdowns
        
        :param strategySeries: Equity curve with both live and backtesting merged
        :param periods: Periods this collection contains
        """
        ...

    @staticmethod
    def FromResult(backtestResult: QuantConnect.Packets.BacktestResult = None, liveResult: QuantConnect.Packets.LiveResult = None, periods: int = 5) -> QuantConnect.Report.DrawdownCollection:
        """
        Generate a new instance of DrawdownCollection from backtest and live Result derived instances
        
        :param backtestResult: Backtest result packet
        :param liveResult: Live result packet
        :param periods: Top N drawdown periods to get
        :returns: DrawdownCollection instance.
        """
        ...

    @staticmethod
    def NormalizeResults(backtestResult: QuantConnect.Packets.BacktestResult, liveResult: QuantConnect.Packets.LiveResult) -> typing.Any:
        """
        Normalizes the Series used to calculate the drawdown plots and charts
        
        :param backtestResult: Backtest result packet
        :param liveResult: Live result packet
        """
        ...

    @staticmethod
    def GetUnderwater(curve: typing.Any) -> typing.Any:
        """
        Gets the underwater plot for the provided curve.
        Data is expected to be the concatenated output of ResultsUtil.EquityPoints.
        
        :param curve: Equity curve
        """
        ...

    @staticmethod
    def GetUnderwaterFrame(curve: typing.Any) -> typing.Any:
        """
        Gets all the data associated with the underwater plot and everything used to generate it.
        Note that you should instead use GetUnderwater(Series{DateTime, double}) if you
        want to just generate an underwater plot. This is internally used to get the top N worst drawdown periods.
        
        :param curve: Equity curve
        :returns: Frame containing the following keys: "returns", "cumulativeMax", "drawdown".
        """
        ...

    @staticmethod
    def GetTopWorstDrawdowns(curve: typing.Any, periods: int) -> typing.Any:
        """
        Gets the top N worst drawdowns and associated statistics.
        Returns a Frame with the following keys: "duration", "cumulativeMax", "drawdown"
        
        :param curve: Equity curve
        :param periods: Top N worst periods. If this is greater than the results, we retrieve all the items instead
        :returns: Frame with the following keys: "duration", "cumulativeMax", "drawdown".
        """
        ...

    @staticmethod
    def GetDrawdownPeriods(curve: typing.Any, periods: int = 5) -> System.Collections.Generic.IEnumerable[QuantConnect.Report.DrawdownPeriod]:
        """
        Gets the given drawdown periods from the equity curve and the set periods
        
        :param curve: Equity curve
        :param periods: Top N drawdown periods to get
        :returns: Enumerable of DrawdownPeriod.
        """
        ...


class PortfolioLooperAlgorithm(QuantConnect.Algorithm.QCAlgorithm):
    """Fake algorithm that initializes portfolio and algorithm securities. Never ran."""

    def __init__(self, startingCash: float, orders: System.Collections.Generic.IEnumerable[QuantConnect.Orders.Order]) -> None:
        """
        Initialize an instance of PortfolioLooperAlgorithm
        
        :param startingCash: Starting algorithm cash
        :param orders: Orders to use
        """
        ...

    def FromOrders(self, orders: System.Collections.Generic.IEnumerable[QuantConnect.Orders.Order]) -> None:
        """
        Initializes all the proper Securities from the orders provided by the user
        
        :param orders: Orders to use
        """
        ...

    def Initialize(self) -> None:
        """Initialize this algorithm"""
        ...


class PortfolioLooper(System.Object, System.IDisposable):
    """
    Runs LEAN to calculate the portfolio at a given time from Order objects.
    Generates and returns PointInTimePortfolio objects that represents
    the holdings and other miscellaneous metrics at a point in time by reprocessing the orders
    as they were filled.
    """

    @property
    def Algorithm(self) -> QuantConnect.Report.PortfolioLooperAlgorithm:
        """
        QCAlgorithm derived class that sets up internal data feeds for
        use with crypto and forex data, as well as managing the SecurityPortfolioManager
        """
        ...

    @Algorithm.setter
    def Algorithm(self, value: QuantConnect.Report.PortfolioLooperAlgorithm):
        """
        QCAlgorithm derived class that sets up internal data feeds for
        use with crypto and forex data, as well as managing the SecurityPortfolioManager
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    @staticmethod
    def GetHistory(symbols: System.Collections.Generic.List[QuantConnect.Symbol], start: datetime.datetime, end: datetime.datetime, resolution: QuantConnect.Resolution) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]:
        """
        Gets the history for the given symbols from the  to the
        
        :param symbols: Symbols to request history for
        :param start: Start date of history request
        :param end: End date of history request
        :param resolution: Resolution of history request
        :returns: Enumerable of slices.
        """
        ...

    @staticmethod
    def FromOrders(equityCurve: typing.Any, orders: System.Collections.Generic.IEnumerable[QuantConnect.Orders.Order], liveSeries: bool = False) -> System.Collections.Generic.IEnumerable[QuantConnect.Report.PointInTimePortfolio]:
        """
        Gets the point in time portfolio over multiple deployments
        
        :param equityCurve: Equity curve series
        :param orders: Orders
        :param liveSeries: Equity curve series originates from LiveResult
        :returns: Enumerable of PointInTimePortfolio.
        """
        ...


class MockDataFeed(System.Object, QuantConnect.Lean.Engine.DataFeeds.IDataFeed):
    """Fake IDataFeed"""

    @property
    def IsActive(self) -> bool:
        """Bool if the feed is active"""
        ...

    def Initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm, job: QuantConnect.Packets.AlgorithmNodePacket, resultHandler: QuantConnect.Lean.Engine.Results.IResultHandler, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider, factorFileProvider: QuantConnect.Interfaces.IFactorFileProvider, dataProvider: QuantConnect.Interfaces.IDataProvider, subscriptionManager: QuantConnect.Lean.Engine.DataFeeds.IDataFeedSubscriptionManager, dataFeedTimeProvider: QuantConnect.Lean.Engine.DataFeeds.IDataFeedTimeProvider, channelProvider: QuantConnect.Interfaces.IDataChannelProvider) -> None:
        """
        Initialize the data feed
        This implementation does nothing
        """
        ...

    def CreateSubscription(self, request: QuantConnect.Data.UniverseSelection.SubscriptionRequest) -> QuantConnect.Lean.Engine.DataFeeds.Subscription:
        """
        Create Subscription
        
        :param request: Subscription request to use
        :returns: Always null.
        """
        ...

    def RemoveSubscription(self, subscription: QuantConnect.Lean.Engine.DataFeeds.Subscription) -> None:
        """
        Remove Subscription; Not implemented
        
        :param subscription: Subscription to remove
        """
        ...

    def Exit(self) -> None:
        """DataFeed Exit"""
        ...


