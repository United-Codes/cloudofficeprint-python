import sys
sys.path.insert(0, "PATH TO_COP_DIR")
import cloudofficeprint as cop


def test_textbox_from_docs():
    tb = cop.elements.Textbox(name="first_name")
    expected = {
        "type": "text",
        "name": "first_name"
    }
    assert tb.as_dict == expected
    assert tb.available_tags == frozenset({"{?form first_name}"})

    tb2 = cop.elements.Textbox(
        name="last_name",
        value="Apex R&D",
        height=20,
        width=200,
        multiline=True
    )
    expected2 = {
        "type": "text",
        "name": "last_name",
        "value": "Apex R&D",
        "height": 20,
        "width": 200,
        "multiline": True
    }
    assert tb2.as_dict == expected2
    assert tb2.available_tags == frozenset({"{?form last_name}"})


def test_radiobutton_looping_from_docs():
    rb1 = cop.elements.RadioButton(
        name="Radiolist",
        value="List A",
        text="List Option A",
        selected=True
    )
    rb2 = cop.elements.RadioButton(
        name="Radiolist",
        value="List B",
        text="List Option B",
        selected=True
    )
    assert rb1.as_dict == {
        "type": "radio",
        "name": "Radiolist",
        "value": "List A",
        "text": "List Option A",
        "selected": True
    }
    assert rb2.as_dict == {
        "type": "radio",
        "name": "Radiolist",
        "value": "List B",
        "text": "List Option B",
        "selected": True
    }
    assert rb1.available_tags == frozenset({"{?form Radiolist}"})
    assert rb2.available_tags == frozenset({"{?form Radiolist}"})


def test_radiobutton_reference_from_docs():
    rb_a = cop.elements.RadioButton(
        name="Radio",
        value="A",
        text="Option A",
        height=15,
        width=100
    )
    rb_b = cop.elements.RadioButton(
        name="Radio",
        value="B",
        text="Option B",
        height=15,
        width=100
    )
    assert rb_a.as_dict == {
        "type": "radio",
        "name": "Radio",
        "value": "A",
        "text": "Option A",
        "height": 15,
        "width": 100
    }
    assert rb_b.as_dict == {
        "type": "radio",
        "name": "Radio",
        "value": "B",
        "text": "Option B",
        "height": 15,
        "width": 100
    }
    assert rb_a.available_tags == frozenset({"{?form Radio}"})
    assert rb_b.available_tags == frozenset({"{?form Radio}"})


def test_checkbox_from_docs():
    cb = cop.elements.Checkbox(
        name="Checkbox",
        value=True,
        text="IsChecked",
        height=20,
        width=200
    )
    expected = {
        "type": "checkbox",
        "name": "Checkbox",
        "value": True,
        "text": "IsChecked",
        "height": 20,
        "width": 200
    }
    assert cb.as_dict == expected
    assert cb.available_tags == frozenset({"{?form Checkbox}"})



def test_dropdown_from_docs():
    dd = cop.elements.Dropdown(
        name="country",
        options=[
            {"value": "US", "label": "United States"},
            {"value": "BE", "label": "Belgium"},
            {"value": "NP", "label": "Nepal"},
        ],
        value="BE",
        height=20,
        width=200,
    )
    assert dd.as_dict == {
        "type": "dropdown",
        "name": "country",
        "options": [
            {"value": "US", "label": "United States"},
            {"value": "BE", "label": "Belgium"},
            {"value": "NP", "label": "Nepal"},
        ],
        "value": "BE",
        "height": 20,
        "width": 200,
    }
    assert dd.available_tags == frozenset({"{?form country}"})


def test_combobox_from_docs():
    cb = cop.elements.ComboBox(
        name="color",
        options=[{"value": "Red"}, {"value": "Green"}, {"value": "Blue"}],
        value="Magenta",
        height=20,
        width=200,
    )
    assert cb.as_dict == {
        "type": "combobox",
        "name": "color",
        "options": [{"value": "Red"}, {"value": "Green"}, {"value": "Blue"}],
        "value": "Magenta",
        "height": 20,
        "width": 200,
    }
    assert cb.available_tags == frozenset({"{?form color}"})


def test_listbox_from_docs():
    lb = cop.elements.ListBox(
        name="interests",
        options=[
            {"value": "music", "label": "Music"},
            {"value": "sports", "label": "Sports"},
            {"value": "coding", "label": "Coding"},
        ],
        values=["sports", "coding"],
        multi_select=True,
        height=80,
        width=200,
    )
    assert lb.as_dict == {
        "type": "listbox",
        "name": "interests",
        "options": [
            {"value": "music", "label": "Music"},
            {"value": "sports", "label": "Sports"},
            {"value": "coding", "label": "Coding"},
        ],
        "values": ["sports", "coding"],
        "multiSelect": True,
        "height": 80,
        "width": 200,
    }
    assert lb.available_tags == frozenset({"{?form interests}"})


def test_pushbutton_from_docs():
    pb = cop.elements.PushButton(name="submit", caption="Submit form", height=24, width=120)
    assert pb.as_dict == {
        "type": "pushbutton",
        "name": "submit",
        "caption": "Submit form",
        "height": 24,
        "width": 120,
    }
    assert pb.available_tags == frozenset({"{?form submit}"})


def test_password_from_docs():
    pw = cop.elements.Password(name="password", value="s3cret", height=20, width=200)
    assert pw.as_dict == {
        "type": "password",
        "name": "password",
        "value": "s3cret",
        "height": 20,
        "width": 200,
    }
    assert pw.available_tags == frozenset({"{?form password}"})


def test_form_group_in_collection():
    """In a collection, form elements wrap into {name: [field]} and same-name radios merge into one group."""
    collection = cop.elements.ElementCollection()
    collection.add(cop.elements.Textbox(name="first_name", value="John"))
    collection.add(cop.elements.RadioButton(name="radiolist", value="List A", text="Option A", selected=False))
    collection.add(cop.elements.RadioButton(name="radiolist", value="List B", text="Option B", selected=True))
    assert collection.as_dict == {
        "first_name": [{"type": "text", "name": "first_name", "value": "John"}],
        "radiolist": [
            {"type": "radio", "name": "radiolist", "value": "List A", "text": "Option A", "selected": False},
            {"type": "radio", "name": "radiolist", "value": "List B", "text": "Option B", "selected": True},
        ],
    }


def run():
    test_textbox_from_docs()
    test_radiobutton_looping_from_docs()
    test_radiobutton_reference_from_docs()
    test_checkbox_from_docs()
    test_dropdown_from_docs()
    test_combobox_from_docs()
    test_listbox_from_docs()
    test_pushbutton_from_docs()
    test_password_from_docs()
    test_form_group_in_collection()
    # print("tests p")

if __name__ == "__main__":
    run()
