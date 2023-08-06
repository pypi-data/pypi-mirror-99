import time
import logging
import re
from contextlib import contextmanager
from functools import wraps
from typing import Tuple, Optional

from translucent.base import Status
from translucent.formatters import JSON


def to_kebab_case(s):
    with_underscore = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", with_underscore).lower()


@contextmanager
def extra(**fields):
    root = logging.getLogger()
    restore = {}
    for (i, handler) in enumerate(root.handlers):
        if isinstance(handler.formatter, JSON):
            restore[i] = handler.formatter
            handler.formatter = handler.formatter.clone_with_extra(fields)
    yield

    for (i, formatter) in restore.items():
        root.handlers[i].formatter = formatter


class _Timer:
    _start: float
    _end: Optional[float]
    is_null: bool

    def __init__(self, start, is_null: bool = False):
        self._start = start
        self.is_null = is_null
        self._end = None

    @classmethod
    def start(cls):
        return cls(time.time())

    @classmethod
    def null(cls):
        return cls(0, is_null=True)

    def end(self):
        self._end = time.time()

    def total_seconds(self) -> Optional[float]:
        if self._end is None:
            return None
        return self._end - self._start


def _to_exception_metadata(exc: Exception, timer: _Timer) -> dict:
    extra = {"status": Status.FAILURE}
    if hasattr(exc, "code"):
        extra["type"] = exc.code  # type: ignore
    else:
        extra["type"] = to_kebab_case(exc.__class__.__name__)
    if not timer.is_null:
        extra["duration"] = timer.total_seconds()  # type: ignore
    return extra


def _to_success_metadata(timer: _Timer):
    extra = {"status": Status.SUCCESS}
    if not timer.is_null:
        extra["duration"] = timer.total_seconds()  # type: ignore
    return extra


def log_status(
    log,
    message: Optional[str] = None,
    non_fatal: Tuple[Exception, ...] = tuple(),
    include_duration: bool = False,
):
    def wrapper(func):
        msg = message if message is not None else func.__name__

        @wraps(func)
        def fn(*args, **kwargs):
            timer = _Timer.start() if include_duration else _Timer.null()
            try:
                result = func(*args, **kwargs)
                timer.end()
                log.info(msg, extra=_to_success_metadata(timer))
                return result
            except non_fatal as exc:
                timer.end()
                log.warning(msg, extra=_to_exception_metadata(exc, timer))
            except Exception as exc:
                timer.end()
                log.error(msg, extra=_to_exception_metadata(exc, timer))
                raise exc

        return fn

    return wrapper
