import functools
import inspect
from typing import Any, Callable, cast, Dict, Tuple, Mapping, Generic, TypeVar
from opentrons.broker import Broker
from . import types as command_types


CacheT = TypeVar("CacheT")


class InspectMemoizer(Generic[CacheT]):
    def __init__(self, method: Callable[[Any], CacheT]) -> None:
        self._method = method
        self._cache: Dict[Callable, CacheT] = {}

    def get(self, f: Callable) -> CacheT:
        v = self._cache.get(f)
        if not v:
            v = self._method(f)
            self._cache[f] = v
        return v


signature_cache = InspectMemoizer(inspect.signature)
"""Cache inspect.signature method calls"""
getfullargspec_cache = InspectMemoizer(inspect.getfullargspec)
"""Cache inspect.getfullargspec method calls"""


class CommandPublisher:
    def __init__(self, broker: Broker) -> None:
        self._broker = broker or Broker()

    @property
    def broker(self) -> Broker:
        return self._broker

    @broker.setter
    def broker(self, broker: Broker) -> None:
        self._broker = broker


CmdFunction = Callable[..., command_types.Command]


def do_publish(
        broker: Broker,
        cmd: CmdFunction,
        f: Callable,
        when: command_types.MessageSequenceId,
        res: Any,
        meta: Any,
        *args: Any, **kwargs: Any) -> None:
    """ Implement the publish so it can be called outside the decorator """
    publish_command = functools.partial(
        broker.publish,
        topic=command_types.COMMAND)
    call_args = _get_args(f, args, kwargs)
    if when == 'before':
        broker.logger.info("{}: {}".format(
            f.__qualname__,
            {k: v for k, v in call_args.items() if str(k) != 'self'}))
    getfullargspec = getfullargspec_cache.get(cmd)
    command_args = dict(
        zip(
            reversed(getfullargspec.args),
            reversed(getfullargspec.defaults
                     or [])))

    # TODO (artyom, 20170927): we are doing this to be able to use
    # the decorator in Instrument class methods, in which case
    # self is effectively an instrument.
    # To narrow the scope of this hack, we are checking if the
    # command is expecting instrument first.
    if 'instrument' in getfullargspec.args:
        # We are also checking if call arguments have 'self' and
        # don't have instruments specified, in which case
        # instruments should take precedence.
        if 'instrument' not in call_args and 'self' in call_args:
            call_args['instrument'] = call_args['self']

    command_args.update({
        key: call_args[key]
        for key in
        (set(getfullargspec.args)
         & call_args.keys())
    })

    if meta:
        command_args['meta'] = meta

    payload = cmd(**command_args)

    publish_command(
        message={**payload, '$': when})


def publish_paired(
        broker: Broker,
        cmd: CmdFunction,
        when: command_types.MessageSequenceId,
        res: Any,
        *args: Any,
        pub_type: str = 'Paired Pipettes') -> None:
    """ Implement a second publisher outside of the decorator that
    relies on the method providing all of the arguments required
    rather than binding defaults to the signature"""
    publish_command = functools.partial(
        broker.publish,
        topic=command_types.COMMAND)

    payload = cmd(*args, pub_type)

    publish_command(message={**payload, '$': when})


def _publish_dec(
        before: bool,
        after: bool,
        command: CmdFunction,
        meta: Any = None):  # noqa: ANN202
    def _decorator(f: Callable):  # noqa: ANN202,ANN003,ANN002
        @functools.wraps(
            f,
            updated=functools.WRAPPER_UPDATES+('__globals__',))  # type: ignore
        def _decorated(*args, **kwargs):  # noqa: ANN202,ANN003,ANN002
            try:
                broker = cast(Broker, args[0].broker)
            except AttributeError:
                raise RuntimeError("Only methods of CommandPublisher \
                    classes should be decorated.")
            if before:
                do_publish(
                    broker, command, f, 'before', None, meta, *args, **kwargs)
            res = f(*args, **kwargs)
            if after:
                do_publish(
                    broker, command, f, 'after', res, meta, *args, **kwargs)
            return res
        return _decorated

    return _decorator


class publish:
    """ Class that allows namespaced decorators with valid mypy types

    These were previously defined by adding them as attributes to the
    publish function, which is not currently supported by mypy:
    https://github.com/python/mypy/issues/2087

    Making a simple class with these as attributes does the same thing
    but in a way that mypy can actually verify.

    Only commands inheriting from class CommandPublisher should contain
    decorators.
    """
    before = functools.partial(_publish_dec, before=True, after=False)
    after = functools.partial(_publish_dec, before=False, after=True)
    both = functools.partial(_publish_dec, before=True, after=True)


def _get_args(
        f: Callable,
        args: Tuple,
        kwargs: Mapping[str, Any]) -> Dict[str, Any]:
    # Create the initial dictionary with args that have defaults
    res = {}
    sig = signature_cache.get(f)
    ismethod = inspect.ismethod(f)
    if ismethod and args[0] is f.__self__:  # type: ignore
        args = args[1:]
    if ismethod:
        res['self'] = f.__self__  # type: ignore

    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()
    res.update(bound.arguments)
    return res
