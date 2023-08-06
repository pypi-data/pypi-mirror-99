from typing import Union, List, Optional, Set, Tuple
from pydantic import BaseModel, parse_obj_as

from pynemo.core.base.abstract.expression import Expression
from pynemo.core.base.property import python_type_mapper
from pynemo.core.util import Enum


class LabelExtensionConfig(metaclass=Enum):
    CLASS_NAME_ONLY: int = 1
    INHERIT_ONLY: int = 2


labels_ext_type = Optional[Union[int, str]]
labels_type = Optional[Union[str, List[str], Set[str], Tuple[str]]]


class NodeModelBase(BaseModel, Expression):
    _labels_ext: labels_ext_type = LabelExtensionConfig.CLASS_NAME_ONLY | LabelExtensionConfig.INHERIT_ONLY
    _labels: labels_type = None

    _symbol: str = ''
    _excluded_fields = {'_symbol'}

    def __init__(self, *args, _symbol: str = '', **kwargs):
        super().__init__(*args, **kwargs)
        object.__setattr__(self, '_symbol', _symbol)

    @classmethod
    def get_labels(cls):
        _labels = parse_obj_as(labels_type, cls._labels) or 0
        _labels_ext = parse_obj_as(labels_ext_type, cls._labels_ext)

        labels = set()

        if isinstance(_labels, str):
            _labels = [_labels]
        if _labels:
            labels.update(_labels)

        if isinstance(_labels_ext, str):
            _labels_ext = LabelExtensionConfig[_labels_ext.upper()]
        if isinstance(_labels_ext, int):
            if _labels_ext & LabelExtensionConfig.CLASS_NAME_ONLY:
                labels.add(cls.__name__)
            if _labels_ext & LabelExtensionConfig.INHERIT_ONLY:
                for base in cls.__bases__:
                    if issubclass(base, NodeModelBase) and base is not NodeModelBase:
                        labels.update(base.get_labels())
        return labels

    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        exclude = (exclude or set()) | self._excluded_fields
        return BaseModel.dict(self, include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults,
                              exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)

    def to_cypher(self, symbol: Optional[str] = None):
        symbol = symbol or self._symbol
        labels = ':'.join(self.get_labels())
        if labels:
            labels = ':' + labels

        validators = {k: python_type_mapper.get(v.type_, v.type_).to_cypher for k, v in self.__fields__.items()}
        props = ', '.join([f'{k}: {validators[k](v)}' for k, v in self.dict().items()])

        return f'({symbol}{labels} {{{props}}})'

    def __matmul__(self, other: str):
        n = self.__class__(**self.dict(), _symbol=other)
        return n

    def get_instances(self):
        assert self._symbol
        return [NodeSymbol(self._symbol)]


class NodeSymbol(Expression):
    def __init__(self, symbol):
        self.symbol = symbol

    def to_cypher(self):
        return f'({self.symbol})'
