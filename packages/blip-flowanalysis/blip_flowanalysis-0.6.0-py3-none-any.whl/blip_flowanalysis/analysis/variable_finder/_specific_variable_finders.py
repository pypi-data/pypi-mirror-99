__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import abc
import typing as tp

from .interface_variable_finder import IVariableFinder

Condition = tp.Dict[str, tp.Any]
Conditions = tp.List[Condition]


class _DataVariableFinder(IVariableFinder, abc.ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    def _is_on_dict(self, data: tp.Dict[str, tp.Any], variable: str) -> bool:
        return any(self._is_on_data(item, variable) for item in data.values())
    
    def _is_on_list(self, data: tp.List[tp.Any], variable: str) -> bool:
        return any(self._is_on_data(item, variable) for item in data)
    
    def _is_on_string(self, data: str, variable: str) -> bool:
        return (
            data == variable
            or data == f'context.{variable}'
            or f'{{{{{variable}}}}}' in data
            or f'${{{variable}}}' in data
            or f'{{{{context.{variable}}}}}' in data
            or f'${{context.{variable}}}' in data
        )
    
    def _is_on_data(self, data: tp.Any, variable: str) -> bool:
        return (
            self._is_on_dict(data, variable) if isinstance(data, dict)
            else self._is_on_list(data, variable) if isinstance(data, list)
            else self._is_on_string(data, variable) if isinstance(data, str)
            else False
        )


class _ConditionVariableFinder(_DataVariableFinder, abc.ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    def _find_on_conditions(
            self,
            conditions: Conditions,
            variable: str) -> tp.Union[int, None]:
        for k, condition in enumerate(conditions):
            if self._is_on_data(condition, variable):
                return k
        return None
