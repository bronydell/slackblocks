from abc import ABC, abstractmethod
from enum import Enum
from json import dumps
from typing import List, Optional, Dict, Any

from slackblocks.slackblocks.blocks import Block
from slackblocks.slackblocks.elements.base_elements import Element


class SlackViewType(Enum):
    """
    Convenience class for referencing the various views that Slack
    provides.
    """
    HOME = "home"
    MODAL = "modal"


class BaseSlackView(ABC):
    def __init__(self,
                 view_type: SlackViewType,
                 blocks: Optional[List[Block]] = None,
                 private_metadata: Optional[Dict[str, Any]] = None,
                 callback_id: Optional[str] = None,
                 external_id: Optional[str] = None,):
        if blocks is None:
            blocks = list()
        self.type = view_type
        self.blocks = blocks
        self.external_id = external_id
        self.callback_id = callback_id
        self.private_metadata = private_metadata

    def _attributes(self) -> Dict[str, Any]:
        attributes = {
            "type": self.type.value,
            "blocks": [block._resolve() for block in self.blocks]
        }

        if self.external_id:
            attributes["external_id"] = self.external_id
        if self.callback_id:
            attributes["callback_id"] = self.callback_id
        if self.private_metadata:
            attributes["private_metadata"] = dumps(self.private_metadata)
        return attributes

    @abstractmethod
    def _resolve(self) -> Dict[str, Any]:
        pass

