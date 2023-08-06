__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp

from ._specific_variable_finders import _ConditionVariableFinder

Action = tp.Dict[str, tp.Any]
Location = tp.Tuple[int, int]
LocationOrNone = tp.Union[Location, None]


class ActionVariableFinder(_ConditionVariableFinder):
    """Variable finder on an action.
    
    Find a given variable on an action.
    Variable can be found on conditions or on settings.
    """
    
    def __init__(self) -> None:
        super().__init__()
    
    def find(self, data: Action, variable: str) -> LocationOrNone:
        """Find where is variable on an action.
        
        Location is represented as a 2 values tuple with:
        * First number: 0 represents conditions and 1 represents settings.
        * Second number: Condition position if first is 0 otherwise 0.
        Then each place is comparable by other place to check which is early.
        
        :param data: Action data.
        :type data: `dict`
        :param variable: Variable to find.
        :type variable: `str`
        :return: Location where is variable used in data or None if not found.
        :rtype: `tuple` or `None`
        """
        if 'conditions' in data:
            position = self._find_on_conditions(data['conditions'], variable)
            if position is not None:
                return 0, position
        
        if self._is_on_data(data['settings'], variable):
            return 1, 0
        
        return None
