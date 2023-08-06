from typing import List
import java.lang


class MultipleProgramsStrategy(object):
    ALL_PROGRAMS: ghidra.app.util.importer.MultipleProgramsStrategy = ghidra.app.util.importer.MultipleProgramsStrategy$1@30d89abd
    ONE_PROGRAM_OR_EXCEPTION: ghidra.app.util.importer.MultipleProgramsStrategy = ghidra.app.util.importer.MultipleProgramsStrategy$2@3642a366
    ONE_PROGRAM_OR_NULL: ghidra.app.util.importer.MultipleProgramsStrategy = ghidra.app.util.importer.MultipleProgramsStrategy$3@6195647







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def handlePrograms(self, __a0: List[object], __a1: object) -> List[object]: ...

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

