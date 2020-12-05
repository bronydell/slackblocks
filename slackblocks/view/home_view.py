from typing import List, Optional, Dict, Any

from slackblocks.slackblocks.elements.base_elements import Element
from slackblocks.slackblocks.view.base_view import BaseSlackView, SlackViewType


class HomeSlackView(BaseSlackView):
    def __init__(self,
                 blocks: Optional[List[Element]] = None,
                 private_metadata: Optional[Dict[str, Any]] = None,
                 callback_id: Optional[str] = None,
                 external_id: Optional[str] = None):
        super().__init__(SlackViewType.HOME, blocks, private_metadata, callback_id, external_id)

    def _resolve(self) -> Dict[str, Any]:
        return self._attributes()
