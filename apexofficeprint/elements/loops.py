from .elements import Element
from typing import Iterable, FrozenSet

class ForEach(Element):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name)
        self._content = list(content)
        self._tags = {
            "{#" + name + "}",
            "{/" + name + "}"
        }

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value: Iterable[Element]):
        self._content = value

    @property
    def available_tags(self) -> FrozenSet[str]:
        result = self._tags

        for element in self.content:
            result |= element.available_tags

        return frozenset(result)

    @property
    def as_dict(self):
        return {
            self.name: [element.as_dict for element in self.content]
        }


class Labels(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{-" + name + "}"
        }


class ForEachSlide(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{!" + name + "}"
        }


class ForEachInline(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{:" + name + "}",
            "{/" + name + "}"
        }


class ForEachTableRow(ForEach):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name, content)
        self._tags = {
            "{=" + name + "}",
            "{/" + name + "}"
        }


# These are the same, but they may not be forever
# and combining them into one class breaks consistency
ForEachSheet = ForEachSlide  # TODO: sheet name
ForEachHorizontal = ForEachInline