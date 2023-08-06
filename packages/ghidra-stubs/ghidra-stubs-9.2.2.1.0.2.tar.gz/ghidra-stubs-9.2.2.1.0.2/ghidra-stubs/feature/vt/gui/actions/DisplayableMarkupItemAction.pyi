import ghidra.feature.vt.api.main
import java.lang


class DisplayableMarkupItemAction(object):
    ADD_ACTION: ghidra.feature.vt.gui.actions.DisplayableMarkupItemAction = ghidra.feature.vt.gui.actions.DisplayableMarkupItemAction@34e973c
    EXCLUDE_ACTION: ghidra.feature.vt.gui.actions.DisplayableMarkupItemAction = ghidra.feature.vt.gui.actions.DisplayableMarkupItemAction@6628bce
    REPLACE_ACTION: ghidra.feature.vt.gui.actions.DisplayableMarkupItemAction = ghidra.feature.vt.gui.actions.DisplayableMarkupItemAction@93dad3c







    def equals(self, __a0: object) -> bool: ...

    def getAction(self) -> ghidra.feature.vt.api.main.VTMarkupItemApplyActionType: ...

    def getClass(self) -> java.lang.Class: ...

    def getDisplayString(self) -> unicode: ...

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

    @property
    def action(self) -> ghidra.feature.vt.api.main.VTMarkupItemApplyActionType: ...

    @property
    def displayString(self) -> unicode: ...