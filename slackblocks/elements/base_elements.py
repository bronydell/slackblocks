from abc import ABC, abstractmethod
from enum import Enum
from json import dumps
from typing import Any, Dict, Optional, Union

from slackblocks.slackblocks.errors import InvalidUsageError


class ElementType(Enum):
    """
    Convenience class for referencing the various message elements Slack
    provides.
    """
    TEXT = "text"
    IMAGE = "image"
    TIME_PICKER = "timepicker"
    DATE_PICKER = "datepicker"
    STATIC_SELECT = "static_select"
    CHECKBOXES = "checkboxes"
    MULTI_USERS_SELECT = "multi_users_select"
    BUTTON = "button"
    CONFIRM = "confirm"
    PLAIN_TEXT_INPUT = "plain_text_input"


class TextType(Enum):
    """
    Allowable types for Slack Text objects.
    N.B: some usages of Text objects only allow the plaintext variety.
    """
    MARKDOWN = "mrkdwn"
    PLAINTEXT = "plain_text"


class Element(ABC):
    """
    Basis element containing attributes and behaviour common to all elements.
    N.B: Element is an abstract class and cannot be used directly.
    """
    def __init__(self, type_: ElementType):
        super().__init__()
        self.type = type_

    def _attributes(self) -> Dict[str, Any]:
        return {
            "type": self.type.value
        }

    @abstractmethod
    def _resolve(self) -> Dict[str, Any]:
        pass


class Text(Element):
    """
    An object containing some text, formatted either as plain_text or using
    Slack's "mrkdwn"
    """
    def __init__(self,
                 text: str,
                 type_: TextType = TextType.MARKDOWN,
                 emoji: bool = False,
                 verbatim: bool = False):
        super().__init__(type_=ElementType.TEXT)
        self.text_type = type_
        self.text = text
        if self.text_type == TextType.MARKDOWN:
            self.verbatim = verbatim
            self.emoji = None
        elif self.text_type == TextType.PLAINTEXT:
            self.verbatim = None
            self.emoji = emoji

    def _resolve(self) -> Dict[str, Any]:
        text = {
            "type": self.text_type.value,
            "text": self.text,
        }
        if self.text_type == TextType.MARKDOWN:
            text["verbatim"] = self.verbatim
        elif self.type == TextType.PLAINTEXT and self.emoji:
            text["emoji"] = self.emoji
        return text

    @staticmethod
    def to_text(text: Optional[Union[str, "Text"]],
                force_plaintext=False,
                max_length: Optional[int] = None) ->  Optional["Text"]:
        type_ = TextType.PLAINTEXT if force_plaintext else TextType.MARKDOWN
        if not text:
            return None
        if type(text) is str:
            if max_length and len(text) > max_length:
                raise InvalidUsageError("Text length exceeds Slack-imposed limit")
            return Text(text=text,
                        type_=type_)
        else:
            if max_length and len(text) > max_length:
                raise InvalidUsageError("Text length exceeds Slack-imposed limit")
            return Text(text=text.text,
                        type_=type_)

    def __str__(self) -> str:
        return dumps(self._resolve())
