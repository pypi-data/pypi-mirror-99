import System
import System.Configuration.Assemblies


class AssemblyVersionCompatibility(System.Enum):
    """This class has no documentation."""

    SameMachine = 1

    SameProcess = 2

    SameDomain = 3


class AssemblyHashAlgorithm(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    MD5 = ...

    SHA1 = ...

    SHA256 = ...

    SHA384 = ...

    SHA512 = ...


