from gdo.base.Application import Application
from gdo.base.GDO_Module import GDO_Module
from gdo.base.Message import Message
from gdo.bridge.GDO_Bridge import GDO_Bridge


class module_bridge(GDO_Module):

    def gdo_classes(self):
        return [
            GDO_Bridge,
        ]

    async def gdo_subscribe_events(self):
        Application.EVENTS.subscribe('new_message', self.on_incoming)
        Application.EVENTS.subscribe('msg_sent', self.on_outgoing)

    async def on_incoming(self, message: Message):
        if message._env_channel:
            if bridges := GDO_Bridge.for_message(message):
                for bridge in bridges:
                    await bridge.bridge_incoming(message)

    async def on_outgoing(self, message: Message):
        if message._env_channel:
            if bridges := GDO_Bridge.for_message(message):
                for bridge in bridges:
                   await bridge.bridge_outgoing(message)
