import dataclasses as dc
import typing
import inspect


class XMonadBase:
    def __init__(self, cls: type):
        self._cls = cls

    @property
    def __xm_declare__(self):
        return ""

    def __repr(self):
        _args = inspect.getargspec(self._cls.__init__)
        if len(_args.args) == 0:
            return f"{self._cls.__name__}()"
        elif len(_args.args) >= 2:
            _argsMap = ""
            for i in range(1, len(_args.args)):
                _argsMap += _args.args[i]
                if _args.args[i] != _args.args[-1]:
                    _argsMap += ", "
            return f"{self._cls.__name__}({_argsMap})"


def _validateType(func):
    def inner(*args, **kwargs):
        assert isinstance(kwargs["dataType"], type)
        assert type(kwargs["val"]) == kwargs["dataType"]
        return func(*args, **kwargs)

    return inner


@dc.dataclass(init=True, eq=True, repr=True)
class Variable(XMonadBase):
    var: str
    val: typing.Any
    dataType: type

    @_validateType
    def __init__(self, var: str, val: typing.Any, dataType: type):
        # TODO: Check for AssertionError on self.__call__() throw from _validType() method
        super(XMonadBase, self)
        self.var = var
        self.val = val
        self.dataType = dataType


class XMonadImport:
    def __init__(self, namespace: str, qualified: bool = False):
        self._namespace = namespace
        self._qualified = qualified

    def __str__(self, *args, **kwargs) -> str:
        return "import " + ("qualified" if self.qualified else "") + self.namespace

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def qualified(self) -> str:
        return self._qualified


class XMonad:
    def __init__(self, configPath: str = None):
        self._configPath = (
            configPath if (configPath != "" or configPath is not None) else "xmonad.hs"
        )
        self._imports = [
            XMonadImport(namespace="Xmonad", qualified=False),
        ]

    @property
    def configPath(self) -> str:
        return self.configPath

    @property
    def imports(self) -> list:
        return self._imports

    def imports(self, *imports: XMonadImport) -> None:
        for i in imports:
            self._imports.append(i)

    def addImport(self, *args, **kwargs):
        self._imports.append(XMonadImport(*args, **kwargs))
