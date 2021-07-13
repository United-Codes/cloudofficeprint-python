import apexofficeprint as aop


def test_property():
    """Test for Property. Also serves as a test for Html, RightToLeft, FootNote, Raw, Formula, PageBreak and MarkdownContent."""
    prop = aop.elements.Property(
        name='name',
        value='value'
    )
    prop_expected = {
        'name': 'value'
    }
    assert prop.as_dict == prop_expected


def test_cell_style_property():
    style = aop.elements.CellStyle(
        background_color='red',
        width=10
    )
    style_property = aop.elements.CellStyleProperty(
        name='name',
        value='value',
        cell_style=style
    )
    style_property_expected = {
        'name': 'value',
        'name_background_color': 'red',
        'name_width': 10
    }
    assert style_property.as_dict == style_property_expected


def test_hyperlink():
    hyperlink = aop.elements.Hyperlink(
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
    toc = aop.elements.TableOfContents(
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
    span = aop.elements.Span(
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
    styled_prop = aop.elements.StyledProperty(
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
        'cust_first_name_highlight':'darkMagenta'
    }
    assert styled_prop.as_dict == styled_prop_expected


def test_watermark():
    watermark = aop.elements.Watermark(
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
    d3 = aop.elements.D3Code(
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
    tbox = aop.elements.TextBox(
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
    data = aop.elements.ElementCollection('data') # Name doesn't get used
    element1 = aop.elements.Image.from_url('image1', 'url')
    element1.alt_text = 'alt_text'
    data.add(element1)
    element2 = aop.elements.ForEach(
        name='loop',
        content=(aop.elements.Property('prop', 'value1'), aop.elements.Property('prop', 'value2'))
    )
    data.add(element2)
    data_expected = {
        'image1': 'url',
        'image1_alt_text': 'alt_text',
        'image1_url': 'url',
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

    collection = aop.elements.ElementCollection.element_to_element_collection(
        element=element1,
        name='test_name' # Doesn't get used
    )
    collection_expected = {
        'image1': 'url',
        'image1_alt_text': 'alt_text',
        'image1_url': 'url'
    }
    assert collection.as_dict == collection_expected


def run():
    test_property()
    test_cell_style_property()
    test_hyperlink()
    test_table_of_content()
    test_span()
    test_styled_property()
    test_watermark()
    test_d3_code()
    test_text_box()
    test_element_collection()
    # AOP charts get tested in test_charts.py


if __name__ == '__main__':
    run()