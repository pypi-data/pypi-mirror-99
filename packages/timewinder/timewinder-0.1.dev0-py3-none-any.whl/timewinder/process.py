from abc import ABC
from abc import abstractmethod

from .model import Model
from .closure import Closure

from inspect import isfunction

from typing import List

from timewinder.statetree import TreeType


def step(function):
    """Decorator representing an atomic operation between states."""
    if not isfunction(function):
        raise TypeError("Single threads can only be created by decorators on fuctions")

    return Closure(function, Step)


class StopProcess(BaseException):
    pass


class Process(Model, ABC):
    @abstractmethod
    def execute(self, state_controller):
        pass

    @abstractmethod
    def can_execute(self) -> bool:
        pass


class Step:
    def __init__(self, func, args, kwargs):
        self.args = args
        self.kwargs = kwargs
        self.func = func

    def _eval(self, thread_state):
        return self.func(thread_state, *self.args, **self.kwargs)


class FuncProcess(Process):
    def __init__(self, *args, state=None):
        self.steps: List[Step] = args
        self.pc = 0
        self.state = state

    @property
    def name(self):
        return self.__repr__()

    def get_state(self) -> TreeType:
        return {
            "pc": self.pc,
            "state": self.state,
        }

    def set_state(self, state: TreeType) -> None:
        assert isinstance(state, dict)
        self.pc = state["pc"]
        self.state = state["state"]

    def can_execute(self) -> bool:
        if self.pc < 0:
            return False
        return self.pc < len(self.steps)

    def execute(self, state_controller):
        assert self.can_execute()
        try:
            self.steps[self.pc]._eval(self.state)
            self.pc += 1
        except StopProcess:
            self.pc = -1

    def __repr__(self) -> str:
        funcs = ",".join([s.func.__name__ for s in self.steps])
        return f"FuncProcess([{funcs}])@{self.pc}:{self.state}"


class ProcessException(BaseException):
    def __init__(self, info, wrapped):
        self.info = info
        self.wrapped = wrapped

    def __repr__(self):
        return f"{self.info} caught an exception: {self.wrapped}"
