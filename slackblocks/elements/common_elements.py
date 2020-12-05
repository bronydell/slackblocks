from typing import Any, Dict, Optional, Union

from .base_elements import Text, Element, ElementType


class Image(Element):
    """
    An element to insert an image - this element can be used in section
    and context blocks only. If you want a block with only an image in it,
    you're looking for the image block.
    """
    def __init__(self,
                 image_url: str,
                 alt_text: str):
        super().__init__(type_=ElementType.IMAGE)
        self.image_url = image_url
        self.alt_text = alt_text

    def _resolve(self) -> Dict[str, Any]:
        image = self._attributes()
        image["image_url"] = self.image_url
        image["alt_text"] = self.alt_text
        return image


class Confirm(Element):
    """
    An object that defines a dialog that provides a confirmation step
    to any interactive element. This dialog will ask the user to confirm
    their action by offering confirm and deny buttons.
    """
    def __init__(self,
                 title: Union[str, Text],
                 text: Union[str, Text],
                 confirm: Union[str, Text],
                 deny: Union[str, Text]):
        super().__init__(type_=ElementType.CONFIRM)
        self.title = Text.to_text(title, max_length=100, force_plaintext=True)
        self.text = Text.to_text(text, max_length=300)
        self.confirm = Text.to_text(confirm, max_length=30, force_plaintext=True)
        self.deny = Text.to_text(deny, max_length=30, force_plaintext=True)

    def _resolve(self) -> Dict[str, Any]:
        return {
            "title": self.title._resolve(),
            "text": self.text._resolve(),
            "confirm": self.confirm._resolve(),
            "deny": self.deny._resolve()
        }


class Button(Element):
    """
    An interactive element that inserts a button. The button can be a
    trigger for anything from opening a simple link to starting a complex
    workflow.
    """
    def __init__(self,
                 text: Union[str, Text],
                 action_id: str,
                 url: Optional[str] = None,
                 value: Optional[str] = None,
                 style: Optional[str] = None,
                 confirm: Optional[Confirm] = None):
        super().__init__(type_=ElementType.BUTTON)
        self.text = Text.to_text(text, max_length=75, force_plaintext=True)
        self.action_id = action_id
        self.url = url
        self.value = value
        self.style = style
        self.confirm = confirm

    def _resolve(self) -> Dict[str, Any]:
        button = self._attributes()
        button["text"] = self.text._resolve()
        button["action_id"] = self.action_id
        if self.style:
            button["style"] = self.style
        if self.url:
            button["url"] = self.url
        if self.value:
            button["value"] = self.value
        if self.confirm:
            button["confirm"] = self.confirm._resolve()
        return button


class DispatchActionConfig:
    def __init__(self,
                 on_character_entered: bool = False,
                 on_enter_pressed: bool = False):
        self.on_character_entered = on_character_entered
        self.on_enter_pressed = on_enter_pressed

    def _resolve(self) -> Dict[str, Any]:
        actions = []
        if self.on_character_entered:
            actions.append("on_character_entered")
        if self.on_enter_pressed:
            actions.append("on_enter_pressed")

        return {
            "trigger_actions_on": actions
        }


class TextInput(Element):
    def __init__(self,
                 action_id: str,
                 placeholder: Optional[Union[str, Text]] = None,
                 initial_value: Optional[str] = None,
                 multiline: bool = False,
                 min_length: Optional[int] = None,
                 max_length: Optional[int] = None,
                 dispatch_config: Optional[DispatchActionConfig] = None):
        super().__init__(ElementType.PLAIN_TEXT_INPUT)
        self.action_id = action_id
        self.placeholder = Text.to_text(placeholder, max_length=150, force_plaintext=True)
        self.initial_value = initial_value
        self.multiline = multiline
        self.min_length = min_length
        self.max_length = max_length
        self.dispatch_config = dispatch_config

    def _resolve(self) -> Dict[str, Any]:
        inputfield = self._attributes()
        inputfield["action_id"] = self.action_id
        inputfield["multiline"] = self.multiline
        if self.placeholder:
            inputfield["placeholder"] = self.placeholder._resolve()
        if self.initial_value:
            inputfield["initial_value"] = self.initial_value
        if self.min_length:
            inputfield["min_length"] = self.min_length
        if self.max_length:
            inputfield["max_length"] = self.max_length
        if self.dispatch_config:
            inputfield["dispatch_action_config"] = self.dispatch_config._resolve()
        return inputfield
