from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Message import Message
from gdo.base.Render import Mode
from gdo.base.Util import Strings, html
from gdo.core.GDO_Channel import GDO_Channel
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Channel import GDT_Channel
from gdo.core.GDT_Creator import GDT_Creator
from gdo.date.GDT_Created import GDT_Created


class GDO_Bridge(GDO):

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('bridge_id'),
            GDT_Channel('bridge_a'),
            GDT_Channel('bridge_b'),
            GDT_Creator('bridge_creator'),
            GDT_Created('bridge_created'),
        ]

    @classmethod
    def for_message(cls, message: Message) -> list['GDO_Bridge']:
        chan_id = message._env_channel.get_id()
        return cls.table().select().where(f"bridge_a={chan_id} OR bridge_b={chan_id}").exec().fetch_all()

    def get_channel_a(self) -> GDO_Channel:
        return self.gdo_value('bridge_a')

    def get_channel_b(self) -> GDO_Channel:
        return self.gdo_value('bridge_b')

    def get_target_channel(self, message: Message) -> GDO_Channel:
        a = self.get_channel_a()
        b = self.get_channel_b()
        curr = message._env_channel
        if curr == a:
            return b
        elif curr == b:
            return a

    async def bridge_incoming(self, message: Message):
        target = self.get_target_channel(message)
        t_serv = target.get_server()
        msg = Message('', Mode.TXT).env_copy(message).env_channel(target).env_server(t_serv).result(message._message)
        await msg.get_connector().send_to_channel(msg, False)

    async def bridge_outgoing(self, message: Message):
        target = self.get_target_channel(message)
        t_serv = target.get_server()
        msg = Message('', Mode.TXT).env_copy(message).env_channel(target).env_server(t_serv).result(html(Strings.html_to_text(message._result)))
        await msg.get_connector().send_to_channel(msg, False)
