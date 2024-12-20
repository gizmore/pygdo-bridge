from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.bridge.GDO_Bridge import GDO_Bridge
from gdo.core.GDO_Channel import GDO_Channel
from gdo.core.GDT_Channel import GDT_Channel


class bridge(Method):
    """
    Bridge 2 GDO_Channels.
    Lower ID is bridge_a
    """

    def gdo_trigger(self) -> str:
        return 'bridge'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Channel('target_channel').not_null(),
        ]

    def get_target_channel(self) -> GDO_Channel:
        return self.param_value('target_channel')

    async def gdo_execute(self) -> GDT:
        target = self.get_target_channel()
        a = self._env_channel.get_id()
        b = target.get_id()
        GDO_Bridge.blank({
            'bridge_a': min(a, b),
            'bridge_b': max(a, b),
        }).insert()
        return self.reply('msg_bridged', [target.render_name()])
