import collections
import datetime
from abc import abstractmethod
from dataclasses import MISSING, is_dataclass
from decimal import Decimal
from enum import Enum
from functools import partial
from inspect import isclass
from typing import (
    Any,
    AnyStr,
    Callable,
    Deque,
    Dict,
    FrozenSet,
    Generic,
    List,
    NamedTuple,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import Protocol, TypedDict

from chocs.json_schema.iso_datetime import (
    parse_iso_date_string,
    parse_iso_datetime_string,
    parse_iso_duration_string,
    parse_iso_time_string,
    timedelta_to_iso_string,
)
from .typing import (
    get_dataclass_fields,
    get_origin_type,
    get_parameters_map,
    get_type_args,
    is_enum_type,
    is_named_tuple,
    is_optional,
    is_typed_dict,
    map_generic_type,
    unpack_optional,
)

T = TypeVar("T")


class HydrationStrategy(Protocol):
    @abstractmethod
    def hydrate(self, value: Any) -> Any:
        ...

    @abstractmethod
    def extract(self, value: Any) -> Any:
        ...


class DataclassStrategy(HydrationStrategy):
    def __init__(self, dataclass_name: Type):
        self._getters: Dict[str, Callable] = {}
        self._setters: Dict[str, Callable] = {}
        self._dataclass_name = dataclass_name
        self._set_strategies()

    def hydrate(self, value: Any) -> Any:
        instance = self._dataclass_name.__new__(self._dataclass_name)  # type: ignore

        for setter in self._setters.values():
            setter(instance, value)

        if hasattr(instance, "__post_init__"):
            instance.__post_init__()

        return instance

    def extract(self, value: Any) -> Any:
        if not isinstance(value, self._dataclass_name):
            raise ValueError(f"Passed value must be type of {self._dataclass_name}.")

        result = {}
        for name, get in self._getters.items():
            result[name] = get(getattr(value, name, None))

        return result

    def _get_strategy(self, field_type: Type) -> HydrationStrategy:
        return get_strategy_for(field_type)

    def _set_strategies(self) -> None:
        fields = get_dataclass_fields(self._dataclass_name)
        for field_name, field_descriptor in fields.items():
            if not field_descriptor.init and not field_descriptor.repr:
                continue

            strategy = self._get_strategy(field_descriptor.type)
            if field_descriptor.init:
                self._setters[field_name] = partial(
                    set_dataclass_property,
                    setter=strategy.hydrate,
                    property_name=field_name,
                    default_factory=field_descriptor.default_factory,  # type: ignore
                    default_value=field_descriptor.default,
                    optional=is_optional(field_descriptor.type),
                )

            if field_descriptor.repr:
                self._getters[field_name] = strategy.extract


class GenericDataclassStrategy(DataclassStrategy):
    def __init__(self, dataclass_name: Type):
        self._generic_type = dataclass_name
        self._generic_parameters = get_parameters_map(dataclass_name)
        type_: Type = get_origin_type(dataclass_name)  # type: ignore
        super().__init__(type_)

    def _get_strategy(self, field_type: Type) -> HydrationStrategy:
        return get_strategy_for(map_generic_type(field_type, self._generic_parameters))


class DummyStrategy(HydrationStrategy):
    def hydrate(self, value: Any, *args) -> Any:
        return value

    def extract(self, value: Any, *args) -> Any:
        return value


class SimpleStrategy(HydrationStrategy):
    def __init__(self, hydrate_type: Type, extract_type: Type):
        self._hydrate_type = hydrate_type
        self._extract_type = extract_type

    def hydrate(self, value: Any) -> Any:
        return self._hydrate_type(value)

    def extract(self, value: Any) -> Any:
        return self._extract_type(value)


class ListStrategy(HydrationStrategy):
    def __init__(self, subtype: HydrationStrategy):
        self._subtype = subtype

    def hydrate(self, value: Any) -> Any:
        return [self._subtype.hydrate(item) for item in value]

    def extract(self, value: Any) -> Any:
        return [self._subtype.extract(item) for item in value]


class SetStrategy(ListStrategy):
    def hydrate(self, value: Any) -> Any:
        return set(super().hydrate(value))


class FrozenSetStrategy(ListStrategy):
    def hydrate(self, value: Any) -> Any:
        return frozenset(super().hydrate(value))


class DequeStrategy(ListStrategy):
    def hydrate(self, value: Any) -> Any:
        return collections.deque(super().hydrate(value))


class TupleStrategy(HydrationStrategy):
    def __init__(self, subtypes: List[HydrationStrategy]):
        self._subtypes = subtypes
        self._subtypes_length = len(subtypes)
        self._is_ellipsis_present = self._subtypes[-1] is ...

    def hydrate(self, value: Any) -> Any:
        if self._is_ellipsis_present:
            return self._hydrate_ellipsis_tuple(value)

        result = []
        for index, subtype in enumerate(self._subtypes):
            result.append(subtype.hydrate(value[index]))

        return tuple(result)

    def extract(self, value: Any) -> Any:
        if self._is_ellipsis_present:
            return self._extract_ellipsis_tuple(value)

        return [subtype.extract(value[index]) for index, subtype in enumerate(self._subtypes)]

    def _hydrate_ellipsis_tuple(self, value) -> Any:
        last_known_strategy = self._subtypes[0]
        result = []
        for index, item in enumerate(value):
            if index + 1 < self._subtypes_length:
                last_known_strategy = self._subtypes[index]

            result.append(last_known_strategy.hydrate(item))

        return tuple(result)

    def _extract_ellipsis_tuple(self, value) -> Any:
        last_known_strategy = self._subtypes[0]
        result = []
        for index, item in enumerate(value):
            if index + 1 < self._subtypes_length:
                last_known_strategy = self._subtypes[index]

            result.append(last_known_strategy.extract(item))

        return result


class NamedTupleStrategy(HydrationStrategy):
    def __init__(self, class_name: Type[NamedTuple]):
        self._class_name = class_name
        self._is_typed = hasattr(class_name, "__annotations__")
        self._arg_strategies: List[HydrationStrategy] = []
        if self._is_typed:
            self._build_type_mapper(class_name.__annotations__)

    def hydrate(self, value: Any) -> Any:
        if not self._is_typed:
            return self._class_name(*value)

        hydrated_values = []
        for index, item in enumerate(value):
            if index < len(self._arg_strategies):
                hydrated_values.append(self._arg_strategies[index].hydrate(item))
                continue
            hydrated_values.append(item)

        return self._class_name(*hydrated_values)

    def extract(self, value: Any) -> Any:
        result = list(value)
        if not self._is_typed:
            return result
        extracted_values = []
        for index, item in enumerate(result):
            if index < len(self._arg_strategies):
                extracted_values.append(self._arg_strategies[index].extract(item))
                continue
            extracted_values.append(item)

        return extracted_values

    def _build_type_mapper(self, field_types: Dict[str, Type]) -> None:
        for item_type in field_types.values():
            self._arg_strategies.append(get_strategy_for(item_type))


class EnumStrategy(HydrationStrategy):
    def __init__(self, class_name: Type[Enum]):
        self._class_name = class_name

    def hydrate(self, value: Any) -> Any:
        return self._class_name(value)

    def extract(self, value: Any) -> Any:
        return value.value


class DictStrategy(HydrationStrategy):
    def __init__(self, key: HydrationStrategy, value: HydrationStrategy):
        self._key = key
        self._value = value

    def hydrate(self, value: Any) -> Any:
        return {self._key.hydrate(key): self._value.hydrate(item) for key, item in value.items()}

    def extract(self, value: Any) -> Any:
        return {self._key.extract(key): self._value.extract(item) for key, item in value.items()}


class OrderedDictStrategy(DictStrategy):
    def hydrate(self, value: Any) -> Any:
        return collections.OrderedDict(super().hydrate(value))


class TypedDictStrategy(HydrationStrategy):
    def __init__(self, type_name: Type):
        self._strategies: Dict[str, HydrationStrategy] = {}
        for key_name, key_type in type_name.__annotations__.items():
            self._strategies[key_name] = get_strategy_for(key_type)

    def hydrate(self, value: Any) -> Any:
        return {key: self._strategies[key].hydrate(item) for key, item in value.items()}

    def extract(self, value: Any) -> Any:
        return {key: self._strategies[key].extract(item) for key, item in value.items()}


class DateStrategy(HydrationStrategy):
    """
    Conforms ISO 8601 standard https://www.iso.org/iso-8601-date-and-time-format.html
    """

    def hydrate(self, value: Any) -> Any:
        if isinstance(value, datetime.date):
            return value

        return parse_iso_date_string(value)

    def extract(self, value: Any) -> Any:
        return value.isoformat()


class DateTimeStrategy(HydrationStrategy):
    """
    Conforms ISO 8601 standard https://www.iso.org/iso-8601-date-and-time-format.html
    """

    def hydrate(self, value: Any) -> Any:
        if isinstance(value, datetime.datetime):
            return value

        return parse_iso_datetime_string(value)

    def extract(self, value: Any) -> Any:
        return value.isoformat()


class TimeStrategy(HydrationStrategy):
    """
    Conforms ISO 8601 standard https://www.iso.org/iso-8601-date-and-time-format.html
    """

    def hydrate(self, value: Any) -> Any:
        if isinstance(value, datetime.time):
            return value

        return parse_iso_time_string(value)

    def extract(self, value: Any) -> Any:
        return value.isoformat()


class TimeDeltaStrategy(HydrationStrategy):
    """
    Conforms ISO 8601 standard https://www.iso.org/iso-8601-date-and-time-format.html
    """

    def hydrate(self, value: Any) -> Any:
        if isinstance(value, datetime.timedelta):
            return value

        return parse_iso_duration_string(value)

    def extract(self, value: Any) -> Any:
        return timedelta_to_iso_string(value)


class OptionalTypeStrategy(HydrationStrategy):
    def __init__(self, type_strategy: HydrationStrategy):
        self._type_strategy = type_strategy

    def hydrate(self, value: Any, *args) -> Any:
        if value is None:
            return None

        return self._type_strategy.hydrate(value)

    def extract(self, value: Any, *args) -> Any:
        if value is None:
            return None

        return self._type_strategy.extract(value)


def set_dataclass_property(
    obj: object,
    attributes: Dict[str, Any],
    property_name: str,
    setter: Callable,
    default_factory: Union[Callable, Any],
    default_value: Any,
    optional: bool,
) -> None:
    if property_name in attributes:
        setattr(obj, property_name, setter(attributes[property_name]))
        return

    if callable(default_factory):
        setattr(obj, property_name, default_factory())
        return

    if default_value is not MISSING:
        setattr(obj, property_name, default_value)
        return

    attribute_value = attributes.get(property_name, MISSING)

    if attribute_value is MISSING:
        if optional:
            setattr(obj, property_name, None)
            return
        raise AttributeError(f"Property `{property_name}` is required.")

    try:
        setattr(obj, property_name, setter(attribute_value))
    except Exception as error:
        raise AttributeError(f"Could not hydrate `{property_name}` property with `{attribute_value}` value.") from error


BUILT_IN_HYDRATOR_STRATEGY: Dict[Any, HydrationStrategy] = {
    bool: SimpleStrategy(bool, bool),
    collections.OrderedDict: SimpleStrategy(collections.OrderedDict, dict),
    int: SimpleStrategy(int, int),
    float: SimpleStrategy(float, float),
    str: SimpleStrategy(str, str),
    bytes: SimpleStrategy(bytes, bytes),
    list: SimpleStrategy(list, list),
    set: SimpleStrategy(set, list),
    frozenset: SimpleStrategy(frozenset, list),
    tuple: SimpleStrategy(tuple, list),
    dict: SimpleStrategy(dict, dict),
    datetime.time: TimeStrategy(),
    datetime.date: DateStrategy(),
    datetime.datetime: DateTimeStrategy(),
    datetime.timedelta: TimeDeltaStrategy(),
    collections.deque: SimpleStrategy(collections.deque, list),
    TypedDict: SimpleStrategy(dict, dict),  # type: ignore
    Dict: SimpleStrategy(dict, dict),  # type: ignore
    List: SimpleStrategy(list, list),
    Sequence: SimpleStrategy(list, list),
    Tuple: SimpleStrategy(tuple, list),  # type: ignore
    Set: SimpleStrategy(set, list),
    FrozenSet: SimpleStrategy(frozenset, list),
    Deque: SimpleStrategy(collections.deque, list),
    AnyStr: SimpleStrategy(str, str),
    Any: DummyStrategy(),  # type: ignore
    Decimal: SimpleStrategy(Decimal, str),
}

CACHED_HYDRATION_STRATEGIES: Dict[Any, HydrationStrategy] = {}


def get_strategy_for(type_name: Type) -> HydrationStrategy:
    if type_name in BUILT_IN_HYDRATOR_STRATEGY:
        return BUILT_IN_HYDRATOR_STRATEGY[type_name]

    if type_name in CACHED_HYDRATION_STRATEGIES:
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if is_dataclass(type_name):
        if issubclass(type_name, Generic):  # type: ignore
            raise ValueError("Cannot automatically hydrate non-parametrised generic classes.")

        CACHED_HYDRATION_STRATEGIES[type_name] = DataclassStrategy(type_name)
        return CACHED_HYDRATION_STRATEGIES[type_name]

    origin_type = get_origin_type(type_name)

    if origin_type is None:
        if not isclass(type_name):
            return BUILT_IN_HYDRATOR_STRATEGY[Any]  # type: ignore

        if is_enum_type(type_name):
            CACHED_HYDRATION_STRATEGIES[type_name] = EnumStrategy(type_name)
            return CACHED_HYDRATION_STRATEGIES[type_name]

        if is_named_tuple(type_name):
            CACHED_HYDRATION_STRATEGIES[type_name] = NamedTupleStrategy(type_name)
            return CACHED_HYDRATION_STRATEGIES[type_name]

        if is_typed_dict(type_name):
            CACHED_HYDRATION_STRATEGIES[type_name] = TypedDictStrategy(type_name)
            return CACHED_HYDRATION_STRATEGIES[type_name]

        return BUILT_IN_HYDRATOR_STRATEGY[Any]  # type: ignore

    if is_dataclass(origin_type):
        CACHED_HYDRATION_STRATEGIES[type_name] = GenericDataclassStrategy(type_name)
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if origin_type not in BUILT_IN_HYDRATOR_STRATEGY:
        if not is_optional(type_name):
            return BUILT_IN_HYDRATOR_STRATEGY[Any]  # type: ignore

        CACHED_HYDRATION_STRATEGIES[type_name] = OptionalTypeStrategy(get_strategy_for(unpack_optional(type_name)))
        return CACHED_HYDRATION_STRATEGIES[type_name]

    subtypes: List[Union[HydrationStrategy, Any]] = []
    for subtype in get_type_args(type_name):
        if subtype is ...:
            subtypes.append(...)
            continue
        subtypes.append(get_strategy_for(subtype))

    if origin_type is list:
        CACHED_HYDRATION_STRATEGIES[type_name] = ListStrategy(subtypes[0])
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if origin_type is tuple:
        CACHED_HYDRATION_STRATEGIES[type_name] = TupleStrategy(subtypes)
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if origin_type is dict:
        CACHED_HYDRATION_STRATEGIES[type_name] = DictStrategy(subtypes[0], subtypes[1])
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if origin_type is collections.OrderedDict:
        CACHED_HYDRATION_STRATEGIES[type_name] = OrderedDictStrategy(subtypes[0], subtypes[1])
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if origin_type is set:
        CACHED_HYDRATION_STRATEGIES[type_name] = SetStrategy(subtypes[0])
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if origin_type is frozenset:
        CACHED_HYDRATION_STRATEGIES[type_name] = FrozenSetStrategy(subtypes[0])
        return CACHED_HYDRATION_STRATEGIES[type_name]

    if origin_type is collections.deque:
        CACHED_HYDRATION_STRATEGIES[type_name] = DequeStrategy(subtypes[0])
        return CACHED_HYDRATION_STRATEGIES[type_name]

    return BUILT_IN_HYDRATOR_STRATEGY[Any]  # type: ignore
