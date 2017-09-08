import typing
from typing import Any
from ..types.assignor import MasterAssignorT
from ..types.topics import TopicT
from ..types.tuples import TopicPartition
from ..utils.objects import cached_property
from ..utils.services import Service


if typing.TYPE_CHECKING:
    from ..app import AppT
else:
    class AppT: ...      # noqa


class MasterAssignor(Service, MasterAssignorT):

    def __init__(self, app: AppT, **kwargs: Any) -> None:
        Service.__init__(self, **kwargs)
        self.app = app

    async def on_first_start(self) -> None:
        await self._master_topic.maybe_declare()

    @cached_property
    def _master_topic(self) -> TopicT:
        return self.app.topic(
            self._master_topic_name,
            partitions=1,
        )

    @cached_property
    def _master_topic_name(self) -> str:
        return f'__{self.app.id}-__assignor-__master'

    @cached_property
    def _master_tp(self) -> TopicPartition:
        return TopicPartition(self._master_topic_name, 0)

    def is_master(self) -> bool:
        consumer = self.app.consumer
        return self._master_tp in consumer.assignment()
