from attrs import define, field
from sqlalchemy import ColumnElement

from . import MessagesList


__all__ = ["Step", "StepsGroup"]


@define(kw_only=True)
class Step:
    uid: str = field(init=True)
    messages: MessagesList = field(init=True)

    name = field(init=False, default=None)
    _group = field(init=False, default=None)

    def _set_parent(self, owner):
        if not issubclass(owner, StepsGroup):
            raise TypeError('Group must be subclass of StatesGroup')
        self._group = owner

    def __set_name__(self, owner: "StepsGroup", name):
        self.name = name
        self._set_parent(owner)

    async def sql_requirements(self) -> tuple[ColumnElement]:
        """SQLAlchemy requirements to get users for sending messages"""
        raise NotImplementedError

    async def is_finished(self) -> None:
        """Going to the next step then"""
        raise NotImplementedError

    async def on_finish(self) -> None:
        """It's being called when step is finished and can turn on next"""
        raise NotImplementedError
    
    def next_step(self) -> "Step":
        current_step_index = self._group.steps.index(self)
        try:
            return self._group.steps[current_step_index + 1]
        
        except:
            return None



class StepsGroupMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super(StepsGroupMeta, mcs).__new__(mcs, name, bases, namespace)

        steps = []

        cls._group_name = name

        for name, prop in namespace.items():
            if isinstance(prop, Step):
                steps.append(prop)

        cls._parent = None
        cls._steps = tuple(steps)
        cls._steps_uid = tuple(step.uid for step in steps)

        return cls

    @property
    def __group_name__(cls) -> str:
        return cls._group_name

    @property
    def steps(cls) -> tuple:
        return cls._steps

    @property
    def steps_uid(cls) -> tuple:
        return cls._steps_uid

    def __contains__(cls, item):
        if isinstance(item, Step):
            return item.uid in cls._steps_uid
        elif isinstance(item, str):
            return item in cls._steps_uid
        return False

    def __str__(self):
        return f"<StepsGroup '{self.__group_name__}'>"


class StepsGroup(metaclass=StepsGroupMeta):
    ...
