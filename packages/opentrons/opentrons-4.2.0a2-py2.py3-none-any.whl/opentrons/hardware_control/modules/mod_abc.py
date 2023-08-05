import abc
import asyncio
import logging
import re
from pkg_resources import parse_version
from typing import Mapping, Optional
from opentrons.config import IS_ROBOT, ROBOT_FIRMWARE_DIR
from opentrons.hardware_control.util import use_or_initialize_loop
from ..execution_manager import ExecutionManager
from .types import BundledFirmware, UploadFunction, InterruptCallback, LiveData

mod_log = logging.getLogger(__name__)


class AbstractModule(abc.ABC):
    """ Defines the common methods of a module. """

    @classmethod
    @abc.abstractmethod
    async def build(cls,
                    port: str,
                    execution_manager: ExecutionManager,
                    interrupt_callback: InterruptCallback = None,
                    simulating: bool = False,
                    loop: asyncio.AbstractEventLoop = None,
                    sim_model: str = None) \
            -> 'AbstractModule':
        """ Modules should always be created using this factory.

        This lets the (perhaps blocking) work of connecting to and initializing
        a module be in a place that can be async.
        """
        pass

    @abc.abstractmethod
    def __init__(self,
                 port: str,
                 execution_manager: ExecutionManager,
                 simulating: bool = False,
                 loop: asyncio.AbstractEventLoop = None,
                 sim_model: str = None) -> None:
        self._port = port
        self._loop = use_or_initialize_loop(loop)
        self._execution_manager = execution_manager
        self._device_info: Mapping[str, str]
        self._bundled_fw: Optional[BundledFirmware] = self.get_bundled_fw()

    def get_bundled_fw(self) -> Optional[BundledFirmware]:
        """ Get absolute path to bundled version of module fw if available. """
        if not IS_ROBOT:
            return None
        name_to_fw_file_prefix = {
            "tempdeck": "temperature-module", "magdeck": "magnetic-module"}
        name = self.name()
        file_prefix = name_to_fw_file_prefix.get(name, name)

        MODULE_FW_RE = re.compile(f'^{file_prefix}@v(.*)[.](hex|bin)$')
        for fw_resource in ROBOT_FIRMWARE_DIR.iterdir():  # type: ignore
            matches = MODULE_FW_RE.search(fw_resource.name)
            if matches:
                return BundledFirmware(version=matches.group(1),
                                       path=fw_resource)

        mod_log.info(f"no available fw file found for: {file_prefix}")
        return None

    def has_available_update(self) -> bool:
        """ Return whether a newer firmware file is available """
        if self._device_info and self._bundled_fw:
            device_version = parse_version(self._device_info['version'])
            available_version = parse_version(self._bundled_fw.version)
            return available_version > device_version
        return False

    async def wait_for_is_running(self):
        if not self.is_simulated:
            await self._execution_manager.wait_for_is_running()

    async def make_cancellable(self, task: asyncio.Task):
        self._execution_manager.register_cancellable_task(task)

    @abc.abstractmethod
    def deactivate(self):
        """ Deactivate the module. """
        pass

    @property
    @abc.abstractmethod
    def status(self) -> str:
        """ Return some string describing status. """
        pass

    @property
    @abc.abstractmethod
    def device_info(self) -> Mapping[str, str]:
        """ Return a dict of the module's static information (serial, etc)"""
        pass

    @property
    @abc.abstractmethod
    def live_data(self) -> LiveData:
        """ Return a dict of the module's dynamic information """
        pass

    @property
    @abc.abstractmethod
    def is_simulated(self) -> bool:
        """ True if >this is a simulated module. """
        pass

    @property
    @abc.abstractmethod
    def port(self) -> str:
        """ The port where the module is connected. """
        pass

    @abc.abstractmethod
    async def prep_for_update(self) -> str:
        """ Prepare for an update.

        By the time this coroutine completes, the hardware should be ready
        to take an update. This implicitly tears down the module instance;
        it does not need to be either working or recoverable after this
        coroutine completes.

        :returns str: The port we're running on.
        """
        pass

    @property
    @abc.abstractmethod
    def interrupt_callback(self) -> InterruptCallback:
        pass

    @property
    def bundled_fw(self):
        return self._bundled_fw

    @abc.abstractmethod
    def model(self) -> str:
        """ A name for this specific module, matching module defs """
        pass

    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        """ A shortname used for looking up firmware, among other things """
        pass

    @classmethod
    @abc.abstractmethod
    def bootloader(cls) -> UploadFunction:
        """ Method used to upload file to this module's bootloader. """
        pass
