import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Orders.Fees
import QuantConnect.Orders.Fills
import QuantConnect.Orders.OptionExercise
import QuantConnect.Orders.Slippage
import QuantConnect.Securities
import QuantConnect.Securities.Future
import QuantConnect.Securities.Interfaces
import QuantConnect.Securities.Option
import System
import System.Collections.Generic

GeneralizedBlackScholesProcess = typing.Any
IPricingEngine = typing.Any
QuantConnect_Securities_Option_OptionStrategy_LegData = typing.Any


class OptionMarginModel(QuantConnect.Securities.SecurityMarginModel):
    """Represents a simple option margin model."""

    def __init__(self, requiredFreeBuyingPowerPercent: float = 0) -> None:
        """
        Initializes a new instance of the OptionMarginModel
        
        :param requiredFreeBuyingPowerPercent: The percentage used to determine the required unused buying power for the account.
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the current leverage of the security
        
        :param security: The security to get leverage for
        :returns: The current leverage in the security.
        """
        ...

    def SetLeverage(self, security: QuantConnect.Securities.Security, leverage: float) -> None:
        """
        Sets the leverage for the applicable securities, i.e, options.
        
        :param leverage: The new leverage
        """
        ...

    def GetInitialMarginRequiredForOrder(self, parameters: QuantConnect.Securities.InitialMarginRequiredForOrderParameters) -> float:
        """
        Gets the total margin required to execute the specified order in units of the account currency including fees
        
        This method is protected.
        
        :param parameters: An object containing the portfolio, the security and the order
        :returns: The total margin in terms of the currency quoted in the order.
        """
        ...

    def GetMaintenanceMargin(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the margin currently alloted to the specified holding
        
        This method is protected.
        
        :param security: The security to compute maintenance margin for
        :returns: The maintenance margin required for the.
        """
        ...

    def GetInitialMarginRequirement(self, security: QuantConnect.Securities.Security, quantity: float) -> float:
        """
        The margin that must be held in order to increase the position by the provided quantity
        
        This method is protected.
        """
        ...


class OptionPriceModelResult(System.Object):
    """Result type for IOptionPriceModel.Evaluate"""

    @property
    def TheoreticalPrice(self) -> float:
        """Gets the theoretical price as computed by the IOptionPriceModel"""
        ...

    @TheoreticalPrice.setter
    def TheoreticalPrice(self, value: float):
        """Gets the theoretical price as computed by the IOptionPriceModel"""
        ...

    @property
    def ImpliedVolatility(self) -> float:
        """Gets the implied volatility of the option contract"""
        ...

    @property
    def Greeks(self) -> QuantConnect.Data.Market.Greeks:
        """Gets the various sensitivities as computed by the IOptionPriceModel"""
        ...

    @typing.overload
    def __init__(self, theoreticalPrice: float, greeks: QuantConnect.Data.Market.Greeks) -> None:
        """
        Initializes a new instance of the OptionPriceModelResult class
        
        :param theoreticalPrice: The theoretical price computed by the price model
        :param greeks: The sensitivities (greeks) computed by the price model
        """
        ...

    @typing.overload
    def __init__(self, theoreticalPrice: float, impliedVolatility: typing.Callable[[], float], greeks: typing.Callable[[], QuantConnect.Data.Market.Greeks]) -> None:
        """
        Initializes a new instance of the OptionPriceModelResult class with lazy calculations of implied volatility and greeks
        
        :param theoreticalPrice: The theoretical price computed by the price model
        :param impliedVolatility: The calculated implied volatility
        :param greeks: The sensitivities (greeks) computed by the price model
        """
        ...


class IOptionPriceModel(metaclass=abc.ABCMeta):
    """Defines a model used to calculate the theoretical price of an option contract."""

    def Evaluate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        Evaluates the specified option contract to compute a theoretical price, IV and greeks
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...


class OptionSymbolProperties(QuantConnect.Securities.SymbolProperties):
    """Represents common properties for a specific option contract"""

    @property
    def ContractUnitOfTrade(self) -> int:
        """
        When the holder of an equity option exercises one contract, or when the writer of an equity option is assigned
        an exercise notice on one contract, this unit of trade, usually 100 shares of the underlying security, changes hands.
        """
        ...

    @ContractUnitOfTrade.setter
    def ContractUnitOfTrade(self, value: int):
        """
        When the holder of an equity option exercises one contract, or when the writer of an equity option is assigned
        an exercise notice on one contract, this unit of trade, usually 100 shares of the underlying security, changes hands.
        """
        ...

    @property
    def MinimumPriceVariation(self) -> float:
        """
        Overridable minimum price variation, required for index options contracts with
        variable sized quoted prices depending on the premium of the option.
        """
        ...

    @MinimumPriceVariation.setter
    def MinimumPriceVariation(self, value: float):
        """
        Overridable minimum price variation, required for index options contracts with
        variable sized quoted prices depending on the premium of the option.
        """
        ...

    @typing.overload
    def __init__(self, description: str, quoteCurrency: str, contractMultiplier: float, pipSize: float, lotSize: float) -> None:
        """Creates an instance of the OptionSymbolProperties class"""
        ...

    @typing.overload
    def __init__(self, properties: QuantConnect.Securities.SymbolProperties) -> None:
        """Creates an instance of the OptionSymbolProperties class from SymbolProperties class"""
        ...


class Option(QuantConnect.Securities.Security, QuantConnect.Securities.IDerivativeSecurity, QuantConnect.Interfaces.IOptionPrice):
    """Option Security Object Implementation for Option Assets"""

    DefaultSettlementDays: int = 1
    """The default number of days required to settle an equity sale"""

    DefaultSettlementTime: datetime.timedelta = ...
    """The default time of day for settlement"""

    @property
    def IsOptionChain(self) -> bool:
        """Returns true if this is the option chain security, false if it is a specific option contract"""
        ...

    @property
    def IsOptionContract(self) -> bool:
        """Returns true if this is a specific option contract security, false if it is the option chain security"""
        ...

    @property
    def StrikePrice(self) -> float:
        """Gets the strike price"""
        ...

    @property
    def Expiry(self) -> datetime.datetime:
        """Gets the expiration date"""
        ...

    @property
    def Right(self) -> int:
        """
        Gets the right being purchased (call [right to buy] or put [right to sell])
        
        This property contains the int value of a member of the QuantConnect.OptionRight enum.
        """
        ...

    @property
    def Style(self) -> int:
        """
        Gets the option style
        
        This property contains the int value of a member of the QuantConnect.OptionStyle enum.
        """
        ...

    @property
    def BidPrice(self) -> float:
        """Gets the most recent bid price if available"""
        ...

    @property
    def AskPrice(self) -> float:
        """Gets the most recent ask price if available"""
        ...

    @property
    def ContractUnitOfTrade(self) -> int:
        """
        When the holder of an equity option exercises one contract, or when the writer of an equity option is assigned
        an exercise notice on one contract, this unit of trade, usually 100 shares of the underlying security, changes hands.
        """
        ...

    @ContractUnitOfTrade.setter
    def ContractUnitOfTrade(self, value: int):
        """
        When the holder of an equity option exercises one contract, or when the writer of an equity option is assigned
        an exercise notice on one contract, this unit of trade, usually 100 shares of the underlying security, changes hands.
        """
        ...

    @property
    def ContractMultiplier(self) -> int:
        """The contract multiplier for the option security"""
        ...

    @ContractMultiplier.setter
    def ContractMultiplier(self, value: int):
        """The contract multiplier for the option security"""
        ...

    @property
    def ExerciseSettlement(self) -> int:
        """
        Specifies if option contract has physical or cash settlement on exercise
        
        This property contains the int value of a member of the QuantConnect.SettlementType enum.
        """
        ...

    @ExerciseSettlement.setter
    def ExerciseSettlement(self, value: int):
        """
        Specifies if option contract has physical or cash settlement on exercise
        
        This property contains the int value of a member of the QuantConnect.SettlementType enum.
        """
        ...

    @property
    def Underlying(self) -> QuantConnect.Securities.Security:
        """Gets or sets the underlying security object."""
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Securities.Security):
        """Gets or sets the underlying security object."""
        ...

    @property
    def PriceModel(self) -> QuantConnect.Securities.Option.IOptionPriceModel:
        """Gets or sets the price model for this option security"""
        ...

    @PriceModel.setter
    def PriceModel(self, value: QuantConnect.Securities.Option.IOptionPriceModel):
        """Gets or sets the price model for this option security"""
        ...

    @property
    def OptionExerciseModel(self) -> QuantConnect.Orders.OptionExercise.IOptionExerciseModel:
        """Fill model used to produce fill events for this security"""
        ...

    @OptionExerciseModel.setter
    def OptionExerciseModel(self, value: QuantConnect.Orders.OptionExercise.IOptionExerciseModel):
        """Fill model used to produce fill events for this security"""
        ...

    @property
    def EnableGreekApproximation(self) -> bool:
        """When enabled, approximates Greeks if corresponding pricing model didn't calculate exact numbers"""
        ...

    @EnableGreekApproximation.setter
    def EnableGreekApproximation(self, value: bool):
        """When enabled, approximates Greeks if corresponding pricing model didn't calculate exact numbers"""
        ...

    @property
    def ContractFilter(self) -> QuantConnect.Securities.IDerivativeSecurityFilter:
        """Gets or sets the contract filter"""
        ...

    @ContractFilter.setter
    def ContractFilter(self, value: QuantConnect.Securities.IDerivativeSecurityFilter):
        """Gets or sets the contract filter"""
        ...

    @typing.overload
    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours, config: QuantConnect.Data.SubscriptionDataConfig, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.Option.OptionSymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider) -> None:
        """
        Constructor for the option security
        
        :param exchangeHours: Defines the hours this exchange is open
        :param config: The subscription configuration for this security
        :param quoteCurrency: The cash object that represent the quote currency
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.Option.OptionSymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider, securityCache: QuantConnect.Securities.SecurityCache) -> None:
        """
        Constructor for the option security
        
        :param symbol: The symbol of the security
        :param exchangeHours: Defines the hours this exchange is open
        :param quoteCurrency: The cash object that represent the quote currency
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        :param securityCache: Cache to store security information
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.SymbolProperties, exchange: QuantConnect.Securities.SecurityExchange, cache: QuantConnect.Securities.SecurityCache, portfolioModel: QuantConnect.Securities.ISecurityPortfolioModel, fillModel: QuantConnect.Orders.Fills.IFillModel, feeModel: QuantConnect.Orders.Fees.IFeeModel, slippageModel: QuantConnect.Orders.Slippage.ISlippageModel, settlementModel: QuantConnect.Securities.ISettlementModel, volatilityModel: QuantConnect.Securities.IVolatilityModel, buyingPowerModel: QuantConnect.Securities.IBuyingPowerModel, dataFilter: QuantConnect.Securities.Interfaces.ISecurityDataFilter, priceVariationModel: QuantConnect.Securities.IPriceVariationModel, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypesProvider: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider) -> None:
        """
        Creates instance of the Option class.
        
        This method is protected.
        """
        ...

    def GetAggregateExerciseAmount(self) -> float:
        """
        Aggregate exercise amount or aggregate contract value. It is the total amount of cash one will pay (or receive) for the shares of the
        underlying stock if he/she decides to exercise (or is assigned an exercise notice). This amount is not the premium paid or received for an equity option.
        """
        ...

    @typing.overload
    def GetExerciseQuantity(self) -> float:
        """
        Returns the directional quantity of underlying shares that are going to change hands on exercise/assignment of all
        contracts held by this account, taking into account the contract's Right as well as the contract's current
        ContractUnitOfTrade, which may have recently changed due to a split/reverse split in the underlying security.
        """
        ...

    @typing.overload
    def GetExerciseQuantity(self, exerciseOrderQuantity: float) -> float:
        """
        Returns the directional quantity of underlying shares that are going to change hands on exercise/assignment of the
        specified , taking into account the contract's Right as well
        as the contract's current ContractUnitOfTrade, which may have recently changed due to a split/reverse
        split in the underlying security.
        """
        ...

    def IsAutoExercised(self, underlyingPrice: float) -> bool:
        """Checks if option is eligible for automatic exercise on expiration"""
        ...

    def GetIntrinsicValue(self, underlyingPrice: float) -> float:
        """Intrinsic value function of the option"""
        ...

    def GetPayOff(self, underlyingPrice: float) -> float:
        """
        Option payoff function at expiration time
        
        :param underlyingPrice: The price of the underlying
        """
        ...

    def EvaluatePriceModel(self, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        For this option security object, evaluates the specified option
        contract to compute a theoretical price, IV and greeks
        
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...

    @typing.overload
    def SetFilter(self, minStrike: int, maxStrike: int) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike values. Contracts with expirations further than 35
        days out will also be filtered.
        
        :param minStrike: The min strike rank relative to market price, for example, -1 would put a lower bound of one strike under market price, where a +1 would put a lower bound of one strike over market price
        :param maxStrike: The max strike rank relative to market place, for example, -1 would put an upper bound of on strike under market price, where a +1 would be an upper bound of one strike over market price
        """
        ...

    @typing.overload
    def SetFilter(self, minExpiry: datetime.timedelta, maxExpiry: datetime.timedelta) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike and expiration range values
        
        :param minExpiry: The minimum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in more than 10 days
        :param maxExpiry: The maxmium time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in less than 10 days
        """
        ...

    @typing.overload
    def SetFilter(self, minStrike: int, maxStrike: int, minExpiry: datetime.timedelta, maxExpiry: datetime.timedelta) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike and expiration range values
        
        :param minStrike: The min strike rank relative to market price, for example, -1 would put a lower bound of one strike under market price, where a +1 would put a lower bound of one strike over market price
        :param maxStrike: The max strike rank relative to market place, for example, -1 would put an upper bound of on strike under market price, where a +1 would be an upper bound of one strike over market price
        :param minExpiry: The minimum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in more than 10 days
        :param maxExpiry: The maxmium time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in less than 10 days
        """
        ...

    @typing.overload
    def SetFilter(self, minStrike: int, maxStrike: int, minExpiryDays: int, maxExpiryDays: int) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified min and max strike and expiration range values
        
        :param minStrike: The min strike rank relative to market price, for example, -1 would put a lower bound of one strike under market price, where a +1 would put a lower bound of one strike over market price
        :param maxStrike: The max strike rank relative to market place, for example, -1 would put an upper bound of on strike under market price, where a +1 would be an upper bound of one strike over market price
        :param minExpiryDays: The minimum time, expressed in days, until expiry to include, for example, 10 would exclude contracts expiring in more than 10 days
        :param maxExpiryDays: The maximum time, expressed in days, until expiry to include, for example, 10 would exclude contracts expiring in less than 10 days
        """
        ...

    @typing.overload
    def SetFilter(self, universeFunc: typing.Callable[[QuantConnect.Securities.OptionFilterUniverse], QuantConnect.Securities.OptionFilterUniverse]) -> None:
        """
        Sets the ContractFilter to a new universe selection function
        
        :param universeFunc: new universe selection function
        """
        ...

    @typing.overload
    def SetFilter(self, universeFunc: typing.Any) -> None:
        """
        Sets the ContractFilter to a new universe selection function
        
        :param universeFunc: new universe selection function
        """
        ...

    def SetDataNormalizationMode(self, mode: QuantConnect.DataNormalizationMode) -> None:
        """Sets the data normalization mode to be used by this security"""
        ...


class OptionHolding(QuantConnect.Securities.SecurityHolding):
    """Option holdings implementation of the base securities class"""

    def __init__(self, security: QuantConnect.Securities.Option.Option, currencyConverter: QuantConnect.Securities.ICurrencyConverter) -> None:
        """
        Option Holding Class constructor
        
        :param security: The option security being held
        :param currencyConverter: A currency converter instance
        """
        ...


class OptionSymbol(System.Object):
    """Static class contains common utility methods specific to symbols representing the option contracts"""

    @staticmethod
    def IsStandardContract(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if the option is a standard contract that expires 3rd Friday of the month
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def IsStandard(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if the option is a standard contract that expires 3rd Friday of the month
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def IsWeekly(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if the option is a weekly contract that expires on Friday , except 3rd Friday of the month
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def GetLastDayOfTrading(symbol: typing.Union[QuantConnect.Symbol, str]) -> datetime.datetime:
        """
        Returns the last trading date for the option contract
        
        :param symbol: Option symbol
        """
        ...

    @staticmethod
    def IsOptionContractExpired(symbol: typing.Union[QuantConnect.Symbol, str], currentTimeUtc: datetime.datetime) -> bool:
        """
        Returns true if the option contract is expired at the specified time
        
        :param symbol: The option contract symbol
        :param currentTimeUtc: The current time (UTC)
        :returns: True if the option contract is expired at the specified time, false otherwise.
        """
        ...


class IQLDividendYieldEstimator(metaclass=abc.ABCMeta):
    """
    Defines QuantLib dividend yield estimator for option pricing model. User may define his own estimators,
    including those forward and backward looking ones.
    """

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current estimate of the stock dividend yield
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: Dividend yield.
        """
        ...


class IQLUnderlyingVolatilityEstimator(metaclass=abc.ABCMeta):
    """
    Defines QuantLib underlying volatility estimator for option pricing model. User may define his own estimators,
    including those forward and backward looking ones.
    """

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current estimate of the underlying volatility
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: Volatility.
        """
        ...


class IQLRiskFreeRateEstimator(metaclass=abc.ABCMeta):
    """Defines QuantLib risk free rate estimator for option pricing model."""

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current estimate of the risk free rate
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: Risk free rate.
        """
        ...


class QLOptionPriceModel(System.Object, QuantConnect.Securities.Option.IOptionPriceModel):
    """Provides QuantLib(QL) implementation of IOptionPriceModel to support major option pricing models, available in QL."""

    @property
    def EnableGreekApproximation(self) -> bool:
        """
        When enabled, approximates Greeks if corresponding pricing model didn't calculate exact numbers.
        The default value is true.
        """
        ...

    @EnableGreekApproximation.setter
    def EnableGreekApproximation(self, value: bool):
        """
        When enabled, approximates Greeks if corresponding pricing model didn't calculate exact numbers.
        The default value is true.
        """
        ...

    @typing.overload
    def __init__(self, pricingEngineFunc: typing.Callable[[GeneralizedBlackScholesProcess], IPricingEngine], underlyingVolEstimator: QuantConnect.Securities.Option.IQLUnderlyingVolatilityEstimator, riskFreeRateEstimator: QuantConnect.Securities.Option.IQLRiskFreeRateEstimator, dividendYieldEstimator: QuantConnect.Securities.Option.IQLDividendYieldEstimator) -> None:
        """
        Method constructs QuantLib option price model with necessary estimators of underlying volatility, risk free rate, and underlying dividend yield
        
        :param pricingEngineFunc: Function modeled stochastic process, and returns new pricing engine to run calculations for that option
        :param underlyingVolEstimator: The underlying volatility estimator
        :param riskFreeRateEstimator: The risk free rate estimator
        :param dividendYieldEstimator: The underlying dividend yield estimator
        """
        ...

    @typing.overload
    def __init__(self, pricingEngineFunc: typing.Callable[[QuantConnect.Symbol, GeneralizedBlackScholesProcess], IPricingEngine], underlyingVolEstimator: QuantConnect.Securities.Option.IQLUnderlyingVolatilityEstimator, riskFreeRateEstimator: QuantConnect.Securities.Option.IQLRiskFreeRateEstimator, dividendYieldEstimator: QuantConnect.Securities.Option.IQLDividendYieldEstimator) -> None:
        """
        Method constructs QuantLib option price model with necessary estimators of underlying volatility, risk free rate, and underlying dividend yield
        
        :param pricingEngineFunc: Function takes option and modeled stochastic process, and returns new pricing engine to run calculations for that option
        :param underlyingVolEstimator: The underlying volatility estimator
        :param riskFreeRateEstimator: The risk free rate estimator
        :param dividendYieldEstimator: The underlying dividend yield estimator
        """
        ...

    def Evaluate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        Evaluates the specified option contract to compute a theoretical price, IV and greeks
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...


class OptionCache(QuantConnect.Securities.SecurityCache):
    """Option specific caching support"""


class OptionStrategy(System.Object):
    """Option strategy specification class. Describes option strategy and its parameters for trading."""

    class LegData(System.Object, metaclass=abc.ABCMeta):
        """Defines common properties between OptionLegData and UnderlyingLegData"""

        @property
        def Symbol(self) -> QuantConnect.Symbol:
            """
            This is an optional parameter that, if not specified, is resolved by the algorithm's base class.
            If the strategy is produced via the OptionStrategyMatcher, then this will be populated.
            """
            ...

        @Symbol.setter
        def Symbol(self, value: QuantConnect.Symbol):
            """
            This is an optional parameter that, if not specified, is resolved by the algorithm's base class.
            If the strategy is produced via the OptionStrategyMatcher, then this will be populated.
            """
            ...

        @property
        def Quantity(self) -> int:
            """Quantity multiplier used to specify proper scale (and direction) of the leg within the strategy"""
            ...

        @Quantity.setter
        def Quantity(self, value: int):
            """Quantity multiplier used to specify proper scale (and direction) of the leg within the strategy"""
            ...

        @property
        def OrderType(self) -> int:
            """
            Type of order that is to be sent to the market on strategy execution
            
            This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
            """
            ...

        @OrderType.setter
        def OrderType(self, value: int):
            """
            Type of order that is to be sent to the market on strategy execution
            
            This property contains the int value of a member of the QuantConnect.Orders.OrderType enum.
            """
            ...

        @property
        def OrderPrice(self) -> float:
            """Order limit price of the leg in case limit order is sent to the market on strategy execution"""
            ...

        @OrderPrice.setter
        def OrderPrice(self, value: float):
            """Order limit price of the leg in case limit order is sent to the market on strategy execution"""
            ...

        def Invoke(self, underlyingHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData], None], optionHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.OptionLegData], None]) -> None:
            """Invokes the correct handler based on the runtime type."""
            ...

    class OptionLegData(QuantConnect_Securities_Option_OptionStrategy_LegData):
        """This class is a POCO containing basic data for the option legs of the strategy"""

        @property
        def Right(self) -> int:
            """
            Option right (type) of the option leg
            
            This property contains the int value of a member of the QuantConnect.OptionRight enum.
            """
            ...

        @Right.setter
        def Right(self, value: int):
            """
            Option right (type) of the option leg
            
            This property contains the int value of a member of the QuantConnect.OptionRight enum.
            """
            ...

        @property
        def Expiration(self) -> datetime.datetime:
            """Expiration date of the leg"""
            ...

        @Expiration.setter
        def Expiration(self, value: datetime.datetime):
            """Expiration date of the leg"""
            ...

        @property
        def Strike(self) -> float:
            """Strike price of the leg"""
            ...

        @Strike.setter
        def Strike(self, value: float):
            """Strike price of the leg"""
            ...

        @staticmethod
        def Create(quantity: int, symbol: typing.Union[QuantConnect.Symbol, str], orderType: QuantConnect.Orders.OrderType = ..., orderPrice: typing.Optional[float] = None) -> QuantConnect.Securities.Option.OptionStrategy.OptionLegData:
            """Creates a new instance of OptionLegData from the specified parameters"""
            ...

        def Invoke(self, underlyingHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData], None], optionHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.OptionLegData], None]) -> None:
            """Invokes the"""
            ...

    class UnderlyingLegData(QuantConnect_Securities_Option_OptionStrategy_LegData):
        """This class is a POCO containing basic data for the underlying leg of the strategy"""

        @staticmethod
        @typing.overload
        def Create(quantity: int, symbol: typing.Union[QuantConnect.Symbol, str], orderType: QuantConnect.Orders.OrderType = ..., orderPrice: typing.Optional[float] = None) -> QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData:
            """Creates a new instance of UnderlyingLegData for the specified  of underlying shares."""
            ...

        @staticmethod
        @typing.overload
        def Create(quantity: int, orderType: QuantConnect.Orders.OrderType = ..., orderPrice: typing.Optional[float] = None) -> QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData:
            """Creates a new instance of UnderlyingLegData for the specified  of underlying shares."""
            ...

        def Invoke(self, underlyingHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData], None], optionHandler: typing.Callable[[QuantConnect.Securities.Option.OptionStrategy.OptionLegData], None]) -> None:
            """Invokes the"""
            ...

    @property
    def Name(self) -> str:
        """Option strategy name"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Option strategy name"""
        ...

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        """Underlying symbol of the strategy"""
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Symbol):
        """Underlying symbol of the strategy"""
        ...

    @property
    def OptionLegs(self) -> System.Collections.Generic.List[QuantConnect.Securities.Option.OptionStrategy.OptionLegData]:
        """Option strategy legs"""
        ...

    @OptionLegs.setter
    def OptionLegs(self, value: System.Collections.Generic.List[QuantConnect.Securities.Option.OptionStrategy.OptionLegData]):
        """Option strategy legs"""
        ...

    @property
    def UnderlyingLegs(self) -> System.Collections.Generic.List[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData]:
        """Option strategy underlying legs (usually 0 or 1 legs)"""
        ...

    @UnderlyingLegs.setter
    def UnderlyingLegs(self, value: System.Collections.Generic.List[QuantConnect.Securities.Option.OptionStrategy.UnderlyingLegData]):
        """Option strategy underlying legs (usually 0 or 1 legs)"""
        ...


class OptionExchange(QuantConnect.Securities.SecurityExchange):
    """Option exchange class - information and helper tools for option exchange properties"""

    @property
    def TradingDaysPerYear(self) -> int:
        """Number of trading days per year for this security, 252."""
        ...

    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> None:
        """
        Initializes a new instance of the OptionExchange class using the specified
        exchange hours to determine open/close times
        
        :param exchangeHours: Contains the weekly exchange schedule plus holidays
        """
        ...


class ConstantQLDividendYieldEstimator(System.Object, QuantConnect.Securities.Option.IQLDividendYieldEstimator):
    """Class implements default flat dividend yield curve estimator, implementing IQLDividendYieldEstimator."""

    def __init__(self, dividendYield: float = 0.00) -> None:
        """Constructor initializes class with constant dividend yield."""
        ...

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current flat estimate of the dividend yield
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: The estimate.
        """
        ...


class CurrentPriceOptionPriceModel(System.Object, QuantConnect.Securities.Option.IOptionPriceModel):
    """
    Provides a default implementation of IOptionPriceModel that does not compute any
    greeks and uses the current price for the theoretical price.
    This is a stub implementation until the real models are implemented
    """

    def Evaluate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> QuantConnect.Securities.Option.OptionPriceModelResult:
        """
        Creates a new OptionPriceModelResult containing the current Security.Price
        and a default, empty instance of first Order Greeks
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: An instance of OptionPriceModelResult containing the theoretical price of the specified option contract.
        """
        ...


class ConstantQLRiskFreeRateEstimator(System.Object, QuantConnect.Securities.Option.IQLRiskFreeRateEstimator):
    """Class implements default flat risk free curve, implementing IQLRiskFreeRateEstimator."""

    def __init__(self, riskFreeRate: float = 0.01) -> None:
        """Constructor initializes class with risk free rate constant"""
        ...

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current flat estimate of the risk free rate
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: The estimate.
        """
        ...


class OptionPortfolioModel(QuantConnect.Securities.SecurityPortfolioModel):
    """
    Provides an implementation of ISecurityPortfolioModel for options that supports
    default fills as well as option exercising.
    """

    def ProcessFill(self, portfolio: QuantConnect.Securities.SecurityPortfolioManager, security: QuantConnect.Securities.Security, fill: QuantConnect.Orders.OrderEvent) -> None:
        """
        Performs application of an OrderEvent to the portfolio
        
        :param portfolio: The algorithm's portfolio
        :param security: Option security
        :param fill: The order event fill object to be applied
        """
        ...

    def ProcessExerciseFill(self, portfolio: QuantConnect.Securities.SecurityPortfolioManager, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, fill: QuantConnect.Orders.OrderEvent) -> None:
        """
        Processes exercise/assignment event to the portfolio
        
        :param portfolio: The algorithm's portfolio
        :param security: Option security
        :param order: The order object to be applied
        :param fill: The order event fill object to be applied
        """
        ...


class ConstantQLUnderlyingVolatilityEstimator(System.Object, QuantConnect.Securities.Option.IQLUnderlyingVolatilityEstimator):
    """
    Class implements default underlying constant volatility estimator (IQLUnderlyingVolatilityEstimator.), that projects the underlying own volatility
    model into corresponding option pricing model.
    """

    def Estimate(self, security: QuantConnect.Securities.Security, slice: QuantConnect.Data.Slice, contract: QuantConnect.Data.Market.OptionContract) -> float:
        """
        Returns current estimate of the underlying volatility
        
        :param security: The option security object
        :param slice: The current data slice. This can be used to access other information available to the algorithm
        :param contract: The option contract to evaluate
        :returns: The estimate.
        """
        ...


class OptionDataFilter(QuantConnect.Securities.SecurityDataFilter):
    """Option packet by packet data filtering mechanism for dynamically detecting bad ticks."""


class OptionStrategies(System.Object):
    """
    Provides methods for creating popular OptionStrategy instances.
    These strategies can be directly bought and sold via:
        QCAlgorithm.Buy(OptionStrategy strategy, int quantity)
        QCAlgorithm.Sell(OptionStrategy strategy, int quantity)
    
    See also OptionStrategyDefinitions
    """

    @staticmethod
    def BearCallSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bear Call Spread strategy, that consists of two calls with the same expiration but different strikes.
        The strike price of the short call is below the strike of the long call. This is a credit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the short call
        :param leg2Strike: The strike price of the long call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def BearPutSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bear Put Spread strategy, that consists of two puts with the same expiration but different strikes.
        The strike price of the short put is below the strike of the long put. This is a debit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the long put
        :param leg2Strike: The strike price of the short put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def BullCallSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bull Call Spread strategy, that consists of two calls with the same expiration but different strikes.
        The strike price of the short call is higher than the strike of the long call. This is a debit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the long call
        :param leg2Strike: The strike price of the short call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def BullPutSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Bull Put Spread strategy, that consists of two puts with the same expiration but different strikes.
        The strike price of the short put is above the strike of the long put. This is a credit spread.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the short put
        :param leg2Strike: The strike price of the long put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def Straddle(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Straddle strategy, that is a combination of buying a call and buying a put, both with the same strike price and expiration.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def Strangle(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Strangle strategy, that buying a call option and a put option with the same expiration date.
        The strike price of the call is above the strike of the put.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The strike price of the long call
        :param leg2Strike: The strike price of the long put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def CallButterfly(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, leg3Strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Call Butterfly strategy, that consists of two short calls at a middle strike, and one long call each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The upper strike price of the long call
        :param leg2Strike: The middle strike price of the two short calls
        :param leg3Strike: The lower strike price of the long call
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def PutButterfly(canonicalOption: typing.Union[QuantConnect.Symbol, str], leg1Strike: float, leg2Strike: float, leg3Strike: float, expiration: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Put Butterfly strategy, that consists of two short puts at a middle strike, and one long put each at a lower and upper strike.
        The upper and lower strikes must both be equidistant from the middle strike.
        
        :param canonicalOption: Option symbol
        :param leg1Strike: The upper strike price of the long put
        :param leg2Strike: The middle strike price of the two short puts
        :param leg3Strike: The lower strike price of the long put
        :param expiration: Option expiration date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def CallCalendarSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration1: datetime.datetime, expiration2: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Call Calendar Spread strategy, that is a short one call option and long a second call option with a more distant expiration.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param expiration1: Option expiration near date
        :param expiration2: Option expiration far date
        :returns: Option strategy specification.
        """
        ...

    @staticmethod
    def PutCalendarSpread(canonicalOption: typing.Union[QuantConnect.Symbol, str], strike: float, expiration1: datetime.datetime, expiration2: datetime.datetime) -> QuantConnect.Securities.Option.OptionStrategy:
        """
        Method creates new Put Calendar Spread strategy, that is a short one put option and long a second put option with a more distant expiration.
        
        :param canonicalOption: Option symbol
        :param strike: The strike price of the both legs
        :param expiration1: Option expiration near date
        :param expiration2: Option expiration far date
        :returns: Option strategy specification.
        """
        ...


class EmptyOptionChainProvider(System.Object, QuantConnect.Interfaces.IOptionChainProvider):
    """An implementation of IOptionChainProvider that always returns an empty list of contracts"""

    def GetOptionContractList(self, symbol: typing.Union[QuantConnect.Symbol, str], date: datetime.datetime) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Gets the list of option contracts for a given underlying symbol
        
        :param symbol: The underlying symbol
        :param date: The date for which to request the option chain (only used in backtesting)
        :returns: The list of option contracts.
        """
        ...


class OptionPriceModels(System.Object):
    """Static class contains definitions of major option pricing models that can be used in LEAN"""

    @staticmethod
    def BlackScholes() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European vanilla options using analytical formulae.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_analytic_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BaroneAdesiWhaley() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Barone-Adesi and Whaley pricing engine for American options (1987)
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_barone_adesi_whaley_approximation_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BjerksundStensland() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Bjerksund and Stensland pricing engine for American options (1993)
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_bjerksund_stensland_approximation_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def Integral() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European vanilla options using integral approach.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_integral_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def CrankNicolsonFD() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for European options using finite-differences.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialJarrowRudd() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for vanilla options using binomial trees. Jarrow-Rudd model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialCoxRossRubinstein() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for vanilla options using binomial trees. Cox-Ross-Rubinstein(CRR) model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def AdditiveEquiprobabilities() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for vanilla options using binomial trees. Additive Equiprobabilities model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialTrigeorgis() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for vanilla options using binomial trees. Trigeorgis model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialTian() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for vanilla options using binomial trees. Tian model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialLeisenReimer() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for vanilla options using binomial trees. Leisen-Reimer model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...

    @staticmethod
    def BinomialJoshi() -> QuantConnect.Securities.Option.IOptionPriceModel:
        """
        Pricing engine for vanilla options using binomial trees. Joshi model.
        QuantLib reference: http://quantlib.org/reference/class_quant_lib_1_1_f_d_european_engine.html
        
        :returns: New option price model instance.
        """
        ...


class FuturesOptionsMarginModel(QuantConnect.Securities.Future.FutureMarginModel):
    """
    Defines a margin model for future options (an option with a future as its underlying).
    We re-use the FutureMarginModel implementation and multiply its results
    by 1.5x to simulate the increased margins seen for future options.
    """

    def __init__(self, requiredFreeBuyingPowerPercent: float = 0, futureOption: QuantConnect.Securities.Option.Option = None) -> None:
        """
        Creates an instance of FutureOptionMarginModel
        
        :param requiredFreeBuyingPowerPercent: The percentage used to determine the required unused buying power for the account.
        :param futureOption: Option Security containing a Future security as the underlying
        """
        ...

    def GetMaintenanceMargin(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the margin currently alloted to the specified holding.
        
        This method is protected.
        
        :param security: The option to compute maintenance margin for
        :returns: The maintenance margin required for the option.
        """
        ...

    def GetInitialMarginRequirement(self, security: QuantConnect.Securities.Security, quantity: float) -> float:
        """
        The margin that must be held in order to increase the position by the provided quantity
        
        This method is protected.
        
        :param security: The option to compute the initial margin for
        :param quantity: The amount desired
        :returns: The initial margin required for the option (i.e. the equity required to enter a position for this option).
        """
        ...


