import ghidra.framework
import java.lang


class ShutdownPriority(object):
    DISPOSE_DATABASES: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@7d6ce8ae
    DISPOSE_FILE_HANDLES: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@d7714d7
    FIRST: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@6335a6af
    LAST: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@5651c7b2
    SHUTDOWN_LOGGING: ghidra.framework.ShutdownPriority = ghidra.framework.ShutdownPriority@3455c5d3







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

