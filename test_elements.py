import apexofficeprint as aop
import pprint


def test_property():
    """Test for Property. Also serves as a test for Html, RightToLeft, FootNote, Raw and Formula."""
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


def run():
    test_property()
    test_cell_style_property()
    test_hyperlink()
    test_table_of_content()
    test_span()
    test_styled_property()



if __name__ == '__main__':
    run()