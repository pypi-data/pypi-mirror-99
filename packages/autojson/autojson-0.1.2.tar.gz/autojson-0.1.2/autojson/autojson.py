from typing import TypeVar, Generic, Union, Any, overload, Iterator
from abc import ABCMeta, abstractmethod

class AutoJson(metaclass=ABCMeta):
    @abstractmethod
    def get_default_json(self):
        obj = self.__class__()
        return obj

    @abstractmethod
    def parse_json(self, json: object):
        return self


class Int(int, AutoJson):
    def get_default_json(self) -> "Int":
        return Int()

    def parse_json(self, json: Union[int, float]):
        if not (isinstance(json, int) or isinstance(json, float)):
            raise TypeError()
        return Int(json)


class Float(float, AutoJson):
    def get_default_json(self) -> "Float":
        return Float()

    def parse_json(self, json: Union[int, float]):
        if not (isinstance(json, int) or isinstance(json, float)):
            raise TypeError()
        return Float(json)


class Boolean(int, AutoJson):
    def __init__(self, value: bool = False):
        self.value = value

    def get_default_json(self) ->"Boolean":
        return Boolean()

    def parse_json(self, json: bool):
        if not isinstance(json, bool):
            raise TypeError()
        return Boolean(json)

    def __bool__(self) -> bool:
        return self.value

    def __eq__(self, flag: Union["Boolean", bool]) -> bool:
        if isinstance(flag, Boolean):
            return self.value == flag.value
        elif isinstance(flag, bool):
            return self.value == flag
        else:
            raise TypeError()

    def __lt__(self, flag: Union["Boolean", bool]) -> bool:
        if isinstance(flag, Boolean):
            return self.value < flag.value
        elif isinstance(flag, bool):
            return self.value < flag

    def __le__(self, flag: Union["Boolean", bool]) -> bool:
        if isinstance(flag, Boolean):
            return self.value <= flag.value
        elif isinstance(flag, bool):
            return self.value <= flag

    def __gt__(self, flag: Union["Boolean", bool]) -> bool:
        if isinstance(flag, Boolean):
            return self.value > flag.value
        elif isinstance(flag, bool):
            return self.value > flag

    def __ge__(self, flag: Union["Boolean", bool]) -> bool:
        if isinstance(flag, Boolean):
            return self.value >= flag.value
        elif isinstance(flag, bool):
            return self.value >= flag

    def __str__(self) -> str:
        return "True" if self.value else "False"

    def __repr__(self) -> str:
        return "True" if self.value else "False"

    def __int__(self) -> int:
        return 1 if self.value else 0

    def __float__(self) -> float:
        return 1.0 if self.value else 0.0

    def __bytes__(self) -> bytes:
        return b"\x00" if self.value else b""


class String(str, AutoJson):
    def get_default_json(self) -> "String":
        return String()

    def parse_json(self, json: str):
        if not isinstance(json, str):
            raise TypeError()
        return String(json)


T = TypeVar("T", bound=AutoJson)

class Array(list, AutoJson, Generic[T]):
    def __init__(self, indicator: T, size: int = -1):
        if not isinstance(indicator, AutoJson):
            raise TypeError()
        self.indicator = indicator
        self.size = size
        list.__init__(self)

    @overload
    def __getitem__(self, item: int) -> T:
        ...

    @overload
    def __getitem__(self, item: slice) -> "Array[T]":
        ...

    def __getitem__(self, item):
        obj = list.__getitem__(self, item)
        if isinstance(item, int):
            return obj
        else:
            obj_ret = Array(self.indicator, self.size)
            list.__init__(obj_ret, obj)
            return obj_ret

    def get_default_json(self) -> "Array[T]":
        length = self.size if self.size >= 0 else 1
        obj = Array(self.indicator, self.size)
        for _ in range(length):
            obj.append(self.indicator.get_default_json())
        return obj

    def parse_json(self, json: list) -> "Array[T]":
        if not isinstance(json, list):
            raise TypeError()
        if self.size >= 0 and len(json) != self.size:
            raise IndexError()

        obj = Array(self.indicator, self.size)
        for elem in json:
            obj.append(self.indicator.parse_json(elem))
        return obj

    def __iter__(self) -> Iterator[T]:
        return list.__iter__(self)

class Object(dict, AutoJson):
    def get_default_json(self):
        obj = self.__class__()
        for field, indicator in vars(self.__class__).items():
            if not isinstance(indicator, AutoJson):
                continue
            obj[field] = indicator.get_default_json()
            setattr(obj, field, obj[field])
        return obj

    def parse_json(self, json: dict):
        if not isinstance(json, dict):
            raise TypeError()
        obj = self.__class__()
        for field, indicator in vars(obj.__class__).items():
            if not isinstance(indicator, AutoJson):
                continue

            obj[field] = indicator.parse_json(json[field])

        obj.__autojson_init__()

        return obj

    def __autojson_init__(self):
        pass

    def __setitem__(self, key, value):
        AutoJson.__setattr__(self, key, value)
        dict.__setitem__(self, key, value)

    def __setattr__(self, name: str, value: Any):
        AutoJson.__setattr__(self, name, value)
        dict.__setitem__(self, name, value)
