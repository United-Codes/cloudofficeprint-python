import cloudofficeprint as cop
import base64


def test_property():
    """Test for Property. Also serves as a test for Html, RightToLeft, FootNote, Raw, Formula, PageBreak and MarkdownContent."""
    prop = cop.elements.Property(
        name='name',
        value='value'
    )
    prop_expected = {
        'name': 'value'
    }
    assert prop.as_dict == prop_expected


def test_cell_style_property_docx():
    style = cop.elements.CellStyleDocx(
        cell_background_color='#eb4034',
        width=10
    )
    style_property = cop.elements.CellStyleProperty(
        name='name',
        value='value',
        cell_style=style
    )
    style_property_expected = {
        'name': 'value',
        'name_cell_background_color': '#eb4034',
        'name_width': 10
    }
    assert style_property.as_dict == style_property_expected


def test_cell_style_property_xlsx():
    style = cop.elements.CellStyleXlsx(
        cell_locked=True,
        cell_hidden=False,
        cell_background='#ff0000',
        font_name='Arial',
        font_size=12,
        font_color='#ff0000',
        font_italic=True,
        font_bold=False,
        font_strike=False,
        font_underline=True,
        font_superscript=False,
        font_subscript=True,
        border_top='medium',
        border_top_color='#ff0000',
        border_bottom='mediumDashed',
        border_bottom_color='#ff0000',
        border_left='mediumDashDot',
        border_left_color='#ff0000',
        border_right='mediumDashDotDot',
        border_right_color='#ff0000',
        border_diagonal='thick',
        border_diagonal_direction='up-wards',
        border_diagonal_color='#ff0000',
        text_h_alignment='center',
        text_v_alignment='justify',
        text_rotation=45
    )
    style_property = cop.elements.CellStyleProperty(
        name='name',
        value='value',
        cell_style=style
    )
    style_property_expected = {
        'name': 'value',
        'name_cell_locked': True,
        'name_cell_hidden': False,
        'name_cell_background': '#ff0000',
        'name_font_name': 'Arial',
        'name_font_size': 12,
        'name_font_color': '#ff0000',
        'name_font_italic': True,
        'name_font_bold': False,
        'name_font_strike': False,
        'name_font_underline': True,
        'name_font_superscript': False,
        'name_font_subscript': True,
        'name_border_top': 'medium',
        'name_border_top_color': '#ff0000',
        'name_border_bottom': 'mediumDashed',
        'name_border_bottom_color': '#ff0000',
        'name_border_left': 'mediumDashDot',
        'name_border_left_color': '#ff0000',
        'name_border_right': 'mediumDashDotDot',
        'name_border_right_color': '#ff0000',
        'name_border_diagonal': 'thick',
        'name_border_diagonal_direction': 'up-wards',
        'name_border_diagonal_color': '#ff0000',
        'name_text_h_alignment': 'center',
        'name_text_v_alignment': 'justify',
        'name_text_rotation': 45
    }
    assert style_property.as_dict == style_property_expected


def test_autoLink():
    autoLink = cop.elements.AutoLink(
        name='autoLink',
        value='sample text with hyperlinks',
    )
    autoLink_expected = {
        'autoLink': 'sample text with hyperlinks'
    }
    assert autoLink.as_dict == autoLink_expected


def test_hyperlink():
    hyperlink = cop.elements.Hyperlink(
        name='hyperlink',
        url='url',
        text='hyperlink_text'
    )
    hyperlink_expected = {
        'hyperlink': 'url',
        'hyperlink_text': 'hyperlink_text'
    }
    assert hyperlink.as_dict == hyperlink_expected


def test_table_of_content():
    toc = cop.elements.TableOfContents(
        name='table',
        title='contents',
        depth=4,
        tab_leader='underscore'
    )
    toc_expected = {
        'table_title': 'contents',
        'table_show_level': 4,
        'table_tab_leader': 'underscore'
    }
    assert toc.as_dict == toc_expected


def test_span():
    span = cop.elements.Span(
        name='span_name',
        value='This cell will span 2 rows and 3 columns',
        columns=3,
        rows=2
    )
    span_expected = {
        'span_name': 'This cell will span 2 rows and 3 columns',
        'span_name_col_span': 3,
        'span_name_row_span': 2
    }
    assert span.as_dict == span_expected


def test_styled_property():
    styled_prop = cop.elements.StyledProperty(
        name='cust_first_name',
        value='DemoCustomerName',
        font='NanumMyeongjo',
        font_size='25pt',
        font_color='#ff00ff',
        bold=True,
        italic=True,
        underline=False,
        strikethrough=False,
        highlight_color='darkMagenta'
    )
    styled_prop_expected = {
        'cust_first_name': 'DemoCustomerName',
        'cust_first_name_font_family': 'NanumMyeongjo',
        'cust_first_name_font_size': '25pt',
        'cust_first_name_font_color': '#ff00ff',
        'cust_first_name_bold': True,
        'cust_first_name_italic': True,
        'cust_first_name_underline': False,
        'cust_first_name_strikethrough': False,
        'cust_first_name_highlight': 'darkMagenta'
    }
    assert styled_prop.as_dict == styled_prop_expected


def test_watermark():
    watermark = cop.elements.Watermark(
        name='wm_name',
        text='wm_text',
        color='red',
        font='Arial',
        width=50,
        height=30,
        opacity=50,
        rotation=-45
    )
    watermark_expected = {
        'wm_name': 'wm_text',
        'wm_name_color': 'red',
        'wm_name_font': 'Arial',
        'wm_name_width': 50,
        'wm_name_height': 30,
        'wm_name_opacity': 50,
        'wm_name_rotation': -45
    }
    assert watermark.as_dict == watermark_expected


def test_d3_code():
    d3 = cop.elements.D3Code(
        name='d3_code',
        code='test_code',
        data=['a', 1, 2, 3, 'b']
    )
    d3_expected = {
        'd3_code': 'test_code',
        'd3_code_data': ['a', 1, 2, 3, 'b']
    }
    assert d3.as_dict == d3_expected


def test_text_box():
    tbox = cop.elements.TextBox(
        name='tbox_name',
        value='tbox_value',
        font='Arial',
        font_color='blue',
        font_size=12,
        transparency=50,
        width=30,
        height=25
    )
    tbox_expected = {
        'tbox_name': 'tbox_value',
        'tbox_name_font': 'Arial',
        'tbox_name_font_color': 'blue',
        'tbox_name_font_size': 12,
        'tbox_name_transparency': 50,
        'tbox_name_width': 30,
        'tbox_name_height': 25
    }
    assert tbox.as_dict == tbox_expected


def test_element_collection():
    data = cop.elements.ElementCollection('data')  # Name doesn't get used
    element1 = cop.elements.Image.from_url('image1', 'url_source')
    element1.alt_text = 'alt_text'
    data.add(element1)
    element2 = cop.elements.ForEach(
        name='loop',
        content=(cop.elements.Property('prop', 'value1'),
                 cop.elements.Property('prop', 'value2'))
    )
    data.add(element2)
    data_expected = {
        'image1': 'url_source',
        'image1_alt_text': 'alt_text',
        'loop': [
            {
                'prop': 'value1'
            },
            {
                'prop': 'value2'
            }
        ]
    }
    assert data.as_dict == data_expected

    data.remove_element_by_name('image1')

    data_expected = {
        'loop': [
            {
                'prop': 'value1'
            },
            {
                'prop': 'value2'
            }
        ]
    }

    assert data.as_dict == data_expected

    collection = cop.elements.ElementCollection.element_to_element_collection(
        element=element1,
        name='test_name'  # Doesn't get used
    )
    collection_expected = {
        'image1': 'url_source',
        'image1_alt_text': 'alt_text'
    }
    assert collection.as_dict == collection_expected

def test_freeze_element():
    freezeElement = cop.elements.Freeze(
        name='freeze_element_name',
        value="C10",
    )
    freezeElement_expected = {
        'freeze_element_name' : "C10"
    }
    assert freezeElement.as_dict == freezeElement_expected

def test_insert():
    insertElement1 = cop.elements.Insert(
        name='insert_element_name',
        value=cop.resource.Base64Resource("dummy base64 data", "docx")
    )
    insertElement_expected1 = {
        'insert_element_name' : "dummy base64 data"
    }
    assert insertElement1.as_dict == insertElement_expected1

    insertElement2 = cop.elements.Insert(
        name='insert_element_name',
        value=cop.resource.RawResource(bytes("dummy base64 data", "ascii"), "docx")
    )
    insertElement_expected2 = {
        'insert_element_name': "ZHVtbXkgYmFzZTY0IGRhdGE="
    }
    assert insertElement2.as_dict == insertElement_expected2

def run():
    test_property()
    test_cell_style_property_docx()
    test_cell_style_property_xlsx()
    test_autoLink()
    test_hyperlink()
    test_table_of_content()
    test_span()
    test_styled_property()
    test_watermark()
    test_d3_code()
    test_text_box()
    test_element_collection()
    test_freeze_element()
    test_insert()
    # COP charts get tested in test_charts.py


if __name__ == '__main__':
    run()
