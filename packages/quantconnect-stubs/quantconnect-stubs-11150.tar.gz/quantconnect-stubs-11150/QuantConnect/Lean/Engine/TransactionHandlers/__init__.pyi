import abc
import datetime
import typing

import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.Results
import QuantConnect.Lean.Engine.TransactionHandlers
import QuantConnect.Orders
import QuantConnect.Securities
import System
import System.Collections.Concurrent
import System.Collections.Generic

System_EventHandler = typing.Any


class ITransactionHandler(QuantConnect.Securities.IOrderProcessor, QuantConnect.Securities.IOrderEventProvider, metaclass=abc.ABCMeta):
    """
    Transaction handlers define how the transactions are processed and set the order fill information.
    The pass this information back to the algorithm portfolio and ensure the cash and portfolio are synchronized.
    """

    @property
    @abc.abstractmethod
    def IsActive(self) -> bool:
        """
        Boolean flag indicating the thread is busy.
        False indicates it is completely finished processing and ready to be terminated.
        """
        ...

    @property
    @abc.abstractmethod
    def Orders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]:
        """Gets the permanent storage for all orders"""
        ...

    @property
    @abc.abstractmethod
    def OrderEvents(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Orders.OrderEvent]:
        """Gets all order events"""
        ...

    @property
    @abc.abstractmethod
    def OrderTickets(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.OrderTicket]:
        """Gets the permanent storage for all order tickets"""
        ...

    def Initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm, brokerage: QuantConnect.Interfaces.IBrokerage, resultHandler: QuantConnect.Lean.Engine.Results.IResultHandler) -> None:
        """Initializes the transaction handler for the specified algorithm using the specified brokerage implementation"""
        ...

    def Exit(self) -> None:
        """Signal a end of thread request to stop montioring the transactions."""
        ...

    def ProcessSynchronousEvents(self) -> None:
        """Process any synchronous events from the primary algorithm thread."""
        ...

    def AddOpenOrder(self, order: QuantConnect.Orders.Order, orderTicket: QuantConnect.Orders.OrderTicket) -> None:
        """Register an already open Order"""
        ...


class CancelPendingOrders(System.Object):
    """Class used to keep track of CancelPending orders and their original or updated status"""

    @property
    def GetCancelPendingOrdersSize(self) -> int:
        """Amount of CancelPending Orders"""
        ...

    def Set(self, orderId: int, status: QuantConnect.Orders.OrderStatus) -> None:
        """
        Adds an order which will be canceled and we want to keep track of it Status in case of fallback
        
        :param orderId: The order id
        :param status: The order Status, before the cancel request
        """
        ...

    def UpdateOrRemove(self, orderId: int, newStatus: QuantConnect.Orders.OrderStatus) -> None:
        """
        Updates an order that is pending to be canceled.
        
        :param orderId: The id of the order
        :param newStatus: The new status of the order. If its OrderStatus.Canceled or OrderStatus.Filled it will be removed
        """
        ...

    def RemoveAndFallback(self, order: QuantConnect.Orders.Order) -> None:
        """
        Removes an order which we failed to cancel and falls back the order Status to previous value
        
        :param order: The order that failed to be canceled
        """
        ...


class BrokerageTransactionHandler(System.Object, QuantConnect.Lean.Engine.TransactionHandlers.ITransactionHandler):
    """Transaction handler for all brokerages"""

    @property
    def _orderRequestQueue(self) -> QuantConnect.Interfaces.IBusyCollection[QuantConnect.Orders.OrderRequest]:
        """
        OrderQueue holds the newly updated orders from the user algorithm waiting to be processed. Once
        orders are processed they are moved into the Orders queue awaiting the brokerage response.
        
        This field is protected.
        """
        ...

    @_orderRequestQueue.setter
    def _orderRequestQueue(self, value: QuantConnect.Interfaces.IBusyCollection[QuantConnect.Orders.OrderRequest]):
        """
        OrderQueue holds the newly updated orders from the user algorithm waiting to be processed. Once
        orders are processed they are moved into the Orders queue awaiting the brokerage response.
        
        This field is protected.
        """
        ...

    @property
    def _cancelPendingOrders(self) -> QuantConnect.Lean.Engine.TransactionHandlers.CancelPendingOrders:
        """
        The _cancelPendingOrders instance will help to keep track of CancelPending orders and their Status
        
        This field is protected.
        """
        ...

    @property
    def NewOrderEvent(self) -> typing.List[System_EventHandler]:
        """Event fired when there is a new OrderEvent"""
        ...

    @NewOrderEvent.setter
    def NewOrderEvent(self, value: typing.List[System_EventHandler]):
        """Event fired when there is a new OrderEvent"""
        ...

    @property
    def Orders(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.Order]:
        """Gets the permanent storage for all orders"""
        ...

    @property
    def OrderEvents(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Orders.OrderEvent]:
        """Gets all order events"""
        ...

    @property
    def OrderTickets(self) -> System.Collections.Concurrent.ConcurrentDictionary[int, QuantConnect.Orders.OrderTicket]:
        """Gets the permanent storage for all order tickets"""
        ...

    @property
    def OrdersCount(self) -> int:
        """Gets the current number of orders that have been processed"""
        ...

    @property
    def IsActive(self) -> bool:
        """
        Boolean flag indicating the Run thread method is busy.
        False indicates it is completely finished processing and ready to be terminated.
        """
        ...

    @IsActive.setter
    def IsActive(self, value: bool):
        """
        Boolean flag indicating the Run thread method is busy.
        False indicates it is completely finished processing and ready to be terminated.
        """
        ...

    @property
    def TimeSinceLastFill(self) -> datetime.timedelta:
        """
        Gets the amount of time since the last call to algorithm.Portfolio.ProcessFill(fill)
        
        This property is protected.
        """
        ...

    @property
    def CurrentTimeUtc(self) -> datetime.datetime:
        """
        Gets current time UTC. This is here to facilitate testing
        
        This property is protected.
        """
        ...

    def Initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm, brokerage: QuantConnect.Interfaces.IBrokerage, resultHandler: QuantConnect.Lean.Engine.Results.IResultHandler) -> None:
        """
        Creates a new BrokerageTransactionHandler to process orders using the specified brokerage implementation
        
        :param algorithm: The algorithm instance
        :param brokerage: The brokerage implementation to process orders and fire fill events
        """
        ...

    def InitializeTransactionThread(self) -> None:
        """
        Create and start the transaction thread, who will be in charge of processing
        the order requests
        
        This method is protected.
        """
        ...

    def Process(self, request: QuantConnect.Orders.OrderRequest) -> QuantConnect.Orders.OrderTicket:
        ...

    def AddOrder(self, request: QuantConnect.Orders.SubmitOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """
        Add an order to collection and return the unique order id or negative if an error.
        
        :param request: A request detailing the order to be submitted
        :returns: New unique, increasing orderid.
        """
        ...

    def WaitForOrderSubmission(self, ticket: QuantConnect.Orders.OrderTicket) -> None:
        """
        Wait for the order to be handled by the _processingThread
        
        This method is protected.
        
        :param ticket: The OrderTicket expecting to be submitted
        """
        ...

    def UpdateOrder(self, request: QuantConnect.Orders.UpdateOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """
        Update an order yet to be filled such as stop or limit orders.
        
        :param request: Request detailing how the order should be updated
        """
        ...

    def CancelOrder(self, request: QuantConnect.Orders.CancelOrderRequest) -> QuantConnect.Orders.OrderTicket:
        """
        Remove this order from outstanding queue: user is requesting a cancel.
        
        :param request: Request containing the specific order id to remove
        """
        ...

    def GetOrderTickets(self, filter: typing.Callable[[QuantConnect.Orders.OrderTicket], bool] = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Orders.OrderTicket]:
        """
        Gets and enumerable of OrderTicket matching the specified
        
        :param filter: The filter predicate used to find the required order tickets
        :returns: An enumerable of OrderTicket matching the specified.
        """
        ...

    def GetOpenOrderTickets(self, filter: typing.Callable[[QuantConnect.Orders.OrderTicket], bool] = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Orders.OrderTicket]:
        """
        Gets and enumerable of opened OrderTicket matching the specified
        
        :param filter: The filter predicate used to find the required order tickets
        :returns: An enumerable of opened OrderTicket matching the specified.
        """
        ...

    def GetOrderTicket(self, orderId: int) -> QuantConnect.Orders.OrderTicket:
        """
        Gets the order ticket for the specified order id. Returns null if not found
        
        :param orderId: The order's id
        :returns: The order ticket with the specified id, or null if not found.
        """
        ...

    def GetOrderById(self, orderId: int) -> QuantConnect.Orders.Order:
        ...

    def GetOrderByBrokerageId(self, brokerageId: str) -> QuantConnect.Orders.Order:
        """
        Gets the order by its brokerage id
        
        :param brokerageId: The brokerage id to fetch
        :returns: The first order matching the brokerage id, or null if no match is found.
        """
        ...

    def GetOrders(self, filter: typing.Callable[[QuantConnect.Orders.Order], bool] = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Orders.Order]:
        """
        Gets all orders matching the specified filter. Specifying null will return an enumerable
        of all orders.
        
        :param filter: Delegate used to filter the orders
        :returns: All orders this order provider currently holds by the specified filter.
        """
        ...

    def GetOpenOrders(self, filter: typing.Callable[[QuantConnect.Orders.Order], bool] = None) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets open orders matching the specified filter
        
        :param filter: Delegate used to filter the orders
        :returns: All open orders this order provider currently holds.
        """
        ...

    def Run(self) -> None:
        """
        Primary thread entry point to launch the transaction thread.
        
        This method is protected.
        """
        ...

    def ProcessAsynchronousEvents(self) -> None:
        """Processes asynchronous events on the transaction handler's thread"""
        ...

    def ProcessSynchronousEvents(self) -> None:
        """Processes all synchronous events that must take place before the next time loop for the algorithm"""
        ...

    def AddOpenOrder(self, order: QuantConnect.Orders.Order, orderTicket: QuantConnect.Orders.OrderTicket) -> None:
        """Register an already open Order"""
        ...

    def Exit(self) -> None:
        """Signal a end of thread request to stop monitoring the transactions."""
        ...

    def HandleOrderRequest(self, request: QuantConnect.Orders.OrderRequest) -> None:
        """
        Handles a generic order request
        
        :param request: OrderRequest to be handled
        :returns: OrderResponse for request.
        """
        ...

    def RoundOffOrder(self, order: QuantConnect.Orders.Order, security: QuantConnect.Securities.Security) -> float:
        """Rounds off the order towards 0 to the nearest multiple of Lot Size"""
        ...

    def RoundOrderPrices(self, order: QuantConnect.Orders.Order, security: QuantConnect.Securities.Security) -> None:
        """
        Rounds the order prices to its security minimum price variation.
        
        This procedure is needed to meet brokerage precision requirements.
        
        This method is protected.
        """
        ...


class BacktestingTransactionHandler(QuantConnect.Lean.Engine.TransactionHandlers.BrokerageTransactionHandler):
    """This transaction handler is used for processing transactions during backtests"""

    def Initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm, brokerage: QuantConnect.Interfaces.IBrokerage, resultHandler: QuantConnect.Lean.Engine.Results.IResultHandler) -> None:
        """
        Creates a new BacktestingTransactionHandler using the BacktestingBrokerage
        
        :param algorithm: The algorithm instance
        :param brokerage: The BacktestingBrokerage
        """
        ...

    def ProcessSynchronousEvents(self) -> None:
        """Processes all synchronous events that must take place before the next time loop for the algorithm"""
        ...

    def ProcessAsynchronousEvents(self) -> None:
        """Processes asynchronous events on the transaction handler's thread"""
        ...

    def WaitForOrderSubmission(self, ticket: QuantConnect.Orders.OrderTicket) -> None:
        """
        For backtesting we will submit the order ourselves
        
        This method is protected.
        
        :param ticket: The OrderTicket expecting to be submitted
        """
        ...

    def InitializeTransactionThread(self) -> None:
        """
        For backtesting order requests will be processed by the algorithm thread
        sequentially at WaitForOrderToBeProcess and ProcessSynchronousEvents
        
        This method is protected.
        """
        ...


