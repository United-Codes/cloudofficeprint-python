import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
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
        "selected": 1
    }
    assert rb2.as_dict == {
        "type": "radio",
        "name": "Radiolist",
        "value": "List B",
        "text": "List Option B",
        "selected": 1
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
        "value": 1,
        "text": "IsChecked",
        "height": 20,
        "width": 200
    }
    assert cb.as_dict == expected
    assert cb.available_tags == frozenset({"{?form Checkbox}"})



def run():
    test_textbox_from_docs()
    test_radiobutton_looping_from_docs()
    test_radiobutton_reference_from_docs()
    test_checkbox_from_docs()
    # print("tests p")

if __name__ == "__main__":
    run()
