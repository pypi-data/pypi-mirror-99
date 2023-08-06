import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.DataFeeds.Queues
import QuantConnect.Packets
import System
import System.Collections.Generic

System_EventHandler = typing.Any


class FakeDataQueue(System.Object, QuantConnect.Interfaces.IDataQueueHandler):
    """This is an implementation of IDataQueueHandler used for testing"""

    @property
    def TimeProvider(self) -> QuantConnect.ITimeProvider:
        """
        Continuous UTC time provider
        
        This property is protected.
        """
        ...

    @property
    def IsConnected(self) -> bool:
        """Returns whether the data provider is connected"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new instance of the FakeDataQueue class to randomly emit data for each symbol"""
        ...

    @typing.overload
    def __init__(self, dataAggregator: QuantConnect.Data.IDataAggregator) -> None:
        """Initializes a new instance of the FakeDataQueue class to randomly emit data for each symbol"""
        ...

    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: System_EventHandler) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request.
        """
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Sets the job we're subscribing for
        
        :param job: Job we're subscribing for
        """
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


class LiveDataQueue(System.Object, QuantConnect.Interfaces.IDataQueueHandler):
    """Live Data Queue is the cut out implementation of how to bind a custom live data source"""

    @property
    def IsConnected(self) -> bool:
        """Returns whether the data provider is connected"""
        ...

    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: System_EventHandler) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """Desktop/Local doesn't support live data from this handler"""
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """Desktop/Local doesn't support live data from this handler"""
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Sets the job we're subscribing for
        
        :param job: Job we're subscribing for
        """
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


