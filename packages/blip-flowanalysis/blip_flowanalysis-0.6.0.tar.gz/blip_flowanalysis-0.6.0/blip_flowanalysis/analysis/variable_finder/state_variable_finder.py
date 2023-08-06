__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp

from .interface_variable_finder import (
    IVariableFinder,
    IPositionalVariableFinder,
)

State = tp.Dict[str, tp.Any]
Location = tp.Tuple[int, int, int, int]
LocationOrNone = tp.Union[Location, None]


class StateVariableFinder(IPositionalVariableFinder):
    """Variable finder on a state.
    
    Find a given variable on a state.
    Variable can be found on inputActions, outputs or outputActions.
    """
    
    def __init__(
            self,
            action_variable_finder: IVariableFinder,
            output_variable_finder: IVariableFinder,
            stages: tp.Tuple[str, ...]) -> None:
        super().__init__()
        self.action_variable_finder = action_variable_finder
        self.output_variable_finder = output_variable_finder
        self.stages = stages
    
    def find_after(
            self,
            data: State,
            variable: str,
            start: LocationOrNone) -> LocationOrNone:
        """Find where is variable on a state after given start place.
        
        Location is represented as a 4 values tuple with:
        * First number: 0 represents inputActions, 1 represents outputs and 2
          represents outputActions.
        * Second number: Position on represented list by first number.
        * Third number: 0 represents action or output conditions and 1
          represents action settings.
        * Fourth number: Position on conditions list of action or output or 0
          if third number is 1.
        Then each place is comparable by other place to check which is early.
        
        Using start as `None` is same as use `find` and search variable
        occurrence on entire state instead only after a given start.
        
        :param data: State data.
        :type data: `dict`
        :param variable: Variable to find.
        :type variable: `str`
        :param start: Start place to search variable use.
        :type start: `tuple`
        :return: Location where is variable used in data or None if not found.
        :rtype: `tuple` or `None`
        """
        if start is None:
            start_stage = 0
            start_index = 0
        else:
            start_stage, start_index, *_ = start
            start_index += 1
        
        while start_stage < len(self.stages):
            items = data[self.stages[start_stage]]
            if start_index < len(items):
                break
            start_stage += 1
            start_index -= len(items)
        
        for stage in range(start_stage, len(self.stages)):
            variable_finder = (
                self.action_variable_finder if stage == 0
                else self.output_variable_finder if stage == 1
                else self.action_variable_finder
            )
            items = data[self.stages[stage]]
            for index, item in enumerate(items[start_index:], start_index):
                place = variable_finder.find(item, variable)
                if place is not None:
                    internal_stage, internal_index = place
                    return stage, index, internal_stage, internal_index
            start_index = 0
        
        return None
