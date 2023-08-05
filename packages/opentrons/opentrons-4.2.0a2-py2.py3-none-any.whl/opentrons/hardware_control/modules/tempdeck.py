import asyncio
import logging
from threading import Thread, Event
from typing import Mapping, Union, Optional
from opentrons.drivers.temp_deck import (
    SimulatingDriver, TempDeck as TempDeckDriver)
from opentrons.drivers.temp_deck.driver import temp_locks
from ..execution_manager import ExecutionManager
from . import update, mod_abc, types

log = logging.getLogger(__name__)

TEMP_POLL_INTERVAL_SECS = 1

FIRST_GEN2_REVISION = 20


def _model_from_revision(revision: Optional[str]) -> str:
    """ Defines the revision -> model mapping"""
    if not revision or 'v' not in revision:
        log.error(f'bad revision: {revision}')
        return 'temperatureModuleV1'
    try:
        revision_num = float(revision.split('v')[-1])  # type: ignore
    except (ValueError, TypeError):
        # none or corrupt
        log.exception('no revision')
        return 'temperatureModuleV1'

    if revision_num < FIRST_GEN2_REVISION:
        return 'temperatureModuleV1'
    else:
        return 'temperatureModuleV2'


class MissingDevicePortError(Exception):
    pass


class Poller(Thread):
    def __init__(self, driver: Union[TempDeckDriver, SimulatingDriver]):
        self._driver_ref = driver
        self._stop_event = Event()
        super().__init__(target=self._poll_temperature,
                         name='Temperature poller for tempdeck')

    def _poll_temperature(self):
        while not self._stop_event.wait(TEMP_POLL_INTERVAL_SECS):
            self._driver_ref.update_temperature()

    def stop(self):
        self._stop_event.set()


class TempDeck(mod_abc.AbstractModule):
    """
    Under development. API subject to change without a version bump
    """
    @classmethod
    async def build(cls,
                    port: str,
                    execution_manager: ExecutionManager,
                    interrupt_callback: types.InterruptCallback = None,
                    simulating: bool = False,
                    loop: asyncio.AbstractEventLoop = None,
                    sim_model: str = None):

        """ Build and connect to a TempDeck"""
        # TempDeck does not currently use interrupts, so the callback is not
        # passed on
        mod = cls(port=port,
                  simulating=simulating,
                  loop=loop,
                  execution_manager=execution_manager,
                  sim_model=sim_model)
        await mod._connect()
        return mod

    @classmethod
    def name(cls) -> str:
        return 'tempdeck'

    def model(self) -> str:
        return _model_from_revision(self._device_info.get('model'))

    @classmethod
    def bootloader(cls) -> mod_abc.UploadFunction:
        return update.upload_via_avrdude

    @staticmethod
    def _build_driver(
            simulating: bool,
            sim_model: str = None
    ) -> Union['SimulatingDriver', 'TempDeckDriver']:
        if simulating:
            return SimulatingDriver(sim_model=sim_model)
        else:
            return TempDeckDriver()

    def __init__(self,
                 port: str,
                 execution_manager: ExecutionManager,
                 simulating: bool,
                 loop: asyncio.AbstractEventLoop = None,
                 sim_model: str = None) -> None:
        super().__init__(port=port,
                         simulating=simulating,
                         loop=loop,
                         execution_manager=execution_manager,
                         sim_model=sim_model)
        self._device_info: Mapping[str, str] = {}
        self._driver: Union['SimulatingDriver', 'TempDeckDriver']
        if temp_locks.get(port):
            self._driver = temp_locks[port][1]
        else:
            self._driver = self._build_driver(
                simulating, sim_model)

        self._poller: Optional[Poller] = None

    async def set_temperature(self, celsius: float):
        """
        Set temperature in degree Celsius
        Range: 4 to 95 degree Celsius (QA tested).
        The internal temp range is -9 to 99 C, which is limited by the 2-digit
        temperature display. Any input outside of this range will be clipped
        to the nearest limit
        """
        await self.wait_for_is_running()
        task = self._loop.create_task(self._driver.set_temperature(celsius))
        await self.make_cancellable(task)
        return await task

    async def start_set_temperature(self, celsius):
        """
        Set temperature in degree Celsius
        Range: 4 to 95 degree Celsius (QA tested).
        The internal temp range is -9 to 99 C, which is limited by the 2-digit
        temperature display. Any input outside of this range will be clipped
        to the nearest limit
        """
        await self.wait_for_is_running()
        return self._driver.start_set_temperature(celsius)

    async def await_temperature(self, awaiting_temperature: float):
        """
        Await temperature in degree Celsius
        Polls temperature module's temperature until
        the specified temperature is reached
        """
        await self.wait_for_is_running()

        async def _await_temperature(awaiting_temperature: float):
            status = self.status

            if status == 'heating':
                while self.temperature < awaiting_temperature:
                    await asyncio.sleep(0.2)

            elif status == 'cooling':
                while self.temperature > awaiting_temperature:
                    await asyncio.sleep(0.2)

        t = self._loop.create_task(_await_temperature(awaiting_temperature))
        await self.make_cancellable(t)
        await t

    async def deactivate(self):
        """ Stop heating/cooling and turn off the fan """
        await self.wait_for_is_running()
        self._driver.deactivate()

    @property
    def device_info(self) -> Mapping[str, str]:
        return self._device_info

    @property
    def live_data(self) -> types.LiveData:
        return {
            'status': self.status,
            'data': {
                'currentTemp': self.temperature,
                'targetTemp': self.target
            }
        }

    @property
    def temperature(self) -> float:
        return self._driver.temperature

    @property
    def target(self) -> Optional[float]:
        return self._driver.target

    @property
    def status(self) -> str:
        return self._driver.status

    @property
    def port(self) -> str:
        return self._port

    @property
    def is_simulated(self) -> bool:
        return isinstance(self._driver, SimulatingDriver)

    @property
    def interrupt_callback(self) -> types.InterruptCallback:
        return lambda x: None

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop

    async def _connect(self):
        """
        Connect to the 'TempDeck' port
        Planned change- will connect to the correct port in case of multiple
        TempDecks
        """
        if self._poller:
            self._poller.stop()
            self._poller.join()
        if not self._driver.is_connected():
            self._driver.connect(self._port)
        self._device_info = self._driver.get_device_info()
        self._poller = Poller(self._driver)
        self._poller.start()

    def __del__(self):
        if hasattr(self, '_poller') and self._poller:
            self._poller.stop()

    async def prep_for_update(self) -> str:
        model = self._device_info and self._device_info.get('model')
        if model in ('temp_deck_v1', 'temp_deck_v1.1', 'temp_deck_v2'):
            raise types.UpdateError("This Temperature Module can't be updated."
                                    "Please contact Opentrons Support.")

        if self._poller:
            self._poller.stop()
            self._poller.join()
        del self._poller
        self._poller = None
        self._driver.enter_programming_mode()
        new_port = await update.find_bootloader_port()
        return new_port or self.port

    def has_available_update(self) -> bool:
        """ Override of abc implementation to suppress update notifications
        for v1, v1.1, and v2 temperature modules which cannot be updated """
        if not self._device_info:
            model = None
        else:
            model = self._device_info.get('model')
        if model in {'temp_deck_v1', 'temp_deck_v1.1', 'temp_deck_v2', None}:
            return False
        return super().has_available_update()
