__author__ = 'Gabriel Salgado'
__version__ = '0.1.0'

import abc
import typing as tp
import dataclasses as dc

Data = tp.Dict[str, tp.Any]
Location = tp.Tuple[int, ...]
LocationOrNone = tp.Union[Location, None]


class IVariableFinder(abc.ABC):
    """Interface for variable finders."""
    
    def __init__(self) -> None:
        super().__init__()
    
    @abc.abstractmethod
    def find(self, data: Data, variable: str) -> LocationOrNone:
        """Find where is variable in data.
        
        Location is represented as `tuple` of `int`.
        Each `int` is position or part.
        Then each place is comparable by other place to check which is early.
        
        :param data: Data.
        :type data: `dict`
        :param variable: Variable to find.
        :type variable: `str`
        :return: Location where is variable used in data or None if not found.
        :rtype: `tuple` or `None`
        """
        raise NotImplementedError()


class IPositionalVariableFinder(IVariableFinder, abc.ABC):
    
    _INITIAL = None
    
    def __init__(self) -> None:
        super().__init__()
    
    def find(self, data: Data, variable: str) -> LocationOrNone:
        """Find where is variable in data.
        
        Location is represented as `tuple` of `int`.
        Each `int` is position or part.
        Then each place is comparable by other place to check which is early.
        
        :param data: Data.
        :type data: `dict`
        :param variable: Variable to find.
        :type variable: `str`
        :return: Location where is variable used in data or None if not found.
        :rtype: `tuple` or `None`
        """
        return self.find_after(data, variable, self._INITIAL)
    
    @abc.abstractmethod
    def find_after(
            self,
            data: Data,
            variable: str,
            start: LocationOrNone) -> LocationOrNone:
        """Find where is variable in data after given start place.
        
        Location is represented as `tuple` of `int`.
        Each `int` is position or part.
        Then each place is comparable by other place to check which is early.
        
        :param data: Data.
        :type data: `dict`
        :param variable: Variable to find.
        :type variable: `str`
        :param start: Start place to search variable use.
        :type start: `tuple`
        :return: Location where is variable used in data or None if not found.
        :rtype: `tuple` or `None`
        """
        raise NotImplementedError()
