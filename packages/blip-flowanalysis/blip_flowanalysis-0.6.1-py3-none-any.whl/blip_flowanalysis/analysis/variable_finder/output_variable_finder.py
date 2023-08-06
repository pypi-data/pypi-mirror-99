__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp

from ._specific_variable_finders import _ConditionVariableFinder

Output = tp.Dict[str, tp.Any]
Location = tp.Tuple[int, int]
LocationOrNone = tp.Union[Location, None]


class OutputVariableFinder(_ConditionVariableFinder):
    """Variable finder on an output.
    
    Find a given variable on an output.
    Variable can be found on conditions.
    """
    
    def __init__(self) -> None:
        super().__init__()
    
    def find(self, data: Output, variable: str) -> LocationOrNone:
        """Find where is variable on an output.
        
        Location is represented as a 2 values tuple with:
        * First number: 0.
        * Second number: Condition position.
        Then each place is comparable by other place to check which is early.
        
        :param data: Output data.
        :type data: `dict`
        :param variable: Variable to find.
        :type variable: `str`
        :return: Location where is variable used in data or None if not found.
        :rtype: `tuple` or `None`
        """
        if 'conditions' not in data:
            return None
        
        position = self._find_on_conditions(data['conditions'], variable)
        
        if position is not None:
            return 0, position
        
        return None
