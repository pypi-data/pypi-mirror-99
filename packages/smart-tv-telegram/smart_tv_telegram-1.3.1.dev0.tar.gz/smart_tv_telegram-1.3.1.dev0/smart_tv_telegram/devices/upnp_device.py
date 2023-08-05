import typing
from ipaddress import IPv4Address
from xml.sax.saxutils import escape

import async_upnp_client
from async_upnp_client import UpnpFactory, UpnpError
from async_upnp_client.aiohttp import AiohttpRequester
from async_upnp_client.search import async_search

from . import Device, DeviceFinder, RoutersDefType, DevicePlayerFunction
from .. import Config, Mtproto
from ..tools import ascii_only


__all__ = [
    "UpnpDevice",
    "UpnpDeviceFinder"
]


_AVTRANSPORT_SCHEMA = "urn:schemas-upnp-org:service:AVTransport:1"

_DLL_METADATA = """
<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
    xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/"
    xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
    <item id="R:0/0/0" parentID="R:0/0" restricted="true">
        <dc:title>{title}</dc:title>
        <upnp:class>object.item.videoItem.movie</upnp:class>
        <desc id="cdudn" nameSpace="urn:schemas-rinconnetworks-com:metadata-1-0/">
            SA_RINCON65031_
        </desc>
        <res protocolInfo="http-get:*:video/mp4:DLNA.ORG_OP=01;DLNA.ORG_CI=0;DLNA.ORG_FLAGS=01700000000000000000000000000000">{url}</res>
    </item>
</DIDL-Lite>
"""


class UpnpPlayFunction(DevicePlayerFunction):
    _service: async_upnp_client.UpnpService

    def __init__(self, service: async_upnp_client.UpnpService):
        self._service = service

    async def get_name(self) -> str:
        return "PLAY"

    async def handle(self, mtproto: Mtproto):
        play = self._service.action("Play")
        await play.async_call(InstanceID=0, Speed="1")

    async def is_enabled(self, config: Config):
        return config.upnp_enabled


class UpnpPauseFunction(DevicePlayerFunction):
    _service: async_upnp_client.UpnpService

    def __init__(self, service: async_upnp_client.UpnpService):
        self._service = service

    async def get_name(self) -> str:
        return "PAUSE"

    async def handle(self, mtproto: Mtproto):
        play = self._service.action("Pause")
        await play.async_call(InstanceID=0)

    async def is_enabled(self, config: Config):
        return config.upnp_enabled


class UpnpDevice(Device):
    _device: async_upnp_client.UpnpDevice
    _service: async_upnp_client.UpnpService

    def __init__(self, device: async_upnp_client.UpnpDevice):
        self._device = device
        self._service = self._device.service(_AVTRANSPORT_SCHEMA)

    def get_device_name(self) -> str:
        return self._device.friendly_name

    async def stop(self):
        stop = self._service.action("Stop")

        try:
            await stop.async_call(InstanceID=0)
        except UpnpError as error:
            if "Transition not available" not in str(error):
                raise error

    async def play(self, url: str, title: str):
        set_url = self._service.action("SetAVTransportURI")
        meta = _DLL_METADATA.format(title=escape(ascii_only(title)), url=escape(url))
        await set_url.async_call(InstanceID=0, CurrentURI=url, CurrentURIMetaData=meta)

        play = self._service.action("Play")
        await play.async_call(InstanceID=0, Speed="1")

    def get_player_functions(self) -> typing.List[DevicePlayerFunction]:
        return [
            UpnpPlayFunction(self._service),
            UpnpPauseFunction(self._service)
        ]


class UpnpDeviceFinder(DeviceFinder):
    async def find(self, config: Config) -> typing.List[Device]:
        devices = []
        requester = AiohttpRequester()
        factory = UpnpFactory(requester)
        source_ip = IPv4Address("0.0.0.0")

        async def on_response(data: typing.Mapping[str, typing.Any]) -> None:
            devices.append(await factory.async_create_device(data.get("LOCATION")))

        await async_search(service_type=_AVTRANSPORT_SCHEMA,
                           source_ip=source_ip,
                           timeout=config.upnp_scan_timeout,
                           async_callback=on_response)

        return [UpnpDevice(device) for device in devices]

    @staticmethod
    def is_enabled(config: Config) -> bool:
        return config.upnp_enabled

    async def get_routers(self, config: Config) -> RoutersDefType:
        return []
