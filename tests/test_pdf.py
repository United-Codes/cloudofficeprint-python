import cloudofficeprint as cop


def test_cop_pdf_texts():
    """Test cop_pdf_texts element"""
    pdf_text1_1 = cop.elements.PDFText(
        text='test1_1',
        x=50,
        y=60,
        page=3,
        rotation=45,
        bold=False,
        italic=True,
        font='Arial',
        font_color='blue',
        font_size=12
    )
    pdf_text1_2 = cop.elements.PDFText(
        text='test1_2',
        x=20,
        y=30,
        page=3,
        rotation=45,
        bold=False,
        italic=False,
        font='Arial',
        font_color='red',
        font_size=10
    )
    pdf_text2 = cop.elements.PDFText(
        text='test2',
        x=60,
        y=70,
        page=5,
        rotation=30,
        bold=True,
        italic=True,
        font='Times new roman',
        font_color='#FF00FF',
        font_size=15
    )
    pdf_text_all = cop.elements.PDFText(
        text='test_all',
        x=20,
        y=30,
        rotation=15,
        bold=True,
        italic=False,
        font='Arial',
        font_color='red',
        font_size=20
    )
    pdf_texts = cop.elements.PDFTexts(
        (pdf_text1_1, pdf_text1_2, pdf_text2, pdf_text_all))
    pdf_texts_expected = {
        'AOP_PDF_TEXTS': [
            {
                '3': [
                    {
                        'text': 'test1_1',
                        'x': 50,
                        'y': 60,
                        'rotation': 45,
                        'bold': False,
                        'italic': True,
                        'font': 'Arial',
                        'font_color': 'blue',
                        'font_size': 12
                    },
                    {
                        'text': 'test1_2',
                        'x': 20,
                        'y': 30,
                        'rotation': 45,
                        'bold': False,
                        'italic': False,
                        'font': 'Arial',
                        'font_color': 'red',
                        'font_size': 10
                    }
                ],
                '5': [
                    {
                        'text': 'test2',
                        'x': 60,
                        'y': 70,
                        'rotation': 30,
                        'bold': True,
                        'italic': True,
                        'font': 'Times new roman',
                        'font_color': '#FF00FF',
                        'font_size': 15
                    }
                ],
                'all': [
                    {
                        'text': 'test_all',
                        'x': 20,
                        'y': 30,
                        'rotation': 15,
                        'bold': True,
                        'italic': False,
                        'font': 'Arial',
                        'font_color': 'red',
                        'font_size': 20
                    }
                ]
            }
        ]
    }
    assert pdf_texts.as_dict == pdf_texts_expected


def test_cop_pdf_images():
    """Test cop_pdf_images element"""
    pdf_image1_1 = cop.elements.PDFImage(
        image='test1_1',
        x=50,
        y=60,
        page=3,
        rotation=45,
        width=50,
        height=50,
        max_width=100
    )
    pdf_image1_2 = cop.elements.PDFImage(
        image='test1_2',
        x=60,
        y=70,
        page=3,
        rotation=30,
        width=75,
        height=75,
        max_width=75
    )
    pdf_image2 = cop.elements.PDFImage(
        image='test2',
        x=20,
        y=30,
        page=5,
        rotation=15,
        width=100,
        height=100,
        max_width=100
    )
    pdf_image_all = cop.elements.PDFImage(
        image='test_all',
        x=25,
        y=26,
        rotation=45,
        width=20,
        height=20,
        max_width=50
    )
    pdf_images = cop.elements.PDFImages(
        (pdf_image1_1, pdf_image1_2, pdf_image2, pdf_image_all))
    pdf_images_expected = {
        'AOP_PDF_IMAGES': [
            {
                '3': [
                    {
                        'image': 'test1_1',
                        'x': 50,
                        'y': 60,
                        'rotation': 45,
                        'image_width': 50,
                        'image_height': 50,
                        'image_max_width': 100
                    },
                    {
                        'image': 'test1_2',
                        'x': 60,
                        'y': 70,
                        'rotation': 30,
                        'image_width': 75,
                        'image_height': 75,
                        'image_max_width': 75
                    }
                ],
                '5': [
                    {
                        'image': 'test2',
                        'x': 20,
                        'y': 30,
                        'rotation': 15,
                        'image_width': 100,
                        'image_height': 100,
                        'image_max_width': 100
                    },
                ],
                'all': [
                    {
                        'image': 'test_all',
                        'x': 25,
                        'y': 26,
                        'rotation': 45,
                        'image_width': 20,
                        'image_height': 20,
                        'image_max_width': 50
                    }
                ]
            }
        ]
    }
    assert pdf_images.as_dict == pdf_images_expected


def test_cop_pdf_forms():
    """Test cop_pdf_forms element"""
    form = cop.elements.PDFFormData(
        {
            'f_1': 5,
            'f_2': 'test',
            'r_1': True,
            'r_2': False
        }
    )
    form_expected = {
        'aop_pdf_form_data': {
            'f_1': 5,
            'f_2': 'test',
            'r_1': True,
            'r_2': False
        }
    }
    assert form.as_dict == form_expected


def test_pdf_form_text_box():
    text_box = cop.elements.PDFFormTextBox(
        name="surname",
        value="Apex R&D",
        width=100,
        height=20,
    )
    text_box_expected = {
        "surname": {
            "type": "text",
            "value": "Apex R&D",
            "name": "surname",
            "height": 20,
            "width": 100
        }
    }
    assert text_box.as_dict == text_box_expected


def test_pdf_form_check_box():
    check_box = cop.elements.PDFFormCheckBox(
        name="Checkbox",
        check=True,
        text="Check?",
        width=200,
        height=20,
    )
    check_box_expected = {
        "Checkbox": {
            "type": "checkbox",
            "name": "Checkbox",
            "value": True,
            "height": 20,
            "width": 200,
            "text": "Check?"
        }
    }
    assert check_box.as_dict == check_box_expected


def test_pdf_form_radio_button():
    radio_button = cop.elements.PDFFormRadioButton(
        name="a",
        group="Radio",
        value="A",
        text="Option A",
        selected=True,
        width=200,
        height=20,
    )
    radio_button_expected = {
        "a": {
            "type": "radio",
            "name": "Radio",
            "value": "A",
            "height": 20,
            "width": 200,
            "text": "Option A",
            "selected": True
        }
    }
    assert radio_button.as_dict == radio_button_expected


def test_pdf_form_signature():
    signature = cop.elements.PDFFormSignature(
        name="text1",
        width=150,
        height=50,
    )
    signature_expected = {
        "text1": {
            "type": "signaturefieldunsigned",
            "name": "text1",
            "width": 150,
            "height": 50
        }
    }
    assert signature.as_dict == signature_expected


def test_pdf_form_signature_signed():
    signature = cop.elements.PDFFormSignatureSigned(
        name="text2",
        value="base64 encoded certificate",
        password="certificate password",
        size="md",
        background_image="base64 encoded image",
        width=200,
        height=50,
    )
    signature_expected = {
        "text2": {
            "type": "signaturefieldsigned",
            "name": "text2",
            "size": "md",
            "value": "base64 encoded certificate",
            "background_image": "base64 encoded image",
            "password": "certificate password",
            "width": 200,
            "height": 50
        }
    }
    assert signature.as_dict == signature_expected


def run():
    test_cop_pdf_texts()
    test_cop_pdf_images()
    test_cop_pdf_forms()
    test_pdf_form_text_box()
    test_pdf_form_check_box()
    test_pdf_form_radio_button()
    test_pdf_form_signature()
    test_pdf_form_signature_signed()


if __name__ == '__main__':
    run()
