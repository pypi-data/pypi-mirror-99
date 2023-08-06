import uvicore
from uvicore.support.dumper import dump, dd
from dataclasses import dataclass
from uvicore.typing import Dict, Optional, Union, Callable


@uvicore.service()
class Event:

    # Defaults
    is_async: bool = False

    @classmethod
    @property
    def name(cls):
        name = str(cls).split("'")[1]
        # print(name, 'aaa')
        # if name == 'uvicore.events.event.Event':
        #     name = cls.__module__ + '.' + cls.__name__
        #print(name, 'xxx')
        return name

    @classmethod
    @property
    def description(cls):
        return cls.__doc__

    @classmethod
    def listen(cls, handler: Union[str, Callable]):
        """Listen to to this event using this handler"""
        uvicore.events.listen(cls, handler)

    @classmethod
    def listener(cls, handler: Union[str, Callable]):
        """Alias to Listen"""
        uvicore.events.listen(cls, handler)

    @classmethod
    def handle(cls, handler: Union[str, Callable]):
        """Alias to Listen"""
        uvicore.events.listen(cls, handler)

    @classmethod
    def handler(cls, handler: Union[str, Callable]):
        """Alias to Listen"""
        uvicore.events.listen(cls, handler)

    @classmethod
    def call(cls, handler: Union[str, Callable]):
        """Alias to Listen"""
        uvicore.events.listen(cls, handler)

    def dispatch(self):
        """Dispatch this event which will call all listeners handlers"""
        uvicore.events._dispatch(self)

    async def dispatch_async(self):
        await uvicore.events._dispatch_async(self)


    # No, logging should be a listener
    # def log(self, cls):
    #     uvicore.log.debug("Event " + str(cls.__class__.__module__) + " Dispatched")

