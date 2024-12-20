from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.bridge.GDO_Bridge import GDO_Bridge
from gdo.core.GDO_Channel import GDO_Channel
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_Channel import GDT_Channel


class unbridge(Method):
    """
    Remove one or all chat channel bridge(s)
    """

    def gdo_trigger(self) -> str:
        return 'unbridge'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_Bool('all').not_null().initial('0'),
            GDT_Channel('target_channel').positional(),
        ]

    def get_target_channel(self) -> GDO_Channel:
        return self.param_value('target_channel')

    async def gdo_execute(self) -> GDT:
        a = self._env_channel.get_id()
        query = GDO_Bridge.table().select()
        if self.param_value('all'):
            bridges = query.where(f'bridge_a={a} OR bridge_b={a}').exec()
            for bridge in bridges:
                bridge.delete()
            return self.reply('msg_unbridged_all', [self._env_channel.render_name()])
        b = self.get_target_channel().get_id()
        bridge = query.where(f'(bridge_a={a} AND bridge_b={b}) OR (bridge_a={b} AND bridge_b={a})').first().exec().fetch_object()
        bridge.delete()
        return self.reply('msg_unbridged', [self.get_target_channel().render_name(), self._env_channel.render_name()])
