"""Check if HTTP requests on bot are validated on bot flow.

This is done by class `ProcessHTTPReturnValidation`.
Class `Sample` make this analysis on a specific Process HTTP action.

Bot flow can contain points where HTTP requests are done.
It is desirable that these requests are validated by status.
Sometimes returned content must be also used after HTTP request.
This analyser intend to ensure that each HTTP return is suitably used.

To ensure suitability, HTTP return must be used based on rules.
Status must be always used to validate HTTP return.
Body must be used to agree with intend if HTTP request is GET method.
Body must not be used neither declared on HTTP request using PUT method.
"""
__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.1.0'

import typing as tp
import itertools as it
import dataclasses as dc

from blip_flowanalysis.abstract import Analyser
from blip_flowanalysis.core import Flow
from .variable_finder.interface_variable_finder import (
    IPositionalVariableFinder,
)
from .variable_finder.action_variable_finder import ActionVariableFinder
from .variable_finder.output_variable_finder import OutputVariableFinder
from .variable_finder.state_variable_finder import StateVariableFinder


class Default(object):
    must_use_body_methods: tp.Tuple[str, ...] = ('GET',)
    must_not_declare_body_methods: tp.Tuple[str, ...] = ('PUT',)
    stages: tp.Tuple[str, ...] = ('inputActions', 'outputs', 'outputActions')
    io_actions: tp.Tuple[str, str] = ('inputActions', 'outputActions')
    process_http_type: str = 'ProcessHttp'


Output = tp.Dict[str, tp.Any]
Action = tp.Dict[str, tp.Any]
State = tp.Dict[str, tp.Any]
States = tp.List[State]
MapStates = tp.Dict[str, State]


@dc.dataclass
class Context(object):
    state: State
    io_action: str
    n_action: int
    action: Action


Location = tp.Tuple[int, ...]
LocationOrNone = tp.Union[Location, None]
Path = tp.List[str]


@dc.dataclass
class UseRegister(object):
    used: bool = dc.field(init=False)
    state_index: int
    location: LocationOrNone
    
    def __post_init__(self) -> None:
        self.used = self.location is not None


@dc.dataclass
class StackUseRegister(object):
    path: Path
    status: UseRegister
    body: UseRegister


StackUseRegisters = tp.List[StackUseRegister]


class Sample(object):
    """Represents a sample for HTTP process actions.
    
    This is a business layer that contains context information (including
    state, interface and action) and results (HTTP request method, status
    use and body use).
    
    :param variable_finder: Variable finder instance that find variable usage
        on a state.
    :type variable_finder: `blip_flowanalysis.analysis.variable_finder.interface_variable_finder.IPositionalVariableFinder`
    :param context: Context input. Includes state, interface (inputActions,
        outputs or outputActions) and action (number and data).
    :type context: `blip_flowanalysis.analysis.process_http_return_validation.Context`
    :param map_states: Mapping state id to state.
    :type map_states: `dict` from `str` to `dict`
    :param max_levels: Maximum levels distance from state with HTTP request
        to state with HTTP return use.
    :type max_levels: `int`
    :param must_use_body_methods: HTTP methods that requires body use.
    :type must_use_body_methods: `tuple` of `str`
    :param must_not_declare_body_methods: HTTP methods that forbidden body
        declaration.
    :type must_not_declare_body_methods: `tuple` of `str`
    :param stages: Stages on state where can be found status and body use.
    :type stages: `tuple` of `str`
    """
    
    def __init__(
            self,
            variable_finder: IPositionalVariableFinder,
            context: Context,
            map_states: MapStates,
            max_levels: int = 2,
            must_use_body_methods: tp.Tuple[str, ...] =\
                    Default.must_use_body_methods,
            must_not_declare_body_methods: tp.Tuple[str, ...] =\
                    Default.must_not_declare_body_methods,
            stages: tp.Tuple[str, ...] = Default.stages) -> None:
        super().__init__()
        self.variable_finder = variable_finder
        self.context = context
        self.map_states = map_states
        self.max_levels = max_levels
        self.must_use_body_methods = must_use_body_methods
        self.must_not_declare_body_methods = must_not_declare_body_methods
        self.stages = stages
        self.registers = self._build_registers()
        self.regular_registers = self._build_regular_registers()
        self.registers_with_miss_status = self._build_registers_with_miss_status()
        self.registers_with_miss_body = self._build_registers_with_miss_body()
        self.registers_with_body_before_status = self._build_registers_with_body_before_status()
    
    @property
    def state(self) -> State:
        return self.context.state
    
    @property
    def state_id(self) -> str:
        return self.state['id']
    
    @property
    def state_name(self) -> str:
        return self.state['name']
    
    @property
    def io_action(self) -> str:
        return self.context.io_action
    
    @property
    def n_action(self) -> int:
        return self.context.n_action
    
    @property
    def action(self) -> Action:
        return self.context.action
    
    @property
    def status_variable(self) -> tp.Union[str, None]:
        return self.action['settings'].get('responseStatusVariable', None)
    
    @property
    def body_variable(self) -> tp.Union[str, None]:
        return self.action['settings'].get('responseBodyVariable', None)
    
    @property
    def http_method(self) -> str:
        return self.action['settings']['method']
    
    def _build_registers(self) -> StackUseRegisters:
        if not (self.declared_status() or self.declared_body()):
            return list()
        
        state = self.state
        stage = self.stages.index(self.io_action)
        start = stage, self.n_action, 0, 0
        
        pl_status = self._find_in_state(state, self.status_variable, start)
        pl_body = self._find_in_state(state, self.body_variable, start)
        
        register = StackUseRegister(
            path=[state['id']],
            status=UseRegister(state_index=0, location=pl_status),
            body=UseRegister(state_index=0, location=pl_body),
        )
        
        must_check_outputs = (
            self._miss_status(register)
            or self._miss_body(register)
        )
        
        if must_check_outputs:
            states = [
                self.map_states[output['stateId']]
                for output in state['outputs']
                if 'conditions' in output
            ]
            if states:
                return list(it.chain.from_iterable(
                    self._find_on_output(state, register)
                    for state in states
                ))
            return [register]
        return [register]
    
    def _find_in_state(
            self,
            state: State,
            variable: tp.Union[str, None],
            start: tp.Optional[Location] = None) -> LocationOrNone:
        if variable is None:
            return None
        
        if start is None:
            return self.variable_finder.find(state, variable)
        return self.variable_finder.find_after(state, variable, start)
    
    def _miss_status(
            self,
            register: StackUseRegister) -> bool:
        return not register.status.used
    
    def _miss_body(
            self,
            register: StackUseRegister) -> bool:
        return self.must_use_body() and not register.body.used
    
    def _body_before_status(
            self,
            register: StackUseRegister) -> bool:
        return (
            register.status.used
            and register.body.used
            and register.status.state_index >= register.body.state_index
            and (
                register.status.state_index > register.body.state_index
                or register.status.location > register.body.location
            )
        )
    
    def _build_register(
            self,
            state: State,
            last_register: StackUseRegister,
            pl_status: LocationOrNone,
            pl_body: LocationOrNone) -> StackUseRegister:
        n_state = len(last_register.path)
        return StackUseRegister(
            path=last_register.path + [state['id']],
            status=(
                last_register.status if last_register.status.used
                else UseRegister(state_index=n_state, location=pl_status)
            ),
            body=(
                last_register.body if last_register.body.used
                else UseRegister(state_index=n_state, location=pl_body)
            ),
        )
    
    def _find_on_output(
            self,
            state: State,
            register: StackUseRegister) -> StackUseRegisters:
        n_state = len(register.path)
        
        pl_status = self._find_in_state(state, self.status_variable)
        pl_body = self._find_in_state(state, self.body_variable)
        register = self._build_register(state, register, pl_status, pl_body)
        
        must_check_outputs = (
            (
                self._miss_status(register)
                or self._miss_body(register)
            ) and n_state < self.max_levels
        )
        
        if must_check_outputs:
            states = [
                self.map_states[output['stateId']]
                for output in state['outputs']
                if 'conditions' in output
            ]
            if states:
                return list(it.chain.from_iterable(
                    self._find_on_output(state, register)
                    for state in states
                ))
            return [register]
        return [register]
    
    def _build_regular_registers(self) -> StackUseRegisters:
        if self.improper_declared_body():
            return list()
        return [
            register
            for register in self.registers
            if not (
                self._miss_status(register)
                or self._miss_body(register)
                or self._body_before_status(register)
            )
        ]
    
    def _build_registers_with_miss_status(self) -> StackUseRegisters:
        return [
            register
            for register in self.registers
            if self._miss_status(register)
        ]
    
    def _build_registers_with_miss_body(self) -> StackUseRegisters:
        return [
            register
            for register in self.registers
            if self._miss_body(register)
        ]
    
    def _build_registers_with_body_before_status(self) -> StackUseRegisters:
        return [
            register
            for register in self.registers
            if self._body_before_status(register)
        ]
    
    def declared_status(self) -> bool:
        """Check if declared status variable.
        
        :return: True if status variable is declared otherwise False.
        :rtype: `bool`
        """
        return self.status_variable is not None
    
    def declared_body(self) -> bool:
        """Check if declared body variable.
        
        :return: True if body variable is declared otherwise False.
        :rtype: `bool`
        """
        return self.body_variable is not None
    
    def all_used_status(self) -> bool:
        """Check if used status on all paths.
        
        :return: True if used status on all paths otherwise False.
        :rtype: `bool`
        """
        return bool(self.registers) and all(
            register.status.used
            for register in self.registers
        )
    
    def any_used_body(self) -> bool:
        """Check if used body on any path.
        
        :return: True if used body on any path otherwise False.
        :rtype: `bool`
        """
        return bool(self.registers) and any(
            register.body.used
            for register in self.registers
        )
    
    def any_used_body_before_status(self) -> bool:
        """Check if used body before status on any path.
        
        :return: True if used body before status on any path otherwise False.
        :rtype: `bool`
        """
        return bool(self.registers_with_body_before_status)
    
    def must_use_body(self) -> bool:
        """Check if used HTTP method requires body use.
        
        :return: True if HTTP method requires body use otherwise False.
        :rtype: `bool`
        """
        return self.http_method in self.must_use_body_methods
    
    def must_not_declare_body(self) -> bool:
        """Check if used HTTP method requires do not declare body.
        
        :return: True if HTTP method requires do not declare body otherwise False.
        :rtype: `bool`
        """
        return self.http_method in self.must_not_declare_body_methods
    
    def is_regular(self) -> bool:
        """Check if this HTTP return validation is regular.
        
        If not use status, it is not regular.
        If must use body and do not, it is not regular.
        If must not use body and declared body, it is not regular.
        
        :return: True if it is regular HTTP validation otherwise False.
        :rtype: `bool`
        """
        return not (
            self.missing_status()
            or self.missing_body()
            or self.improper_declared_body()
            or self.any_used_body_before_status()
        )
    
    def missing_status(self) -> bool:
        """Check if miss use status in any path.
        
        :return: True if miss use status in any path otherwise False.
        :rtype: `bool`
        """
        return bool(self.registers_with_miss_status)
    
    def missing_body(self) -> bool:
        """Check if miss use body in any path.
        
        :return: True if miss use body in any path otherwise False.
        :rtype: `bool`
        """
        if self.registers:
            return len(self.registers_with_miss_body) == len(self.registers)
        return self.must_use_body()
    
    def improper_declared_body(self) -> bool:
        """Check if must not declare body but declared this variable.
        
        :return: True if must not declare body and declared it otherwise False.
        :rtype: `bool`
        """
        return self.must_not_declare_body() and self.declared_body()
    
    def which_state_id_used_status(
            self,
            register: StackUseRegister) -> str:
        """Get state id for first status use on given register.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: State id for first status use.
        :rtype: `str`
        """
        return register.path[register.status.state_index]
    
    def which_state_id_used_body(
            self,
            register: StackUseRegister) -> str:
        """Get state id for first body use on given register.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: State id for first body use.
        :rtype: `str`
        """
        return register.path[register.body.state_index]
    
    def which_state_used_status(
            self,
            register: StackUseRegister) -> State:
        """Get state object for first status use on given register.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: State for first status use.
        :rtype: `dict`
        """
        state_id = self.which_state_id_used_status(register)
        return self.map_states[state_id]
    
    def which_state_used_body(
            self,
            register: StackUseRegister) -> State:
        """Get state object for first body use on given register.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: State for first body use.
        :rtype: `dict`
        """
        state_id = self.which_state_id_used_body(register)
        return self.map_states[state_id]
    
    def which_state_stage_used_status(
            self,
            register: StackUseRegister) -> str:
        """Get stage on state for first status use on given register.
        
        Stage is name for list of action or output where was found first use.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: State stage for first status use.
        :rtype: `str`
        """
        return self.stages[register.status.location[0]]
    
    def which_state_stage_used_body(
            self,
            register: StackUseRegister) -> str:
        """Get stage on state for first body use on given register.
        
        Stage is name for list of action or output where was found first use.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: State stage for first body use.
        :rtype: `str`
        """
        return self.stages[register.body.location[0]]
    
    def which_stage_position_used_status(
            self,
            register: StackUseRegister) -> int:
        """Get position on stage for first status use on given register.
        
        Stage is name for list of action or output.
        Position to return is position on this list with first use.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: Position on stage for first status use.
        :rtype: `int`
        """
        return register.status.location[1]
    
    def which_stage_position_used_body(
            self,
            register: StackUseRegister) -> int:
        """Get position on stage for first body use on given register.
        
        Stage is name for list of action or output.
        Position to return is position on this list with first use.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: Position on stage for first body use.
        :rtype: `int`
        """
        return register.body.location[1]
    
    def which_stage_object_used_status(
            self,
            register: StackUseRegister) -> tp.Union[Action, Output]:
        """Get object on stage for first status use on given register.
        
        Stage is name for list of action or output.
        Object to return is action or output on this list with first use.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: Object on stage for first status use.
        :rtype: `dict`
        """
        state = self.which_state_used_status(register)
        stage = self.which_state_stage_used_status(register)
        position = self.which_stage_position_used_status(register)
        return state[stage][position]
    
    def which_stage_object_used_body(
            self,
            register: StackUseRegister) -> tp.Union[Action, Output]:
        """Get object on stage for first body use on given register.
        
        Stage is name for list of action or output.
        Object to return is action or output on this list with first use.
        
        :param register: Register object.
        :type register: `blip_flowanalysis.analysis.process_http_return_validation.StackUseRegister`
        :return: Object on stage for first body use.
        :rtype: `dict`
        """
        state = self.which_state_used_body(register)
        stage = self.which_state_stage_used_body(register)
        position = self.which_stage_position_used_body(register)
        return state[stage][position]
    
    def causes(self) -> tp.List[str]:
        """List causes why this sample has irregularity.
        
        :return: Causes for irregularities.
        :rtype: `list` of `str`
        """
        causes = list()
        
        if self.missing_status():
            causes.append('Missed use status in some path.')
        
        if self.missing_body():
            causes.append(
                f'Missed use body in some path and HTTP method '
                f'{self.http_method} requires to use it.')
        
        if self.improper_declared_body():
            causes.append(
                f'Declared body and HTTP method {self.http_method} requires '
                f'to not declare it.')
        
        return causes


Samples = tp.List[Sample]
Results = tp.Tuple[
    States,
    Samples,
]

ReportSummary = tp.Dict[str, tp.Any]
ReportDetails = tp.List[tp.Dict[str, tp.Any]]
ReportRegister = tp.Dict[str, tp.Any]
Report = tp.Dict[str, tp.Any]


class ProcessHTTPReturnValidation(Analyser):
    """Check if HTTP requests on bot are validated on bot flow.
    
    Bot flow can contain points where HTTP requests are done.
    It is desirable that these requests are validated by status.
    Sometimes returned content must be also used after HTTP request.
    This analyser intend to ensure that each HTTP return is suitably used.
    
    To ensure suitability, HTTP return must be used based on rules.
    Status must be always used to validate HTTP return.
    Body must be used to agree with intend if HTTP request is GET method.
    Body must not be used neither declared on HTTP request using PUT method.
    
    :param max_levels: Maximum levels distance from state with HTTP request
        to state with HTTP return use.
    :type max_levels: `int`
    :param must_use_body_methods: HTTP methods that requires body use.
    :type must_use_body_methods: `tuple` of `str`
    :param must_not_declare_body_methods: HTTP methods that forbidden body
        declaration.
    :type must_not_declare_body_methods: `tuple` of `str`
    :param stages: Stages on state where can be found status and body use.
    :type stages: `tuple` of `str`
    :param io_actions: Interfaces on state that contains actions.
    :type io_actions: `tuple` of `str`
    :param process_http_type: Action type that make HTTP request.
    :type process_http_type: `str`
    
    :cvar action_variable_finder: Finder for variable on an action.
    :type action_variable_finder: ``blip_flowanalysis.analysis.variable_finder.action_variable_finder.ActionVariableFinder``
    :cvar output_variable_finder: Finder for variable on an output.
    :type output_variable_finder: ``blip_flowanalysis.analysis.variable_finder.output_variable_finder.OutputVariableFinder``
    :cvar state_variable_finder: Finder for variable on a state.
    :type state_variable_finder: ``blip_flowanalysis.analysis.variable_finder.state_variable_finder.state_variable_finder``
    """
    
    action_variable_finder = ActionVariableFinder()
    output_variable_finder = OutputVariableFinder()
    state_variable_finder = StateVariableFinder(
        action_variable_finder=action_variable_finder,
        output_variable_finder=output_variable_finder,
        stages=Default.stages,
    )
    
    def __init__(
            self,
            max_levels: int = 2,
            must_use_body_methods: tp.Tuple[str, ...] =\
                    Default.must_use_body_methods,
            must_not_declare_body_methods: tp.Tuple[str, ...] =\
                    Default.must_not_declare_body_methods,
            stages: tp.Tuple[str, ...] = Default.stages,
            io_actions: tp.Tuple[str, str] = Default.io_actions,
            process_http_type: str = Default.process_http_type) -> None:
        super().__init__()
        self.max_levels = max_levels
        self.must_use_body_methods = must_use_body_methods
        self.must_not_declare_body_methods = must_not_declare_body_methods
        self.stages = stages
        self.io_actions = io_actions
        self.process_http_type = process_http_type
    
    def _iterate_contexts(
            self,
            states: States) -> tp.Iterator[Context]:
        for state in states:
            for io_action in self.io_actions:
                for n_action, action in enumerate(state[io_action]):
                    yield Context(
                        state=state,
                        io_action=io_action,
                        n_action=n_action,
                        action=action,
                    )
    
    def _is_process_http(self, action: Action) -> bool:
        return action['type'] == self.process_http_type
    
    def _report_register(
            self,
            sample: Sample,
            register: StackUseRegister) -> ReportRegister:
        map_states = sample.map_states
        
        path = list()
        for id_ in register.path:
            state = map_states[id_]
            path.append(self._report_state(state))
        
        status = dict()
        if register.status.used:
            state = sample.which_state_used_status(register)
            stage = sample.which_state_stage_used_status(register)
            index = sample.which_stage_position_used_status(register)
            status['state'] = self._report_state(state)
            status['stage on state'] = stage
            status['index on stage'] = index
        
        body = dict()
        if register.body.used:
            state = sample.which_state_used_body(register)
            stage = sample.which_state_stage_used_body(register)
            index = sample.which_stage_position_used_body(register)
            status['state'] = self._report_state(state)
            status['stage on state'] = stage
            status['index on stage'] = index
        
        return {
            'path': path,
            'status use': status,
            'body use': body,
        }
    
    def _report_state(self, state: State) -> tp.Dict[str, str]:
        return {
            'id': state['id'],
            'name': state['name'],
        }
    
    def _sample(self, context: Context, map_states: MapStates) -> Sample:
        return Sample(
            self.state_variable_finder,
            context,
            map_states,
            self.max_levels,
            self.must_use_body_methods,
            self.must_not_declare_body_methods,
            self.stages,
        )
    
    def _report_summary(self, results: Results) -> ReportSummary:
        states, samples = results
        n_process_http = len(samples)
        n_regular_process_http = sum(s.is_regular() for s in samples)
        n_missing_status = sum(s.missing_status() for s in samples)
        n_missing_body = sum(s.missing_body() for s in samples)
        n_improper_declared_body= sum(s.improper_declared_body() for s in samples)
        n_any_used_body_before_status = sum(
            s.any_used_body_before_status() for s in samples)
        n_states = len(states)
        n_irregular_states = len({
            s.state_id
            for s in samples
            if not s.is_regular()
        })
        return {
            'process HTTP actions': n_process_http,
            'process HTTP actions regular': n_regular_process_http,
            'process HTTP actions missing status': n_missing_status,
            'process HTTP actions missing body': n_missing_body,
            'process HTTP actions improper declared body': n_improper_declared_body,
            'process HTTP actions any used body before status': n_any_used_body_before_status,
            'states count': n_states,
            'states with irregular process HTTP action': n_irregular_states,
        }
    
    def _report_details(self, results: Results) -> ReportDetails:
        _, samples = results
        details = list()
        for sample in samples:
            if not sample.is_regular():
                details.append({
                    'state id': sample.state_id,
                    'state name': sample.state_name,
                    'io action': sample.io_action,
                    'action number': sample.n_action,
                    'http method': sample.http_method,
                    'status variable': sample.status_variable,
                    'body variable': sample.body_variable,
                    'all paths used status': sample.all_used_status(),
                    'any path used body': sample.any_used_body(),
                    'declared status': sample.declared_status(),
                    'declared body': sample.declared_body(),
                    'must use body': sample.must_use_body(),
                    'must not declare body': sample.must_not_declare_body(),
                    'paths with missing status': [
                        self._report_register(sample, register)
                        for register in sample.registers_with_miss_status
                    ],
                    'paths with missing body': [
                        self._report_register(sample, register)
                        for register in sample.registers_with_miss_body
                    ],
                    'paths with body before status': [
                        self._report_register(sample, register)
                        for register in sample.registers_with_body_before_status
                    ],
                    'causes': sample.causes(),
                })
        return details
    
    def _report(self, results: Results) -> Report:
        summary = self._report_summary(results)
        details = self._report_details(results)
        return {
            'summary': summary,
            'details': details
        }
    
    def analyse(self, flow: Flow) -> Report:
        """Detects if each HTTP return are or not validated on bot flow.
        
        Returns a report with summary and details.
        
        Summary includes:
            * Number of process HTTP actions;
            * Number of process HTTP actions with return validated.
            * Number of process HTTP actions with not validated status.
            * Number of process HTTP actions with not used body and must use it.
            * Number of process HTTP actions with used body and must not use it.
            * Number of process HTTP actions with used body before validate status.
            * Number of states;
            * Number of states with any irregularity on any process HTTP action.
        
        For each irregularity on HTTP return validation, details includes:
            * State name and id where is process HTTP action;
            * Action location on state;
            * Used HTTP method on action;
            * Status and body variables;
            * Indications about status and body variables use/declaration;
            * Indication about requiring body use;
            * Indication about forbidding body declaration;
            * Paths with miss status use;
            * Paths with miss body use;
            * Paths with body use before validation with status;
            * Locations of status and body uses for each path where body was
              used before status validation;
            * Summary causes for irregularity on HTTP return validation for
              this action.
        
        :param flow: Bot flow structure.
        :type flow: `blip_flowanalysis.core.Flow`
        :return: Report with analysis of HTTP return validation on bot flow.
        :rtype: `dict` from `str` to `any`
        """
        states = flow.get_states_list()
        samples = self.measure(states)
        
        results = states, samples
        return self._report(results)
    
    def measure(self, states: States) -> Samples:
        """Measure all HTTP return validation on bot flow.
        
        Returns a list of samples.
        Each sample is related to a HTTP process action and gives a result
        including status and body variables uses after HTTP process.
        
        See also: `blip_flowanalysis.analysis.process_http_return_validation.Sample`.
        
        :param states: List of states on bot flow.
        :type states: `list` of `dict`
        :return: Samples for each HTTP process action.
        :rtype: `list` of `blip_flowanalysis.analysis.process_http_return_validation.Sample`
        """
        map_states = {
            state['id']: state
            for state in states
        }
        samples = list()
        
        for context in self._iterate_contexts(states):
            if self._is_process_http(context.action):
                sample = self._sample(context, map_states)
                samples.append(sample)
        
        return samples
