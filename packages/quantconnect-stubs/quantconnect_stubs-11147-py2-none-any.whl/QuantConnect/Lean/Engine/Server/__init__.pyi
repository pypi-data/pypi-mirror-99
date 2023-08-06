import abc

import QuantConnect.Interfaces
import QuantConnect.Lean.Engine
import QuantConnect.Lean.Engine.Server
import QuantConnect.Packets
import System


class ILeanManager(System.IDisposable, metaclass=abc.ABCMeta):
    """Provides scope into Lean that is convenient for managing a lean instance"""

    def Initialize(self, systemHandlers: QuantConnect.Lean.Engine.LeanEngineSystemHandlers, algorithmHandlers: QuantConnect.Lean.Engine.LeanEngineAlgorithmHandlers, job: QuantConnect.Packets.AlgorithmNodePacket, algorithmManager: QuantConnect.Lean.Engine.AlgorithmManager) -> None:
        """
        Initialize the ILeanManager implementation
        
        :param systemHandlers: Exposes lean engine system handlers running LEAN
        :param algorithmHandlers: Exposes the lean algorithm handlers running lean
        :param job: The job packet representing either a live or backtest Lean instance
        :param algorithmManager: The Algorithm manager
        """
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Sets the IAlgorithm instance in the ILeanManager
        
        :param algorithm: The IAlgorithm instance being run
        """
        ...

    def Update(self) -> None:
        """Update ILeanManager with the IAlgorithm instance"""
        ...

    def OnAlgorithmStart(self) -> None:
        """This method is called after algorithm initialization"""
        ...

    def OnAlgorithmEnd(self) -> None:
        """This method is called before algorithm termination"""
        ...


class LocalLeanManager(System.Object, QuantConnect.Lean.Engine.Server.ILeanManager):
    """NOP implementation of the ILeanManager interface"""

    def Initialize(self, systemHandlers: QuantConnect.Lean.Engine.LeanEngineSystemHandlers, algorithmHandlers: QuantConnect.Lean.Engine.LeanEngineAlgorithmHandlers, job: QuantConnect.Packets.AlgorithmNodePacket, algorithmManager: QuantConnect.Lean.Engine.AlgorithmManager) -> None:
        """
        Empty implementation of the ILeanManager interface
        
        :param systemHandlers: Exposes lean engine system handlers running LEAN
        :param algorithmHandlers: Exposes the lean algorithm handlers running lean
        :param job: The job packet representing either a live or backtest Lean instance
        :param algorithmManager: The Algorithm manager
        """
        ...

    def SetAlgorithm(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        """
        Sets the IAlgorithm instance in the ILeanManager
        
        :param algorithm: The IAlgorithm instance being run
        """
        ...

    def Update(self) -> None:
        """Update ILeanManager with the IAlgorithm instance"""
        ...

    def OnAlgorithmStart(self) -> None:
        """This method is called after algorithm initialization"""
        ...

    def OnAlgorithmEnd(self) -> None:
        """This method is called before algorithm termination"""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...


