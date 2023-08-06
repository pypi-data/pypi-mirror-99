import ghidra.framework
import java.lang


class ShutdownPriority(object):
    DISPOSE_DATABASES: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@334f0a59
    DISPOSE_FILE_HANDLES: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@7a047b26
    FIRST: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@7ab043e0
    LAST: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@23b4dadb
    SHUTDOWN_LOGGING: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@1fba1d6a







    def after(self) -> ghidra.framework.ShutdownPriority: ...

    def before(self) -> ghidra.framework.ShutdownPriority: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

