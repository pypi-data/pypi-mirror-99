import asyncio
import typing

import pychromecast

from . import Device, DeviceFinder, RoutersDefType, DevicePlayerFunction
from .. import Config
from ..tools import run_method_in_executor


__all__ = [
    "ChromecastDevice",
    "ChromecastDeviceFinder"
]


class ChromecastDevice(Device):
    _device: pychromecast.Chromecast

    def __init__(self, device: typing.Any):
        self._device = device
        self._device.wait()

    def get_device_name(self) -> str:
        return self._device.device.friendly_name

    async def stop(self):
        pass

    @run_method_in_executor
    def play(self, url: str, title: str):
        self._device.media_controller.play_media(url, "video/mp4", title=title)
        self._device.media_controller.block_until_active()

    def get_player_functions(self) -> typing.List[DevicePlayerFunction]:
        return []

    def __del__(self):
        self._device.disconnect(blocking=False)


class ChromecastDeviceFinder(DeviceFinder):
    async def find(self, config: Config) -> typing.List[Device]:
        devices: typing.List[pychromecast.Chromecast] = list()

        def callback(device: pychromecast.Chromecast):
            devices.append(device)

        browser = pychromecast.get_chromecasts(
            timeout=config.chromecast_scan_timeout,
            blocking=False,
            callback=callback)

        await asyncio.sleep(config.chromecast_scan_timeout)
        browser.cancel()
        return [ChromecastDevice(device) for device in devices]

    @staticmethod
    def is_enabled(config: Config) -> bool:
        return config.chromecast_enabled

    async def get_routers(self, config: Config) -> RoutersDefType:
        return []
