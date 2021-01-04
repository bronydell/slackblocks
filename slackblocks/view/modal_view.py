from typing import List, Optional, Dict, Any, Union

from slackblocks.slackblocks.blocks import InputBlock, Block
from slackblocks.slackblocks.elements.base_elements import Text
from slackblocks.slackblocks.errors import InvalidUsageError
from slackblocks.slackblocks.view.base_view import BaseSlackView, SlackViewType


class ModalSlackView(BaseSlackView):
    def __init__(self,
                 title: Union[str, Text],
                 close: Optional[Union[str, Text]] = None,
                 submit: Optional[Union[str, Text]] = None,
                 blocks: Optional[List[Block]] = None,
                 private_metadata: Optional[Dict[str, Any]] = None,
                 clear_on_close: Optional[bool] = None,
                 notify_on_close: Optional[bool] = None,
                 callback_id: Optional[str] = None,
                 external_id: Optional[str] = None):
        super().__init__(SlackViewType.MODAL, blocks, private_metadata, callback_id, external_id)
        self.title = Text.to_text(title, force_plaintext=True, max_length=24)
        self.close = Text.to_text(close, force_plaintext=True, max_length=24)
        self.submit = Text.to_text(submit, force_plaintext=True, max_length=24)
        self.clear_on_close = clear_on_close
        self.notify_on_close = notify_on_close

    def _resolve(self) -> Dict[str, Any]:
        view = self._attributes()
        view["title"] = self.title._resolve()
        if self.submit:
            view["submit"] = self.submit._resolve()
        elif any(isinstance(x, (int, InputBlock)) for x in self.blocks):
            raise InvalidUsageError("You have to send Submit text if you have at least one InputBlock."
                                    " Read: https://api.slack.com/reference/surfaces/views")
        if self.close:
            view["close"] = self.close._resolve()
        if self.clear_on_close:
            view["clear_on_close"] = self.clear_on_close
        if self.notify_on_close:
            view["notify_on_close"] = self.notify_on_close
        return view
