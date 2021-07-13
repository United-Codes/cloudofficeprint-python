import apexofficeprint as aop

def test_aop_pdf_texts():
    """Test aop_pdf_texts element"""
    pdf_text1_1 = aop.elements.PDFText(
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
    pdf_text1_2 = aop.elements.PDFText(
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
    pdf_text2 = aop.elements.PDFText(
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
    pdf_text_all = aop.elements.PDFText(
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
    pdf_texts = aop.elements.PDFTexts((pdf_text1_1, pdf_text1_2, pdf_text2, pdf_text_all))
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

def test_aop_pdf_images():
    """Test aop_pdf_images element"""
    pdf_image1_1 = aop.elements.PDFImage(
        image='test1_1',
        x=50,
        y=60,
        page=3,
        rotation=45,
        width=50,
        height=50,
        max_width=100
    )
    pdf_image1_2 = aop.elements.PDFImage(
        image='test1_2',
        x=60,
        y=70,
        page=3,
        rotation=30,
        width=75,
        height=75,
        max_width=75
    )
    pdf_image2 = aop.elements.PDFImage(
        image='test2',
        x=20,
        y=30,
        page=5,
        rotation=15,
        width=100,
        height=100,
        max_width=100
    )
    pdf_image_all = aop.elements.PDFImage(
        image='test_all',
        x=25,
        y=26,
        rotation=45,
        width=20,
        height=20,
        max_width=50
    )
    pdf_images = aop.elements.PDFImages((pdf_image1_1, pdf_image1_2, pdf_image2, pdf_image_all))
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


def test_aop_pdf_forms():
    """Test aop_pdf_forms element"""
    form = aop.elements.PDFFormData(
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


def run():
    test_aop_pdf_texts()
    test_aop_pdf_images()
    test_aop_pdf_forms()


if __name__ == '__main__':
    run()