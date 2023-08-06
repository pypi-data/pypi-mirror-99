import abc

import QuantConnect.Exceptions
import System
import System.Collections.Generic
import System.Reflection


class IExceptionInterpreter(metaclass=abc.ABCMeta):
    """Defines an exception interpreter. Interpretations are invoked on IAlgorithm.RunTimeError"""

    @property
    @abc.abstractmethod
    def Order(self) -> int:
        """Determines the order that a class that implements this interface should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception. This provides a link back allowing the inner exceptions to be interpreted using the interpreters configured in the IExceptionInterpreter. Individual implementations *may* ignore this value if required.
        :returns: The interpreted exception.
        """
        ...


class DllNotFoundPythonExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets DllNotFoundPythonExceptionInterpreter instances"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception.
        :returns: The interpreted exception.
        """
        ...


class KeyErrorPythonExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets KeyErrorPythonExceptionInterpreter instances"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception.
        :returns: The interpreted exception.
        """
        ...


class PythonExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets PythonExceptionInterpreter instances"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception. f
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception.
        :returns: The interpreted exception.
        """
        ...


class InvalidTokenPythonExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets InvalidTokenPythonExceptionInterpreter instances"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception.
        :returns: The interpreted exception.
        """
        ...


class ScheduledEventExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets ScheduledEventException instances"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception. This provides a link back allowing the inner exceptions to be interpreted using the interpreters configured in the IExceptionInterpreter. Individual implementations *may* ignore this value if required.
        :returns: The interpreted exception.
        """
        ...


class StackExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets exceptions using the configured interpretations"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    @property
    def Interpreters(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Exceptions.IExceptionInterpreter]:
        """Gets the interpreters loaded into this instance"""
        ...

    def __init__(self, interpreters: System.Collections.Generic.IEnumerable[QuantConnect.Exceptions.IExceptionInterpreter]) -> None:
        """
        Initializes a new instance of the StackExceptionInterpreter class
        
        :param interpreters: The interpreters to use
        """
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception. This provides a link back allowing the inner exceptions to be interpreted using the intepretators configured in the StackExceptionInterpreter. Individual implementations *may* ignore this value if required.
        :returns: The interpreted exception.
        """
        ...

    def GetExceptionMessageHeader(self, exception: System.Exception) -> str:
        """
        Combines the exception messages from this exception and all inner exceptions.
        
        :param exception: The exception to create a collated message from
        :returns: The collate exception message.
        """
        ...

    @staticmethod
    def CreateFromAssemblies(assemblies: System.Collections.Generic.IEnumerable[System.Reflection.Assembly]) -> QuantConnect.Exceptions.StackExceptionInterpreter:
        """
        Creates a new StackExceptionInterpreter by loading implementations with default constructors from the specified assemblies
        
        :param assemblies: The assemblies to scan
        :returns: A new StackExceptionInterpreter containing interpreters from the specified assemblies.
        """
        ...


class NoMethodMatchPythonExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets NoMethodMatchPythonExceptionInterpreter instances"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception.
        :returns: The interpreted exception.
        """
        ...


class UnsupportedOperandPythonExceptionInterpreter(System.Object, QuantConnect.Exceptions.IExceptionInterpreter):
    """Interprets UnsupportedOperandPythonExceptionInterpreter instances"""

    @property
    def Order(self) -> int:
        """Determines the order that an instance of this class should be called"""
        ...

    def CanInterpret(self, exception: System.Exception) -> bool:
        """
        Determines if this interpreter should be applied to the specified exception.
        
        :param exception: The exception to check
        :returns: True if the exception can be interpreted, false otherwise.
        """
        ...

    def Interpret(self, exception: System.Exception, innerInterpreter: QuantConnect.Exceptions.IExceptionInterpreter) -> System.Exception:
        """
        Interprets the specified exception into a new exception
        
        :param exception: The exception to be interpreted
        :param innerInterpreter: An interpreter that should be applied to the inner exception.
        :returns: The interpreted exception.
        """
        ...


