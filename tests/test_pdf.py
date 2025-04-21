import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
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


def test_cop_pdf_comments():
    """Test cop_pdf_comments element"""
    comment1_1 = cop.elements.PDFComment(
        text="First text to be shown in first page",
        x=50,
        y=50,
        page=1,
        bold=False,
        italic=True,
        font='Arial',
        font_color='blue',
        font_size=12
    )
    comment1_2 = cop.elements.PDFComment(
        text="Second text to be shown in first page",
        x=150,
        y=50,
        page=1,
        bold=False,
        italic=False,
        font='Arial',
        font_color='red',
        font_size=10
    )
    
    comment2 = cop.elements.PDFComment(
        text="First text to be shown in second page",
        x=50,
        y=50,
        page=2,
         bold=True,
        italic=True,
        font='Times new roman',
        font_color='#FF00FF',
        font_size=15
    )
    comment_all = cop.elements.PDFComment(
        text="Page Commenting here",
        x=0,
        y=0,
        bold=True,
        italic=False,
        font='Arial',
        font_color='red',
        font_size=20
    )
    pdf_comments = cop.elements.PDFComments(
        (comment1_1, comment1_2, comment2, comment_all)
    )

    pdf_comments_expected = {
        "AOP_PDF_COMMENTS": [
            {
                "1": [
                    {
                        "text": "First text to be shown in first page",
                        "x": 50,
                        "y": 50,
                        "bold": False,
                        "italic": True,
                        "font": "Arial",
                        "font_color": "blue",
                        "font_size": 12
                    },
                    {
                        "text": "Second text to be shown in first page",
                        "x": 150,
                        "y": 50,
                        "bold": False,
                        "italic": False,
                        "font": "Arial",
                        "font_color": "red",
                        "font_size": 10
                    }
                ],
                "2": [
                    {
                        "text": "First text to be shown in second page",
                        "x": 50,
                        "y": 50,
                        "bold": True,
                        "italic": True,
                        "font": "Times new roman",
                        "font_color": "#FF00FF",
                        "font_size": 15
                    }
                ],
                "all": [
                    {
                        "text": "Page Commenting here",
                        "x": 0,
                        "y": 0,
                        "bold": True,
                        "italic": False,
                        "font": "Arial",
                        "font_color": "red",
                        "font_size": 20
                    }
                ]
            }
        ]
    }

    assert pdf_comments.as_dict == pdf_comments_expected

def run():
    test_cop_pdf_texts()
    test_cop_pdf_images()
    test_cop_pdf_forms()
    test_cop_pdf_comments()

if __name__ == '__main__':
    run()
