from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any

from slackblocks.slackblocks.view.modal_view import ModalSlackView


class ModalResponseAction(Enum):
    ERROR = "errors"
    CLOSE = "clear"
    UPDATE = "update"


class BaseModalResponse(ABC):
    def __init__(self,
                 response_action: ModalResponseAction):
        self.response_action = response_action

    def _attributes(self) -> Dict[str, Any]:
        return {
            "response_action": self.response_action.value
        }

    @abstractmethod
    def _resolve(self) -> Dict[str, Any]:
        pass


class EmptyModalResponse(BaseModalResponse):
    def __init__(self):
        # This won't actually be used, so anything will do
        super().__init__(ModalResponseAction.ERROR)

    def _resolve(self) -> Dict[str, Any]:
        return {}


class CloseModalResponse(BaseModalResponse):
    def __init__(self):
        super().__init__(ModalResponseAction.CLOSE)

    def _resolve(self) -> Dict[str, Any]:
        return self._attributes()


class ErrorModalResponse(BaseModalResponse):
    def __init__(self,
                 errors: Dict[str, str]):
        super().__init__(ModalResponseAction.ERROR)
        self.errors = errors

    def _resolve(self) -> Dict[str, Any]:
        response = self._attributes()
        response["errors"] = self.errors
        return response


class UpdateModalResponse(BaseModalResponse):
    def __init__(self,
                 modal: ModalSlackView):
        super().__init__(ModalResponseAction.UPDATE)
        self.modal = modal

    def _resolve(self) -> Dict[str, Any]:
        response = self._attributes()
        response["view"] = self.modal._resolve()
        return response
