# -*- coding: utf-8 -*-
"""
    pip_services3_commons.run.FixedRateTimer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Fixed rate timer implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import inspect
import time
from threading import Thread, Event, Lock

from pip_services3_commons.run import Parameters
from .IClosable import IClosable


class Timer(Thread):
    def __init__(self, interval, delay, callback):
        Thread.__init__(self)
        self._interval = interval
        self._callback = callback
        self._event = Event()
        self._delay = delay

    def run(self):
        time.sleep(self._delay)
        while not self._event.is_set():
            self._callback()
            time.sleep(self._interval)

    def stop(self):
        if self.is_alive():
            # set event to signal thread to terminate
            self._event.set()
            # block calling thread until thread really has terminated
            self.join()


class FixedRateTimer(IClosable):
    """
    Timer that is triggered in equal time intervals.

    It has summetric cross-language implementation
    and is often used by Pip.Services toolkit to perform periodic processing and cleanup in microservices.
    """

    _lock = None

    def __init__(self, task_or_object=None, interval=None, delay=None):
        """
        Creates new instance of the timer and sets its values.

        :param task: (optional) a Notifiable object or callback function to call when timer is triggered.

        :param interval: (optional) an _interval to trigger timer in milliseconds.

        :param delay: (optional) a _delay before the first triggering in milliseconds.
        """
        self._lock = Lock()
        self._started = False
        self._task = None
        self._callback = None
        self._timer = None
        self._interval = None
        self._delay = None

        if inspect.isclass(task_or_object) and hasattr(task_or_object, 'notify') and inspect.isfunction(
                task_or_object.notify):
            self.set_task(task_or_object)
        else:
            self.set_callback(task_or_object)

        self.set_interval(interval)
        self.set_delay(delay)

    def get_task(self):
        """
        Gets the INotifiable object that receives notifications from this timer.

        :return: the INotifiable object or null if it is not set.
        """
        return self._task

    def set_task(self, value):
        self._task = value
        self._callback = self._timer_callback

    def get_callback(self):
        """
        Gets the callback function that is called when this timer is triggered.

        :return: the callback function or null if it is not set.
        """
        return self._callback

    def set_callback(self, value):
        """
        Sets the callback function that is called when this timer is triggered.

        :param value: the callback function to be called.
        """
        self._callback = value
        self._task = None

    def get_delay(self):
        """
        Gets initial delay before the timer is triggered for the first time.

        :return: the delay in milliseconds.
        """
        return self._delay

    def set_delay(self, value):
        """
        Sets initial delay before the timer is triggered for the first time.
        :param value: a delay in milliseconds.
        """
        self._delay = value

    def get_interval(self):
        """
        Gets periodic timer triggering interval.

        :return: the interval in milliseconds
        """
        return self._interval

    def set_interval(self, value):
        """
        Sets periodic timer triggering interval.

        :param value: an interval in milliseconds.
        """
        self._interval = value

    def is_started(self):
        """
        Checks if the timer is started.

        :return: true if the timer is started and false if it is stopped.
        """
        return self._timer is not None

    def start(self):
        """
        Starts the timer.
        Initially the timer is triggered after _delay.
        After that it is triggered after _interval until it is stopped.
        """
        self._lock.acquire()
        try:
            # Stop previously set timer
            if not (self._timer is None):
                self._timer.stop()
                self._timer = None

            if self._interval is None or self._interval <= 0:
                return

            delay = max(0, self._delay - self._interval)

            # Set a new timer
            self._timer = Timer(self._interval / 1000, delay / 1000, self._callback)
            self._timer.start()

            # Set _started flag
            self._started = True
        finally:
            self._lock.release()

    def _timer_callback(self):
        try:
            self._task.notify("pip-commons-timer", Parameters())
        except:
            # Ignore or better log
            pass

    def stop(self):
        """
        Stops the timer.
        """
        self._lock.acquire()
        try:
            # Stop the timer
            if not (self._timer is None):
                self._timer.stop()
                self._timer = None

            # Unset _started flag
            self._started = False
        finally:
            self._lock.release()

    def close(self, correlation_id):
        """
        Closes the timer.
        This is required by :class:`IClosable <pip_services3_commons.run.IClosable.IClosable>` interface,
        but besides that it is identical to stop().

        :param correlation_id: (optional) transaction id to trace execution through call chain.
        """
        self.stop()
