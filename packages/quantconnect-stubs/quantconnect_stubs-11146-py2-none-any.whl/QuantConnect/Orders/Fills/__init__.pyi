import abc
import datetime
import typing

import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Orders.Fills
import QuantConnect.Python
import QuantConnect.Securities
import System


class Fill(System.Object):
    """Defines the result for IFillModel.Fill"""

    @property
    def OrderEvent(self) -> QuantConnect.Orders.OrderEvent:
        """The order event associated to this Fill instance"""
        ...

    def __init__(self, orderEvent: QuantConnect.Orders.OrderEvent) -> None:
        """Creates a new Fill instance"""
        ...


class FillModelParameters(System.Object):
    """Defines the parameters for the IFillModel method"""

    @property
    def Security(self) -> QuantConnect.Securities.Security:
        """Gets the Security"""
        ...

    @property
    def Order(self) -> QuantConnect.Orders.Order:
        """Gets the Order"""
        ...

    @property
    def ConfigProvider(self) -> QuantConnect.Interfaces.ISubscriptionDataConfigProvider:
        """Gets the SubscriptionDataConfig provider"""
        ...

    @property
    def StalePriceTimeSpan(self) -> datetime.timedelta:
        """Gets the minimum time span elapsed to consider a market fill price as stale (defaults to one hour)"""
        ...

    def __init__(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, configProvider: QuantConnect.Interfaces.ISubscriptionDataConfigProvider, stalePriceTimeSpan: datetime.timedelta) -> None:
        """
        Creates a new instance
        
        :param security: Security asset we're filling
        :param order: Order packet to model
        :param configProvider: The ISubscriptionDataConfigProvider to use
        :param stalePriceTimeSpan: The minimum time span elapsed to consider a fill price as stale
        """
        ...


class IFillModel(metaclass=abc.ABCMeta):
    """Represents a model that simulates order fill events"""

    def Fill(self, parameters: QuantConnect.Orders.Fills.FillModelParameters) -> QuantConnect.Orders.Fills.Fill:
        """
        Return an order event with the fill details
        
        :param parameters: A FillModelParameters object containing the security and order
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...


class FillModel(System.Object, QuantConnect.Orders.Fills.IFillModel):
    """Provides a base class for all fill models"""

    class Prices(System.Object):
        """This class has no documentation."""

        @property
        def EndTime(self) -> datetime.datetime:
            ...

        @property
        def Current(self) -> float:
            ...

        @property
        def Open(self) -> float:
            ...

        @property
        def High(self) -> float:
            ...

        @property
        def Low(self) -> float:
            ...

        @property
        def Close(self) -> float:
            ...

        @typing.overload
        def __init__(self, bar: QuantConnect.Data.Market.IBaseDataBar) -> None:
            ...

        @typing.overload
        def __init__(self, endTime: datetime.datetime, bar: QuantConnect.Data.Market.IBar) -> None:
            ...

        @typing.overload
        def __init__(self, endTime: datetime.datetime, current: float, open: float, high: float, low: float, close: float) -> None:
            ...

    @property
    def Parameters(self) -> QuantConnect.Orders.Fills.FillModelParameters:
        """
        The parameters instance to be used by the different XxxxFill() implementations
        
        This property is protected.
        """
        ...

    @Parameters.setter
    def Parameters(self, value: QuantConnect.Orders.Fills.FillModelParameters):
        """
        The parameters instance to be used by the different XxxxFill() implementations
        
        This property is protected.
        """
        ...

    @property
    def PythonWrapper(self) -> QuantConnect.Python.FillModelPythonWrapper:
        """
        This is required due to a limitation in PythonNet to resolved overriden methods.
        When Python calls a C# method that calls a method that's overriden in python it won't
        run the python implementation unless the call is performed through python too.
        
        This field is protected.
        """
        ...

    @PythonWrapper.setter
    def PythonWrapper(self, value: QuantConnect.Python.FillModelPythonWrapper):
        """
        This is required due to a limitation in PythonNet to resolved overriden methods.
        When Python calls a C# method that calls a method that's overriden in python it won't
        run the python implementation unless the call is performed through python too.
        
        This field is protected.
        """
        ...

    def SetPythonWrapper(self, pythonWrapper: QuantConnect.Python.FillModelPythonWrapper) -> None:
        """Used to set the FillModelPythonWrapper instance if any"""
        ...

    def Fill(self, parameters: QuantConnect.Orders.Fills.FillModelParameters) -> QuantConnect.Orders.Fills.Fill:
        """
        Return an order event with the fill details
        
        :param parameters: A FillModelParameters object containing the security and order
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def MarketFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default market fill model for the base security class. Fills at the last traded price.
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def StopMarketFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.StopMarketOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default stop fill model implementation in base class security. (Stop Market Order Type)
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def StopLimitFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.StopLimitOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default stop limit fill model implementation in base class security. (Stop Limit Order Type)
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def LimitIfTouchedFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.LimitIfTouchedOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default limit if touched fill model implementation in base class security. (Limit If Touched Order Type)
        
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def LimitFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.LimitOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default limit order fill model in the base security class.
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def MarketOnOpenFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOnOpenOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Market on Open Fill Model. Return an order event with the fill details
        
        :param asset: Asset we're trading with this order
        :param order: Order to be filled
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def MarketOnCloseFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOnCloseOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Market on Close Fill Model. Return an order event with the fill details
        
        :param asset: Asset we're trading with this order
        :param order: Order to be filled
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def GetPrices(self, asset: QuantConnect.Securities.Security, direction: QuantConnect.Orders.OrderDirection) -> QuantConnect.Orders.Fills.FillModel.Prices:
        """
        Get the minimum and maximum price for this security in the last bar:
        
        This method is protected.
        
        :param asset: Security asset we're checking
        :param direction: The order direction, decides whether to pick bid or ask
        """
        ...

    @staticmethod
    def IsExchangeOpen(asset: QuantConnect.Securities.Security, isExtendedMarketHours: bool) -> bool:
        """
        Determines if the exchange is open using the current time of the asset
        
        This method is protected.
        """
        ...


class ImmediateFillModel(QuantConnect.Orders.Fills.FillModel):
    """Represents the default fill model used to simulate order fills"""


class LatestPriceFillModel(QuantConnect.Orders.Fills.ImmediateFillModel):
    """
    This fill model is provided because currently the data sourced for Crypto
    is limited to one minute snapshots for Quote data. This fill model will
    ignore the trade/quote distinction and return the latest pricing information
    in order to determine the correct fill price
    """

    def GetPrices(self, asset: QuantConnect.Securities.Security, direction: QuantConnect.Orders.OrderDirection) -> QuantConnect.Orders.Fills.FillModel.Prices:
        """
        Get the minimum and maximum price for this security in the last bar
        Ignore the Trade/Quote distinction - fill with the latest pricing information
        
        This method is protected.
        
        :param asset: Security asset we're checking
        :param direction: The order direction, decides whether to pick bid or ask
        """
        ...


class EquityFillModel(System.Object, QuantConnect.Orders.Fills.IFillModel):
    """Provides a base class for all fill models"""

    class Prices(System.Object):
        """This class has no documentation."""

        @property
        def EndTime(self) -> datetime.datetime:
            ...

        @property
        def Current(self) -> float:
            ...

        @property
        def Open(self) -> float:
            ...

        @property
        def High(self) -> float:
            ...

        @property
        def Low(self) -> float:
            ...

        @property
        def Close(self) -> float:
            ...

        @typing.overload
        def __init__(self, bar: QuantConnect.Data.Market.IBaseDataBar) -> None:
            ...

        @typing.overload
        def __init__(self, endTime: datetime.datetime, bar: QuantConnect.Data.Market.IBar) -> None:
            ...

        @typing.overload
        def __init__(self, endTime: datetime.datetime, current: float, open: float, high: float, low: float, close: float) -> None:
            ...

    @property
    def Parameters(self) -> QuantConnect.Orders.Fills.FillModelParameters:
        """
        The parameters instance to be used by the different XxxxFill() implementations
        
        This property is protected.
        """
        ...

    @Parameters.setter
    def Parameters(self, value: QuantConnect.Orders.Fills.FillModelParameters):
        """
        The parameters instance to be used by the different XxxxFill() implementations
        
        This property is protected.
        """
        ...

    @property
    def PythonWrapper(self) -> QuantConnect.Python.FillModelPythonWrapper:
        """
        This is required due to a limitation in PythonNet to resolved overriden methods.
        When Python calls a C# method that calls a method that's overriden in python it won't
        run the python implementation unless the call is performed through python too.
        
        This field is protected.
        """
        ...

    @PythonWrapper.setter
    def PythonWrapper(self, value: QuantConnect.Python.FillModelPythonWrapper):
        """
        This is required due to a limitation in PythonNet to resolved overriden methods.
        When Python calls a C# method that calls a method that's overriden in python it won't
        run the python implementation unless the call is performed through python too.
        
        This field is protected.
        """
        ...

    def SetPythonWrapper(self, pythonWrapper: QuantConnect.Python.FillModelPythonWrapper) -> None:
        """Used to set the FillModelPythonWrapper instance if any"""
        ...

    def Fill(self, parameters: QuantConnect.Orders.Fills.FillModelParameters) -> QuantConnect.Orders.Fills.Fill:
        """
        Return an order event with the fill details
        
        :param parameters: A FillModelParameters object containing the security and order
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def LimitIfTouchedFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.LimitIfTouchedOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default limit if touched fill model implementation in base class security.
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def MarketFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default market fill model for the base security class. Fills at the last traded price.
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def StopMarketFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.StopMarketOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default stop fill model implementation in base class security. (Stop Market Order Type)
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def StopLimitFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.StopLimitOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default stop limit fill model implementation in base class security. (Stop Limit Order Type)
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def LimitFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.LimitOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Default limit order fill model in the base security class.
        
        :param asset: Security asset we're filling
        :param order: Order packet to model
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def MarketOnOpenFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOnOpenOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Market on Open Fill Model. Return an order event with the fill details
        
        :param asset: Asset we're trading with this order
        :param order: Order to be filled
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def MarketOnCloseFill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOnCloseOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Market on Close Fill Model. Return an order event with the fill details
        
        :param asset: Asset we're trading with this order
        :param order: Order to be filled
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def GetPrices(self, asset: QuantConnect.Securities.Security, direction: QuantConnect.Orders.OrderDirection) -> QuantConnect.Orders.Fills.EquityFillModel.Prices:
        """
        Get the minimum and maximum price for this security in the last bar:
        
        This method is protected.
        
        :param asset: Security asset we're checking
        :param direction: The order direction, decides whether to pick bid or ask
        """
        ...

    @staticmethod
    def IsExchangeOpen(asset: QuantConnect.Securities.Security, isExtendedMarketHours: bool) -> bool:
        """
        Determines if the exchange is open using the current time of the asset
        
        This method is protected.
        """
        ...


