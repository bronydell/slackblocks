from datetime import datetime, time
from typing import Any, Dict, Optional, Union
from .base_elements import Element, ElementType, Text
from .common_elements import Confirm


class TimePicker(Element):
    def __init__(self,
                 action_id: str,
                 initial_time: Optional[time] = None,
                 placeholder: Optional[Union[str, Text]] = None,
                 confirm: Optional[Confirm] = None):
        super().__init__(ElementType.TIME_PICKER)
        self.action_id = action_id
        self.placeholder = Text.to_text(placeholder, max_length=75, force_plaintext=True)
        self.initial_time = initial_time
        self.confirm = confirm

    def _resolve(self) -> Dict[str, Any]:
        time_picker = self._attributes()
        time_picker["placeholder"] = self.placeholder._resolve()
        time_picker["action_id"] = self.action_id
        if self.initial_time:
            time_picker["initial_time"] = self.initial_time.strftime("%H:%M")
        if self.confirm:
            time_picker["confirm"] = self.confirm._resolve()
        return time_picker


class DatePicker(Element):
    def __init__(self,
                 action_id: str,
                 initial_date: Optional[datetime],
                 placeholder: Optional[Union[str, Text]] = None,
                 confirm: Optional[Confirm] = None):
        super().__init__(ElementType.DATE_PICKER)
        self.action_id = action_id
        self.placeholder = Text.to_text(placeholder, max_length=75, force_plaintext=True)
        self.initial_date = initial_date
        self.confirm = confirm

    def _resolve(self) -> Dict[str, Any]:
        date_picker = self._attributes()
        date_picker["action_id"] = self.action_id
        if self.placeholder:
            date_picker["placeholder"] = self.placeholder._resolve()
        if self.initial_date:
            date_picker["initial_date"] = self.initial_date.strftime("%Y-%m-%d")
        if self.confirm:
            date_picker["confirm"] = self.confirm._resolve()
        return date_picker
