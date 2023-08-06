import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm
import QuantConnect.Algorithm.Framework
import QuantConnect.Algorithm.Framework.Alphas
import QuantConnect.Algorithm.Framework.Portfolio
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Scheduling
import QuantConnect.Securities
import System
import System.Collections
import System.Collections.Generic

LinearConstraint = typing.Any


class IPortfolioOptimizer(metaclass=abc.ABCMeta):
    """Interface for portfolio optimization algorithms"""

    def Optimize(self, historicalReturns: typing.List[float], expectedReturns: typing.List[float] = None, covariance: typing.List[float] = None) -> typing.List[float]:
        """
        Perform portfolio optimization for a provided matrix of historical returns and an array of expected returns
        
        :param historicalReturns: Matrix of annualized historical returns where each column represents a security and each row returns for the given date/time (size: K x N).
        :param expectedReturns: Array of double with the portfolio annualized expected returns (size: K x 1).
        :param covariance: Multi-dimensional array of double with the portfolio covariance of annualized returns (size: K x K).
        :returns: Array of double with the portfolio weights (size: K x 1).
        """
        ...


class UnconstrainedMeanVariancePortfolioOptimizer(System.Object, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer):
    """Provides an implementation of a portfolio optimizer with unconstrained mean variance."""

    def Optimize(self, historicalReturns: typing.List[float], expectedReturns: typing.List[float] = None, covariance: typing.List[float] = None) -> typing.List[float]:
        """
        Perform portfolio optimization for a provided matrix of historical returns and an array of expected returns
        
        :param historicalReturns: Matrix of annualized historical returns where each column represents a security and each row returns for the given date/time (size: K x N).
        :param expectedReturns: Array of double with the portfolio annualized expected returns (size: K x 1).
        :param covariance: Multi-dimensional array of double with the portfolio covariance of annualized returns (size: K x K).
        :returns: Array of double with the portfolio weights (size: K x 1).
        """
        ...


class IPortfolioTarget(metaclass=abc.ABCMeta):
    """
    Represents a portfolio target. This may be a percentage of total portfolio value
    or it may be a fixed number of shares.
    """

    @property
    @abc.abstractmethod
    def Symbol(self) -> QuantConnect.Symbol:
        """Gets the symbol of this target"""
        ...

    @property
    @abc.abstractmethod
    def Quantity(self) -> float:
        """Gets the quantity of this symbol the algorithm should hold"""
        ...


class IPortfolioConstructionModel(QuantConnect.Algorithm.Framework.INotifiedSecurityChanges, metaclass=abc.ABCMeta):
    """Algorithm framework model that"""

    def CreateTargets(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, insights: typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        """
        Create portfolio targets from the specified insights
        
        :param algorithm: The algorithm instance
        :param insights: The insights to create portfolio targets from
        :returns: An enumerable of portfolio targets to be sent to the execution model.
        """
        ...


class PortfolioConstructionModelPythonWrapper(QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModel):
    """Provides an implementation of IPortfolioConstructionModel that wraps a PyObject object"""

    @property
    def RebalanceOnSecurityChanges(self) -> bool:
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @RebalanceOnSecurityChanges.setter
    def RebalanceOnSecurityChanges(self, value: bool):
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @property
    def RebalanceOnInsightChanges(self) -> bool:
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    @RebalanceOnInsightChanges.setter
    def RebalanceOnInsightChanges(self, value: bool):
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the IPortfolioConstructionModel class with wrapped PyObject object
        
        :param model: Model defining how to build a portfolio from alphas
        """
        ...

    def CreateTargets(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, insights: typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        """
        Create portfolio targets from the specified insights
        
        :param algorithm: The algorithm instance
        :param insights: The insights to create portfolio targets from
        :returns: An enumerable of portfolio targets to be sent to the execution model.
        """
        ...

    def OnSecuritiesChanged(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time the we add/remove securities from the data feed
        
        :param algorithm: The algorithm instance that experienced the change in securities
        :param changes: The security additions and removals from the algorithm
        """
        ...

    def ShouldCreateTargetForInsight(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if the portfolio construction model should create a
        target for this insight
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the portfolio should create a target for the insight.
        """
        ...

    def IsRebalanceDue(self, insights: typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight], algorithmUtc: datetime.datetime) -> bool:
        """
        Determines if the portfolio should be rebalanced base on the provided rebalancing func,
        if any security change have been taken place or if an insight has expired or a new insight arrived
        If the rebalancing function has not been provided will return true.
        
        This method is protected.
        
        :param insights: The insights to create portfolio targets from
        :param algorithmUtc: The current algorithm UTC time
        :returns: True if should rebalance.
        """
        ...

    def GetTargetInsights(self) -> System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]:
        """
        Gets the target insights to calculate a portfolio target percent for
        
        This method is protected.
        
        :returns: An enumerable of the target insights.
        """
        ...

    def DetermineTargetPercent(self, activeInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Will determine the target percent for each insight
        
        This method is protected.
        
        :param activeInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...


class PortfolioConstructionModel(System.Object, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioConstructionModel):
    """Provides a base class for portfolio construction models"""

    @property
    def RebalanceOnSecurityChanges(self) -> bool:
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @RebalanceOnSecurityChanges.setter
    def RebalanceOnSecurityChanges(self, value: bool):
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @property
    def RebalanceOnInsightChanges(self) -> bool:
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    @RebalanceOnInsightChanges.setter
    def RebalanceOnInsightChanges(self, value: bool):
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    @property
    def InsightCollection(self) -> QuantConnect.Algorithm.Framework.Alphas.InsightCollection:
        """
        Provides a collection for managing insights
        
        This property is protected.
        """
        ...

    @property
    def Algorithm(self) -> QuantConnect.Interfaces.IAlgorithm:
        """
        The algorithm instance
        
        This property is protected.
        """
        ...

    @Algorithm.setter
    def Algorithm(self, value: QuantConnect.Interfaces.IAlgorithm):
        """
        The algorithm instance
        
        This property is protected.
        """
        ...

    @property
    def PythonWrapper(self) -> QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModelPythonWrapper:
        """
        This is required due to a limitation in PythonNet to resolved overriden methods.
        When Python calls a C# method that calls a method that's overriden in python it won't
        run the python implementation unless the call is performed through python too.
        
        This field is protected.
        """
        ...

    @PythonWrapper.setter
    def PythonWrapper(self, value: QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModelPythonWrapper):
        """
        This is required due to a limitation in PythonNet to resolved overriden methods.
        When Python calls a C# method that calls a method that's overriden in python it won't
        run the python implementation unless the call is performed through python too.
        
        This field is protected.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]]) -> None:
        """
        Initialize a new instance of PortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime] = None) -> None:
        """
        Initialize a new instance of PortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        """
        ...

    def SetPythonWrapper(self, pythonWrapper: QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModelPythonWrapper) -> None:
        """
        Used to set the PortfolioConstructionModelPythonWrapper instance if any
        
        This method is protected.
        """
        ...

    def CreateTargets(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, insights: typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        """
        Create portfolio targets from the specified insights
        
        :param algorithm: The algorithm instance
        :param insights: The insights to create portfolio targets from
        :returns: An enumerable of portfolio targets to be sent to the execution model.
        """
        ...

    def OnSecuritiesChanged(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time the we add/remove securities from the data feed
        
        :param algorithm: The algorithm instance that experienced the change in securities
        :param changes: The security additions and removals from the algorithm
        """
        ...

    def GetTargetInsights(self) -> System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]:
        """
        Gets the target insights to calculate a portfolio target percent for
        
        This method is protected.
        
        :returns: An enumerable of the target insights.
        """
        ...

    def ShouldCreateTargetForInsight(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if the portfolio construction model should create a
        target for this insight
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the portfolio should create a target for the insight.
        """
        ...

    def DetermineTargetPercent(self, activeInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Will determine the target percent for each insight
        
        This method is protected.
        
        :param activeInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...

    def SetRebalancingFunc(self, rebalance: typing.Any) -> None:
        """
        Python helper method to set the rebalancing function.
        This is required due to a python net limitation not being able to use the base type constructor, and also because
        when python algorithms use C# portfolio construction models, it can't convert python methods into func nor resolve
        the correct constructor for the date rules, timespan parameter.
        For performance we prefer python algorithms using the C# implementation
        
        This method is protected.
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        """
        ...

    def IsRebalanceDue(self, insights: typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight], algorithmUtc: datetime.datetime) -> bool:
        """
        Determines if the portfolio should be rebalanced base on the provided rebalancing func,
        if any security change have been taken place or if an insight has expired or a new insight arrived
        If the rebalancing function has not been provided will return true.
        
        This method is protected.
        
        :param insights: The insights to create portfolio targets from
        :param algorithmUtc: The current algorithm UTC time
        :returns: True if should rebalance.
        """
        ...

    def RefreshRebalance(self, algorithmUtc: datetime.datetime) -> None:
        """
        Refresh the next rebalance time and clears the security changes flag
        
        This method is protected.
        """
        ...

    @staticmethod
    def FilterInvalidInsightMagnitude(algorithm: QuantConnect.Interfaces.IAlgorithm, insights: typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight]:
        """
        Helper class that can be used by the different IPortfolioConstructionModel
        implementations to filter Insight instances with an invalid
        Insight.Magnitude value based on the IAlgorithmSettings
        
        This method is protected.
        
        :param algorithm: The algorithm instance
        :param insights: The insight collection to filter
        :returns: Returns a new array of insights removing invalid ones.
        """
        ...


class PortfolioBias(System.Enum):
    """Specifies the bias of the portfolio (Short, Long/Short, Long)"""

    Short = -1
    """Portfolio can only have short positions"""

    LongShort = 0
    """Portfolio can have both long and short positions"""

    Long = 1
    """Portfolio can only have long positions"""


class EqualWeightingPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModel):
    """
    Provides an implementation of IPortfolioConstructionModel that gives equal weighting to all
    securities. The target percent holdings of each security is 1/N where N is the number of securities. For
    insights of direction InsightDirection.Up, long targets are returned and for insights of direction
    InsightDirection.Down, short targets are returned.
    """

    @typing.overload
    def __init__(self, rebalancingDateRules: QuantConnect.Scheduling.IDateRule, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of EqualWeightingPortfolioConstructionModel
        
        :param rebalancingDateRules: The date rules used to define the next expected rebalance time in UTC
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of EqualWeightingPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of EqualWeightingPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalance: typing.Any, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of EqualWeightingPortfolioConstructionModel
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, timeSpan: datetime.timedelta, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of EqualWeightingPortfolioConstructionModel
        
        :param timeSpan: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, resolution: QuantConnect.Resolution = ..., portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of EqualWeightingPortfolioConstructionModel
        
        :param resolution: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    def DetermineTargetPercent(self, activeInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Will determine the target percent for each insight
        
        This method is protected.
        
        :param activeInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...

    def RespectPortfolioBias(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if a given insight respects the portfolio bias
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the insight respects the portfolio bias.
        """
        ...


class SectorWeightingPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.EqualWeightingPortfolioConstructionModel):
    """
    Provides an implementation of IPortfolioConstructionModel that generates percent targets based on the
    CompanyReference.IndustryTemplateCode.
    The target percent holdings of each sector is 1/S where S is the number of sectors and
    the target percent holdings of each security is 1/N where N is the number of securities of each sector.
    For insights of direction InsightDirection.Up, long targets are returned and for insights of direction
    InsightDirection.Down, short targets are returned.
    It will ignore Insight for symbols that have no CompanyReference.IndustryTemplateCode value.
    """

    @typing.overload
    def __init__(self, rebalancingDateRules: QuantConnect.Scheduling.IDateRule) -> None:
        """
        Initialize a new instance of SectorWeightingPortfolioConstructionModel
        
        :param rebalancingDateRules: The date rules used to define the next expected rebalance time in UTC
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]]) -> None:
        """
        Initialize a new instance of SectorWeightingPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime]) -> None:
        """
        Initialize a new instance of SectorWeightingPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        """
        ...

    @typing.overload
    def __init__(self, rebalance: typing.Any) -> None:
        """
        Initialize a new instance of SectorWeightingPortfolioConstructionModel
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        """
        ...

    @typing.overload
    def __init__(self, timeSpan: datetime.timedelta) -> None:
        """
        Initialize a new instance of SectorWeightingPortfolioConstructionModel
        
        :param timeSpan: Rebalancing frequency
        """
        ...

    @typing.overload
    def __init__(self, resolution: QuantConnect.Resolution = ...) -> None:
        """
        Initialize a new instance of SectorWeightingPortfolioConstructionModel
        
        :param resolution: Rebalancing frequency
        """
        ...

    def ShouldCreateTargetForInsight(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if the portfolio construction model should create a
        target for this insight
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the portfolio should create a target for the insight.
        """
        ...

    def DetermineTargetPercent(self, activeInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Will determine the target percent for each insight
        
        This method is protected.
        
        :param activeInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...

    def OnSecuritiesChanged(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time the we add/remove securities from the data feed
        
        :param algorithm: The algorithm instance that experienced the change in securities
        :param changes: The security additions and removals from the algorithm
        """
        ...

    def GetSectorCode(self, security: QuantConnect.Securities.Security) -> str:
        """
        Gets the sector code
        
        This method is protected.
        
        :param security: The security to create a sector code for
        :returns: The value of the sector code for the security.
        """
        ...


class InsightWeightingPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.EqualWeightingPortfolioConstructionModel):
    """
    Provides an implementation of IPortfolioConstructionModel that generates percent targets based on the
    Insight.Weight. The target percent holdings of each Symbol is given by the Insight.Weight
    from the last active Insight for that symbol.
    For insights of direction InsightDirection.Up, long targets are returned and for insights of direction
    InsightDirection.Down, short targets are returned.
    If the sum of all the last active Insight per symbol is bigger than 1, it will factor down each target
    percent holdings proportionally so the sum is 1.
    It will ignore Insight that have no Insight.Weight value.
    """

    @typing.overload
    def __init__(self, rebalancingDateRules: QuantConnect.Scheduling.IDateRule, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of InsightWeightingPortfolioConstructionModel
        
        :param rebalancingDateRules: The date rules used to define the next expected rebalance time in UTC
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalance: typing.Any, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of InsightWeightingPortfolioConstructionModel
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of InsightWeightingPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance.
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of InsightWeightingPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, timeSpan: datetime.timedelta, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of InsightWeightingPortfolioConstructionModel
        
        :param timeSpan: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, resolution: QuantConnect.Resolution = ..., portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of InsightWeightingPortfolioConstructionModel
        
        :param resolution: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    def ShouldCreateTargetForInsight(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if the portfolio construction model should create a
        target for this insight
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the portfolio should create a target for the insight.
        """
        ...

    def DetermineTargetPercent(self, activeInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Will determine the target percent for each insight
        
        This method is protected.
        
        :param activeInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...

    def GetValue(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> float:
        """
        Method that will determine which member will be used to compute the weights and gets its value
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: The value of the selected insight member.
        """
        ...


class ReturnsSymbolData(System.Object):
    """Contains returns specific to a symbol required for optimization model"""

    @property
    def Returns(self) -> System.Collections.Generic.Dictionary[datetime.datetime, float]:
        """Historical returns"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], lookback: int, period: int) -> None:
        """
        Initializes a new instance of the ReturnsSymbolData class
        
        :param symbol: The symbol of the data that updates the indicators
        :param lookback: Look-back period for the RateOfChange indicator
        :param period: Size of rolling window that contains historical RateOfChange
        """
        ...

    def Add(self, time: datetime.datetime, value: float) -> None:
        """
        Adds an item to this window and shifts all other elements
        
        :param time: The time associated with the value
        :param value: The value to use to update this window
        """
        ...

    def Update(self, time: datetime.datetime, value: float) -> bool:
        """
        Updates the state of the RateOfChange with the given value and returns true
        if this indicator is ready, false otherwise
        
        :param time: The time associated with the value
        :param value: The value to use to update this indicator
        :returns: True if this indicator is ready, false otherwise.
        """
        ...

    def Reset(self) -> None:
        """Resets all indicators of this object to its initial state"""
        ...


class ReturnsSymbolDataExtensions(System.Object):
    """Extension methods for ReturnsSymbolData"""

    @staticmethod
    def FormReturnsMatrix(symbolData: System.Collections.Generic.Dictionary[QuantConnect.Symbol, QuantConnect.Algorithm.Framework.Portfolio.ReturnsSymbolData], symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> typing.List[float]:
        """
        Converts a dictionary of ReturnsSymbolData keyed by Symbol into a matrix
        
        :param symbolData: Dictionary of ReturnsSymbolData keyed by Symbol to be converted into a matrix
        :param symbols: List of Symbol to be included in the matrix
        """
        ...


class BlackLittermanOptimizationPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModel):
    """
    Provides an implementation of Black-Litterman portfolio optimization. The model adjusts equilibrium market
    returns by incorporating views from multiple alpha models and therefore to get the optimal risky portfolio
    reflecting those views. If insights of all alpha models have None magnitude or there are linearly dependent
    vectors in link matrix of views, the expected return would be the implied excess equilibrium return.
    The interval of weights in optimization method can be changed based on the long-short algorithm.
    The default model uses the 0.0025 as weight-on-views scalar parameter tau. The optimization method
    maximizes the Sharpe ratio with the weight range from -1 to 1.
    """

    @typing.overload
    def __init__(self, timeSpan: datetime.timedelta, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., riskFreeRate: float = 0.0, delta: float = 2.5, tau: float = 0.05, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param timeSpan: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param riskFreeRate: The risk free rate
        :param delta: The risk aversion coeffficient of the market portfolio
        :param tau: The model parameter indicating the uncertainty of the CAPM prior
        :param optimizer: The portfolio optimization algorithm. If no algorithm is explicitly provided then the default will be max Sharpe ratio optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalanceResolution: QuantConnect.Resolution = ..., portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., riskFreeRate: float = 0.0, delta: float = 2.5, tau: float = 0.05, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalanceResolution: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param riskFreeRate: The risk free rate
        :param delta: The risk aversion coeffficient of the market portfolio
        :param tau: The model parameter indicating the uncertainty of the CAPM prior
        :param optimizer: The portfolio optimization algorithm. If no algorithm is explicitly provided then the default will be max Sharpe ratio optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., riskFreeRate: float = 0.0, delta: float = 2.5, tau: float = 0.05, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param riskFreeRate: The risk free rate
        :param delta: The risk aversion coeffficient of the market portfolio
        :param tau: The model parameter indicating the uncertainty of the CAPM prior
        :param optimizer: The portfolio optimization algorithm. If no algorithm is explicitly provided then the default will be max Sharpe ratio optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingDateRules: QuantConnect.Scheduling.IDateRule, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., riskFreeRate: float = 0.0, delta: float = 2.5, tau: float = 0.05, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalancingDateRules: The date rules used to define the next expected rebalance time in UTC
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param riskFreeRate: The risk free rate
        :param delta: The risk aversion coeffficient of the market portfolio
        :param tau: The model parameter indicating the uncertainty of the CAPM prior
        :param optimizer: The portfolio optimization algorithm. If no algorithm is explicitly provided then the default will be max Sharpe ratio optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalance: typing.Any, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., riskFreeRate: float = 0.0, delta: float = 2.5, tau: float = 0.05, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param riskFreeRate: The risk free rate
        :param delta: The risk aversion coeffficient of the market portfolio
        :param tau: The model parameter indicating the uncertainty of the CAPM prior
        :param optimizer: The portfolio optimization algorithm. If no algorithm is explicitly provided then the default will be max Sharpe ratio optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., riskFreeRate: float = 0.0, delta: float = 2.5, tau: float = 0.05, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance.
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param riskFreeRate: The risk free rate
        :param delta: The risk aversion coeffficient of the market portfolio
        :param tau: The model parameter indicating the uncertainty of the CAPM prior
        :param optimizer: The portfolio optimization algorithm. If no algorithm is explicitly provided then the default will be max Sharpe ratio optimization.
        """
        ...

    def ShouldCreateTargetForInsight(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if the portfolio construction model should create a
        target for this insight
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the portfolio should create a target for the insight.
        """
        ...

    def DetermineTargetPercent(self, lastActiveInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Will determine the target percent for each insight
        
        This method is protected.
        
        :param lastActiveInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...

    def GetTargetInsights(self) -> System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]:
        """
        Gets the target insights to calculate a portfolio target percent for
        
        This method is protected.
        
        :returns: An enumerable of the target insights.
        """
        ...

    def OnSecuritiesChanged(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time the we add/remove securities from the data feed
        
        :param algorithm: The algorithm instance that experienced the change in securities
        :param changes: The security additions and removals from the algorithm
        """
        ...

    def GetEquilibriumReturns(self, returns: typing.List[float], Σ: typing.List[float]) -> typing.List[float]:
        """
        Calculate equilibrium returns and covariance
        
        :param returns: Matrix of returns where each column represents a security and each row returns for the given date/time (size: K x N)
        :param Σ: Multi-dimensional array of double with the portfolio covariance of returns (size: K x K).
        :returns: Array of double of equilibrium returns.
        """
        ...


class AccumulativeInsightPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModel):
    """
    Provides an implementation of IPortfolioConstructionModel that allocates percent of account
    to each insight, defaulting to 3%.
    For insights of direction InsightDirection.Up, long targets are returned and
    for insights of direction InsightDirection.Down, short targets are returned.
    By default, no rebalancing shall be done.
    Rules:
       1. On active Up insight, increase position size by percent
       2. On active Down insight, decrease position size by percent
       3. On active Flat insight, move by percent towards 0
       4. On expired insight, and no other active insight, emits a 0 target'''
    """

    @typing.overload
    def __init__(self, rebalancingDateRules: QuantConnect.Scheduling.IDateRule, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., percent: float = 0.03) -> None:
        """
        Initialize a new instance of AccumulativeInsightPortfolioConstructionModel
        
        :param rebalancingDateRules: The date rules used to define the next expected rebalance time in UTC
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param percent: The percentage amount of the portfolio value to allocate to a single insight. The value of percent should be in the range [0,1]. The default value is 0.03.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]] = None, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., percent: float = 0.03) -> None:
        """
        Initialize a new instance of AccumulativeInsightPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param percent: The percentage amount of the portfolio value to allocate to a single insight. The value of percent should be in the range [0,1]. The default value is 0.03.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., percent: float = 0.03) -> None:
        """
        Initialize a new instance of AccumulativeInsightPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param percent: The percentage amount of the portfolio value to allocate to a single insight. The value of percent should be in the range [0,1]. The default value is 0.03.
        """
        ...

    @typing.overload
    def __init__(self, rebalance: typing.Any, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., percent: float = 0.03) -> None:
        """
        Initialize a new instance of AccumulativeInsightPortfolioConstructionModel
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param percent: The percentage amount of the portfolio value to allocate to a single insight. The value of percent should be in the range [0,1]. The default value is 0.03.
        """
        ...

    @typing.overload
    def __init__(self, timeSpan: datetime.timedelta, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., percent: float = 0.03) -> None:
        """
        Initialize a new instance of AccumulativeInsightPortfolioConstructionModel
        
        :param timeSpan: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param percent: The percentage amount of the portfolio value to allocate to a single insight. The value of percent should be in the range [0,1]. The default value is 0.03.
        """
        ...

    @typing.overload
    def __init__(self, resolution: QuantConnect.Resolution, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., percent: float = 0.03) -> None:
        """
        Initialize a new instance of AccumulativeInsightPortfolioConstructionModel
        
        :param resolution: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param percent: The percentage amount of the portfolio value to allocate to a single insight. The value of percent should be in the range [0,1]. The default value is 0.03.
        """
        ...

    def GetTargetInsights(self) -> System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]:
        """
        Gets the target insights to calculate a portfolio target percent for
        
        This method is protected.
        
        :returns: An enumerable of the target insights.
        """
        ...

    def DetermineTargetPercent(self, activeInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Determines the target percent for each insight
        
        This method is protected.
        
        :param activeInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...


class MaximumSharpeRatioPortfolioOptimizer(System.Object, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer):
    """
    Provides an implementation of a portfolio optimizer that maximizes the portfolio Sharpe Ratio.
    The interval of weights in optimization method can be changed based on the long-short algorithm.
    The default model uses flat risk free rate and weight for an individual security range from -1 to 1.
    """

    def __init__(self, lower: float = -1, upper: float = 1, riskFreeRate: float = 0.0) -> None:
        ...

    def GetBudgetConstraint(self, size: int) -> typing.Any:
        """
        Sum of all weight is one: 1^T w = 1 / Σw = 1
        
        This method is protected.
        
        :param size: number of variables
        :returns: linear constaraint object.
        """
        ...

    def GetBoundaryConditions(self, size: int) -> System.Collections.Generic.IEnumerable[LinearConstraint]:
        """
        Boundary constraints on weights: lw ≤ w ≤ up
        
        This method is protected.
        
        :param size: number of variables
        :returns: enumeration of linear constaraint objects.
        """
        ...

    def Optimize(self, historicalReturns: typing.List[float], expectedReturns: typing.List[float] = None, covariance: typing.List[float] = None) -> typing.List[float]:
        """
        Perform portfolio optimization for a provided matrix of historical returns and an array of expected returns
        
        :param historicalReturns: Matrix of annualized historical returns where each column represents a security and each row returns for the given date/time (size: K x N).
        :param expectedReturns: Array of double with the portfolio annualized expected returns (size: K x 1).
        :param covariance: Multi-dimensional array of double with the portfolio covariance of annualized returns (size: K x K).
        :returns: Array of double with the portfolio weights (size: K x 1).
        """
        ...


class MinimumVariancePortfolioOptimizer(System.Object, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer):
    """
    Provides an implementation of a minimum variance portfolio optimizer that calculate the optimal weights
    with the weight range from -1 to 1 and minimize the portfolio variance with a target return of 2%
    """

    def __init__(self, lower: float = -1, upper: float = 1, targetReturn: float = 0.02) -> None:
        ...

    def GetBudgetConstraint(self, size: int) -> typing.Any:
        """
        Sum of all weight is one: 1^T w = 1 / Σw = 1
        
        This method is protected.
        
        :param size: number of variables
        :returns: linear constaraint object.
        """
        ...

    def GetBoundaryConditions(self, size: int) -> System.Collections.Generic.IEnumerable[LinearConstraint]:
        """
        Boundary constraints on weights: lw ≤ w ≤ up
        
        This method is protected.
        
        :param size: number of variables
        :returns: enumeration of linear constaraint objects.
        """
        ...

    def Optimize(self, historicalReturns: typing.List[float], expectedReturns: typing.List[float] = None, covariance: typing.List[float] = None) -> typing.List[float]:
        """
        Perform portfolio optimization for a provided matrix of historical returns and an array of expected returns
        
        :param historicalReturns: Matrix of annualized historical returns where each column represents a security and each row returns for the given date/time (size: K x N).
        :param expectedReturns: Array of double with the portfolio annualized expected returns (size: K x 1).
        :param covariance: Multi-dimensional array of double with the portfolio covariance of annualized returns (size: K x K).
        :returns: Array of double with the portfolio weights (size: K x 1).
        """
        ...


class MeanVarianceOptimizationPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModel):
    """
    Provides an implementation of Mean-Variance portfolio optimization based on modern portfolio theory.
    The interval of weights in optimization method can be changed based on the long-short algorithm.
    The default model uses the last three months daily price to calculate the optimal weight
    with the weight range from -1 to 1 and minimize the portfolio variance with a target return of 2%
    """

    @typing.overload
    def __init__(self, rebalancingDateRules: QuantConnect.Scheduling.IDateRule, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., targetReturn: float = 0.02, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalancingDateRules: The date rules used to define the next expected rebalance time in UTC
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param targetReturn: The target portfolio return
        :param optimizer: The portfolio optimization algorithm. If the algorithm is not provided then the default will be mean-variance optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalanceResolution: QuantConnect.Resolution = ..., portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., targetReturn: float = 0.02, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalanceResolution: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param targetReturn: The target portfolio return
        :param optimizer: The portfolio optimization algorithm. If the algorithm is not provided then the default will be mean-variance optimization.
        """
        ...

    @typing.overload
    def __init__(self, timeSpan: datetime.timedelta, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., targetReturn: float = 0.02, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param timeSpan: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param targetReturn: The target portfolio return
        :param optimizer: The portfolio optimization algorithm. If the algorithm is not provided then the default will be mean-variance optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalance: typing.Any, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., targetReturn: float = 0.02, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param targetReturn: The target portfolio return
        :param optimizer: The portfolio optimization algorithm. If the algorithm is not provided then the default will be mean-variance optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., targetReturn: float = 0.02, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param targetReturn: The target portfolio return
        :param optimizer: The portfolio optimization algorithm. If the algorithm is not provided then the default will be mean-variance optimization.
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ..., lookback: int = 1, period: int = 63, resolution: QuantConnect.Resolution = ..., targetReturn: float = 0.02, optimizer: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioOptimizer = None) -> None:
        """
        Initialize the model
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance.
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        :param lookback: Historical return lookback period
        :param period: The time interval of history price to calculate the weight
        :param resolution: The resolution of the history price
        :param targetReturn: The target portfolio return
        :param optimizer: The portfolio optimization algorithm. If the algorithm is not provided then the default will be mean-variance optimization.
        """
        ...

    def ShouldCreateTargetForInsight(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if the portfolio construction model should create a
        target for this insight
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the portfolio should create a target for the insight.
        """
        ...

    def DetermineTargetPercent(self, activeInsights: System.Collections.Generic.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.Dictionary[QuantConnect.Algorithm.Framework.Alphas.Insight, float]:
        """
        Will determine the target percent for each insight
        
        This method is protected.
        
        :param activeInsights: The active insights to generate a target for
        :returns: A target percent for each insight.
        """
        ...

    def OnSecuritiesChanged(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Event fired each time the we add/remove securities from the data feed
        
        :param algorithm: The algorithm instance that experienced the change in securities
        :param changes: The security additions and removals from the algorithm
        """
        ...


class ConfidenceWeightedPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.InsightWeightingPortfolioConstructionModel):
    """
    Provides an implementation of IPortfolioConstructionModel that generates percent targets based on the
    Insight.Confidence. The target percent holdings of each Symbol is given by the Insight.Confidence
    from the last active Insight for that symbol.
    For insights of direction InsightDirection.Up, long targets are returned and for insights of direction
    InsightDirection.Down, short targets are returned.
    If the sum of all the last active Insight per symbol is bigger than 1, it will factor down each target
    percent holdings proportionally so the sum is 1.
    It will ignore Insight that have no Insight.Confidence value.
    """

    @typing.overload
    def __init__(self, rebalancingDateRules: QuantConnect.Scheduling.IDateRule, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of ConfidenceWeightedPortfolioConstructionModel
        
        :param rebalancingDateRules: The date rules used to define the next expected rebalance time in UTC
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalance: typing.Any, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of ConfidenceWeightedPortfolioConstructionModel
        
        :param rebalance: Rebalancing func or if a date rule, timedelta will be converted into func. For a given algorithm UTC DateTime the func returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of ConfidenceWeightedPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance time or null if unknown, in which case the function will be called again in the next loop. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, rebalancingFunc: typing.Callable[[datetime.datetime], datetime.datetime], portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of ConfidenceWeightedPortfolioConstructionModel
        
        :param rebalancingFunc: For a given algorithm UTC DateTime returns the next expected rebalance UTC time. Returning current time will trigger rebalance. If null will be ignored
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, timeSpan: datetime.timedelta, portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of ConfidenceWeightedPortfolioConstructionModel
        
        :param timeSpan: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    @typing.overload
    def __init__(self, resolution: QuantConnect.Resolution = ..., portfolioBias: QuantConnect.Algorithm.Framework.Portfolio.PortfolioBias = ...) -> None:
        """
        Initialize a new instance of ConfidenceWeightedPortfolioConstructionModel
        
        :param resolution: Rebalancing frequency
        :param portfolioBias: Specifies the bias of the portfolio (Short, Long/Short, Long)
        """
        ...

    def ShouldCreateTargetForInsight(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> bool:
        """
        Method that will determine if the portfolio construction model should create a
        target for this insight
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: True if the portfolio should create a target for the insight.
        """
        ...

    def GetValue(self, insight: QuantConnect.Algorithm.Framework.Alphas.Insight) -> float:
        """
        Method that will determine which member will be used to compute the weights and gets its value
        
        This method is protected.
        
        :param insight: The insight to create a target for
        :returns: The value of the selected insight member.
        """
        ...


class NullPortfolioConstructionModel(QuantConnect.Algorithm.Framework.Portfolio.PortfolioConstructionModel):
    """Provides an implementation of IPortfolioConstructionModel that does nothing"""

    def CreateTargets(self, algorithm: QuantConnect.Algorithm.QCAlgorithm, insights: typing.List[QuantConnect.Algorithm.Framework.Alphas.Insight]) -> System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        ...


class PortfolioTarget(System.Object, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget):
    """
    Provides an implementation of IPortfolioTarget that specifies a
    specified quantity of a security to be held by the algorithm
    """

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Gets the symbol of this target"""
        ...

    @property
    def Quantity(self) -> float:
        """Gets the target quantity for the symbol"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quantity: float) -> None:
        """
        Initializes a new instance of the PortfolioTarget class
        
        :param symbol: The symbol this target is for
        :param quantity: The target quantity
        """
        ...

    @staticmethod
    @typing.overload
    def Percent(algorithm: QuantConnect.Interfaces.IAlgorithm, symbol: typing.Union[QuantConnect.Symbol, str], percent: float) -> QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget:
        """
        Creates a new target for the specified percent
        
        :param algorithm: The algorithm instance, used for getting total portfolio value and current security price
        :param symbol: The symbol the target is for
        :param percent: The requested target percent of total portfolio value
        :returns: A portfolio target for the specified symbol/percent.
        """
        ...

    @staticmethod
    @typing.overload
    def Percent(algorithm: QuantConnect.Interfaces.IAlgorithm, symbol: typing.Union[QuantConnect.Symbol, str], percent: float, returnDeltaQuantity: bool = False) -> QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget:
        """
        Creates a new target for the specified percent
        
        :param algorithm: The algorithm instance, used for getting total portfolio value and current security price
        :param symbol: The symbol the target is for
        :param percent: The requested target percent of total portfolio value
        :param returnDeltaQuantity: True, result quantity will be the Delta required to reach target percent. False, the result quantity will be the Total quantity to reach the target percent, including current holdings
        :returns: A portfolio target for the specified symbol/percent.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class PortfolioTargetCollection(System.Object, System.Collections.Generic.ICollection[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget], typing.Iterable[System.Collections.Generic.KeyValuePair[QuantConnect.Symbol, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]]):
    """Provides a collection for managing IPortfolioTargets for each symbol"""

    @property
    def Count(self) -> int:
        """Gets the number of targets in this collection"""
        ...

    @property
    def IsReadOnly(self) -> bool:
        """Gets `false`. This collection is not read-only."""
        ...

    @property
    def Keys(self) -> System.Collections.Generic.ICollection[QuantConnect.Symbol]:
        """Gets the symbol keys for this collection"""
        ...

    @property
    def Values(self) -> System.Collections.Generic.ICollection[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        """
        Gets all portfolio targets in this collection
        Careful, will return targets for securities that might have no data yet.
        """
        ...

    @typing.overload
    def Add(self, target: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget) -> None:
        """
        Adds the specified target to the collection. If a target for the same symbol
        already exists it wil be overwritten.
        
        :param target: The portfolio target to add
        """
        ...

    @typing.overload
    def Add(self, target: System.Collections.Generic.KeyValuePair[QuantConnect.Symbol, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]) -> None:
        """
        Adds the specified target to the collection. If a target for the same symbol
        already exists it wil be overwritten.
        
        :param target: The portfolio target to add
        """
        ...

    @typing.overload
    def Add(self, symbol: typing.Union[QuantConnect.Symbol, str], target: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget) -> None:
        """
        Adds the specified target to the collection. If a target for the same symbol
        already exists it wil be overwritten.
        
        :param symbol: The symbol key
        :param target: The portfolio target to add
        """
        ...

    @typing.overload
    def AddRange(self, targets: System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]) -> None:
        """
        Adds the specified targets to the collection. If a target for the same symbol
        already exists it will be overwritten.
        
        :param targets: The portfolio targets to add
        """
        ...

    @typing.overload
    def AddRange(self, targets: typing.List[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]) -> None:
        """
        Adds the specified targets to the collection. If a target for the same symbol
        already exists it will be overwritten.
        
        :param targets: The portfolio targets to add
        """
        ...

    def Clear(self) -> None:
        """Removes all portfolio targets from this collection"""
        ...

    def ClearFulfilled(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Removes fulfilled portfolio targets from this collection.
        Will only take into account actual holdings and ignore open orders.
        """
        ...

    @typing.overload
    def Contains(self, target: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget) -> bool:
        """
        Determines whether or not the specified target exists in this collection.
        NOTE: This checks for the exact specified target, not by symbol. Use ContainsKey
        to check by symbol.
        
        :param target: The portfolio target to check for existence.
        :returns: True if the target exists, false otherwise.
        """
        ...

    @typing.overload
    def Contains(self, target: System.Collections.Generic.KeyValuePair[QuantConnect.Symbol, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]) -> bool:
        """
        Determines whether the specified symbol/target pair exists in this collection
        
        :param target: The symbol/target pair
        :returns: True if the pair exists, false otherwise.
        """
        ...

    def ContainsKey(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Determines whether the specified symbol exists as a key in this collection
        
        :param symbol: The symbol key
        :returns: True if the symbol exists in this collection, false otherwise.
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget], arrayIndex: int) -> None:
        """
        Copies the targets in this collection to the specified array
        
        :param array: The destination array to copy to
        :param arrayIndex: The index in the array to start copying to
        """
        ...

    @typing.overload
    def CopyTo(self, array: typing.List[System.Collections.Generic.KeyValuePair[QuantConnect.Symbol, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]], arrayIndex: int) -> None:
        """
        Copies the targets in this collection to the specified array
        
        :param array: The destination array to copy to
        :param arrayIndex: The index in the array to start copying to
        """
        ...

    @typing.overload
    def Remove(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Removes the target for the specified symbol if it exists in this collection.
        
        :param symbol: The symbol to remove
        :returns: True if the symbol's target was removed, false if it doesn't exist in the collection.
        """
        ...

    @typing.overload
    def Remove(self, target: System.Collections.Generic.KeyValuePair[QuantConnect.Symbol, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]) -> bool:
        """
        Removes the target for the specified symbol/target pair if it exists in this collection.
        
        :param target: The symbol/target pair to remove
        :returns: True if the symbol's target was removed, false if it doesn't exist in the collection.
        """
        ...

    @typing.overload
    def Remove(self, target: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget) -> bool:
        """
        Removes the target if it exists in this collection.
        
        :param target: The target to remove
        :returns: True if the target was removed, false if it doesn't exist in the collection.
        """
        ...

    def TryGetValue(self, symbol: typing.Union[QuantConnect.Symbol, str], target: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget) -> bool:
        """
        Attempts to retrieve the target for the specified symbol
        
        :param symbol: The symbol
        :param target: The portfolio target for the symbol, or null if not found
        :returns: True if the symbol's target was found, false if it does not exist in this collection.
        """
        ...

    def __getitem__(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget:
        """
        Gets or sets the portfolio target for the specified symbol
        
        :param symbol: The symbol
        :returns: The symbol's portolio target if it exists in this collection, if not a KeyNotFoundException will be thrown.
        """
        ...

    def __setitem__(self, symbol: typing.Union[QuantConnect.Symbol, str], value: QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget) -> None:
        """
        Gets or sets the portfolio target for the specified symbol
        
        :param symbol: The symbol
        :returns: The symbol's portolio target if it exists in this collection, if not a KeyNotFoundException will be thrown.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[System.Collections.Generic.KeyValuePair[QuantConnect.Symbol, QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]]:
        """
        Gets an enumerator to iterator over the symbol/target key value pairs in this collection.
        
        :returns: Symbol/target key value pair enumerator.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        """
        Gets an enumerator to iterator over all portfolio targets in this collection.
        This is the default enumerator for this collection.
        
        :returns: Portfolio targets enumerator.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Gets an enumerator to iterator over all portfolio targets in this collection.
        This is the default enumerator for this collection.
        Careful, will return targets for securities that might have no data yet.
        
        :returns: Portfolio targets enumerator.
        """
        ...

    def OrderByMarginImpact(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        """
        Returned an ordered enumerable where position reducing orders are executed first
        and the remaining orders are executed in decreasing order value.
        Will NOT return targets for securities that have no data yet.
        Will NOT return targets for which current holdings + open orders quantity, sum up to the target quantity
        
        :param algorithm: The algorithm instance
        """
        ...


