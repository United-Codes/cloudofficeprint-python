from .elements import Element, Object, Property
from typing import Iterable, FrozenSet, Union, Mapping


class ForEach(Element):
    def __init__(self, name: str, content: Iterable[Element]):
        super().__init__(name)
        self._content = list(content)
        # if self._tags should be overwritten in a subclass of this one,
        # remember to do so after calling super().__init__
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


class ForEachSheet(ForEach):
    def __init__(self, name: str, content: Union[Iterable[Element], Mapping[str, Element]]):
        # when content is a mapping, it means "sheet name": content for that sheet
        # when it's just an iterable, don't add sheet names (or they can do the Property manually)
        if isinstance(content, Mapping):
            new_content = []
            for sheetname, sheetcontent in content:
                # we need to add the additional sheet_name property,
                # so we should convert the Element to to an Object if needed
                if not isinstance(sheetcontent, Object):
                    sheetcontent = Object.element_to_object(sheetcontent)
                # adding the new property containing sheet_name
                sheetcontent.add(Property("sheet_name", sheetname))
                new_content.append(sheetcontent)
            content = new_content
        # at this point, content is always Iterable[Element]

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
ForEachHorizontal = ForEachInline
