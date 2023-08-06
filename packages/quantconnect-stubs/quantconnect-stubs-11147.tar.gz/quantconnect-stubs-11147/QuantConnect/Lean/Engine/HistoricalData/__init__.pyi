import abc
import typing

import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.DataFeeds
import QuantConnect.Lean.Engine.HistoricalData
import QuantConnect.Securities
import System.Collections.Generic


class SynchronizingHistoryProvider(QuantConnect.Data.HistoryProviderBase, metaclass=abc.ABCMeta):
    """
    Provides an abstract implementation of IHistoryProvider
    which provides synchronization of multiple history results
    """

    @property
    def DataPointCount(self) -> int:
        """Gets the total number of data points emitted by this history provider"""
        ...

    def CreateSliceEnumerableFromSubscriptions(self, subscriptions: System.Collections.Generic.List[QuantConnect.Lean.Engine.DataFeeds.Subscription], sliceTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]:
        """
        Enumerates the subscriptions into slices
        
        This method is protected.
        """
        ...

    def CreateSubscription(self, request: QuantConnect.Data.HistoryRequest, history: System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]) -> QuantConnect.Lean.Engine.DataFeeds.Subscription:
        """
        Creates a subscription to process the history request
        
        This method is protected.
        """
        ...


class SineHistoryProvider(QuantConnect.Data.HistoryProviderBase):
    """Implements a History provider that always return a IEnumerable of Slice with prices following a sine function"""

    @property
    def DataPointCount(self) -> int:
        """Gets the total number of data points emitted by this history provider"""
        ...

    def __init__(self, securities: QuantConnect.Securities.SecurityManager) -> None:
        """
        Initializes a new instance of the SineHistoryProvider class
        
        :param securities: Collection of securities that a history request can return
        """
        ...

    def Initialize(self, parameters: QuantConnect.Data.HistoryProviderInitializeParameters) -> None:
        """
        Initializes this history provider to work for the specified job
        
        :param parameters: The initialization parameters
        """
        ...

    def GetHistory(self, requests: System.Collections.Generic.IEnumerable[QuantConnect.Data.HistoryRequest], sliceTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]:
        """
        Gets the history for the requested securities
        
        :param requests: The historical data requests
        :param sliceTimeZone: The time zone used when time stamping the slice instances
        :returns: An enumerable of the slices of data covering the span specified in each request.
        """
        ...


class SubscriptionDataReaderHistoryProvider(QuantConnect.Lean.Engine.HistoricalData.SynchronizingHistoryProvider):
    """
    Provides an implementation of IHistoryProvider that uses BaseData
    instances to retrieve historical data
    """

    def Initialize(self, parameters: QuantConnect.Data.HistoryProviderInitializeParameters) -> None:
        """
        Initializes this history provider to work for the specified job
        
        :param parameters: The initialization parameters
        """
        ...

    def GetHistory(self, requests: System.Collections.Generic.IEnumerable[QuantConnect.Data.HistoryRequest], sliceTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]:
        """
        Gets the history for the requested securities
        
        :param requests: The historical data requests
        :param sliceTimeZone: The time zone used when time stamping the slice instances
        :returns: An enumerable of the slices of data covering the span specified in each request.
        """
        ...

    def GetIntradayDataEnumerator(self, rawData: System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData], request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Gets the intraday data enumerator if any
        
        This method is protected.
        """
        ...


class BrokerageHistoryProvider(QuantConnect.Lean.Engine.HistoricalData.SynchronizingHistoryProvider):
    """
    Provides an implementation of IHistoryProvider that relies on
    a brokerage connection to retrieve historical data
    """

    def SetBrokerage(self, brokerage: QuantConnect.Interfaces.IBrokerage) -> None:
        """
        Sets the brokerage to be used for historical requests
        
        :param brokerage: The brokerage instance
        """
        ...

    def Initialize(self, parameters: QuantConnect.Data.HistoryProviderInitializeParameters) -> None:
        """
        Initializes this history provider to work for the specified job
        
        :param parameters: The initialization parameters
        """
        ...

    def GetHistory(self, requests: System.Collections.Generic.IEnumerable[QuantConnect.Data.HistoryRequest], sliceTimeZone: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.Slice]:
        """
        Gets the history for the requested securities
        
        :param requests: The historical data requests
        :param sliceTimeZone: The time zone used when time stamping the slice instances
        :returns: An enumerable of the slices of data covering the span specified in each request.
        """
        ...


