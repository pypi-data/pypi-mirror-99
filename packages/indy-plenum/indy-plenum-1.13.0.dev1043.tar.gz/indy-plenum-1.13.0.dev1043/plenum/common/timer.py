from abc import ABC, abstractmethod
from functools import wraps
from logging import getLogger
from typing import Callable, NamedTuple

import time

from sortedcontainers import SortedListWithKey

logger = getLogger()


class TimerService(ABC):
    @abstractmethod
    def get_current_time(self) -> float:
        pass

    @abstractmethod
    def schedule(self, delay: float, callback: Callable):
        pass

    @abstractmethod
    def cancel(self, callback: Callable):
        pass


class QueueTimer(TimerService):
    TimerEvent = NamedTuple('TimerEvent', [('timestamp', float), ('callback', Callable)])

    def __init__(self, get_current_time=time.perf_counter):
        self._get_current_time = get_current_time
        self._events = SortedListWithKey(key=lambda v: v.timestamp)

    def queue_size(self):
        return len(self._events)

    def service(self):
        while len(self._events) and self._next_timestamp() <= self._get_current_time():
            self._pop_event().callback()

    def get_current_time(self) -> float:
        return self._get_current_time()

    def schedule(self, delay: float, callback: Callable):
        timestamp = self._get_current_time() + delay
        self._events.add(self.TimerEvent(timestamp=timestamp, callback=callback))

    def cancel(self, callback: Callable):
        indexes = [i for i, ev in enumerate(self._events) if ev.callback == callback]
        for i in reversed(indexes):
            del self._events[i]

    def _next_timestamp(self):
        return self._events[0].timestamp

    def _pop_event(self) -> TimerEvent:
        return self._events.pop(0)


class RepeatingTimer:
    def __init__(self, timer: TimerService, interval: float, callback: Callable, active: bool = True):
        @wraps(callback)
        def wrapped_callback():
            if not self._active:
                return
            callback()
            self._timer.schedule(self._interval, self._callback)

        self._timer = timer
        self._interval = None
        self.update_interval(interval)
        self._callback = wrapped_callback
        self._active = False
        # TODO: Make timer always inactive and require calling start to activate
        if active:
            self.start()

    def start(self):
        if self._active or not self._interval:
            return
        self._active = True
        self._timer.schedule(self._interval, self._callback)

    def stop(self):
        if not self._active:
            return
        self._active = False
        self._timer.cancel(self._callback)

    def update_interval(self, interval: float):
        if interval <= 0:
            logger.debug("RepeatingTimer - incorrect interval {}".format(interval))
            return
        self._interval = interval
