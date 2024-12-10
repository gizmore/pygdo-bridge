from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.bridge.GDO_Bridge import GDO_Bridge
from gdo.core.GDO_Channel import GDO_Channel
from gdo.core.GDT_Channel import GDT_Channel


class bridge(Method):

    def gdo_trigger(self) -> str:
        return 'bridge'

    def gdo_in_private(self) -> bool:
        return False

    def gdo_parameters(self) -> [GDT]:
        return [
            GDT_Channel('target_channel').not_null(),
        ]

    def get_target_channel(self) -> GDO_Channel:
        return self.param_value('target_channel')

    def gdo_execute(self):
        target = self.get_target_channel()
        GDO_Bridge.blank({
            'bridge_a': self._env_channel.get_id(),
            'bridge_b': target.get_id(),
        }).insert()
        return self.reply('msg_bridged')