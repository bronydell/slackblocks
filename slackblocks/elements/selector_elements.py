from typing import Any, Dict, Optional, Union, List
from slackblocks.slackblocks.errors import InvalidUsageError

from .base_elements import Text, Element, ElementType
from .common_elements import Confirm


class OptionObject:
    def __init__(self,
                 text: Union[str, Text],
                 value: str,
                 description: Optional[Union[str, Text]] = None,
                 url: Optional[str] = None):
        self.text = Text.to_text(text, max_length=75, force_plaintext=True)
        self.value = value
        self.description = Text.to_text(description, max_length=75, force_plaintext=True)
        self.url = url

    def _resolve(self) -> Dict[str, Any]:
        option = dict()
        option["text"] = self.text._resolve()
        option["value"] = self.value
        if self.description:
            option["description"] = self.description._resolve()
        if self.url:
            option["url"] = self.url
        return option


class OptionGroup:
    def __init__(self, label: Union[str, Text], options: List[OptionObject]):
        self.label = Text.to_text(label, max_length=75, force_plaintext=True)
        self.options = options

    def _resolve(self) -> Dict[str, Any]:
        option_group = dict()
        option_group["label"] = self.label._resolve()
        option_group["options"] = [option._resolve() for option in self.options]
        return option_group


class StaticSelect(Element):
    def __init__(self,
                 action_id: str,
                 placeholder: Union[str, Text],
                 options: Optional[List[Union[OptionObject]]] = None,
                 option_group: Optional[OptionGroup] = None,
                 initial_option: Optional[str] = None,
                 confirm: Optional[Confirm] = None):
        super().__init__(ElementType.STATIC_SELECT)
        if not options and not option_group:
            raise InvalidUsageError("Either options or option group should be passed")
        if options and option_group:
            raise InvalidUsageError("Both options and option group cannot be passed")

        self.action_id = action_id
        self.options = options
        self.option_group = option_group
        self.placeholder = Text.to_text(placeholder, max_length=150, force_plaintext=True)
        self.initial_option = initial_option
        self.confirm = confirm

    def _resolve(self) -> Dict[str, Any]:
        element = self._attributes()
        element["placeholder"] = self.placeholder._resolve()
        element["action_id"] = self.action_id
        if self.options:
            element["options"] = [option._resolve() for option in self.options]
        elif self.option_group:
            element["option_group"] = self.option_group._resolve()
        if self.initial_option:
            element["initial_option"] = self.initial_option._resolve()
        if self.confirm:
            element["confirm"] = self.confirm._resolve()
        return element


class CheckboxSelector(Element):
    def __init__(self,
                 action_id: str,
                 options: List[OptionObject] = None,
                 initial_options: Optional[List[OptionObject]] = None,
                 confirm: Optional[Confirm] = None):
        super().__init__(ElementType.CHECKBOXES)

        self.action_id = action_id
        self.options = options
        self.initial_options = initial_options
        self.confirm = confirm

    def _resolve(self) -> Dict[str, Any]:
        element = self._attributes()
        element["action_id"] = self.action_id
        if self.options:
            element["options"] = [option._resolve() for option in self.options]
        if self.initial_options:
            element["initial_options"] = [option._resolve() for option in self.initial_options]
        if self.confirm:
            element["confirm"] = self.confirm
        return element


class MultiUsersSelect(Element):
    def __init__(self,
                 action_id: str,
                 placeholder: Union[str, Text],
                 initial_users: Optional[List[str]] = None,
                 max_selected_items: Optional[int] = None,
                 confirm: Optional[Confirm] = None):
        super().__init__(ElementType.MULTI_USERS_SELECT)

        self.action_id = action_id
        self.initial_users = initial_users
        self.placeholder = Text.to_text(placeholder, max_length=150, force_plaintext=True)
        self.max_selected_items = max_selected_items
        self.confirm = confirm

    def _resolve(self) -> Dict[str, Any]:
        element = self._attributes()
        element["placeholder"] = self.placeholder._resolve()
        element["action_id"] = self.action_id
        if self.max_selected_items:
            element["max_selected_items"] = self.max_selected_items
        elif self.initial_users:
            element["initial_users"] = self.initial_users
        if self.confirm:
            element["confirm"] = self.confirm
        return element
