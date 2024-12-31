import sys
sys.path.insert(0, "D:/UC/cloudofficeprint-python")
import cloudofficeprint as cop


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
    
def test_html():
    """Test for Html property."""
    html_prop = cop.elements.Html(
        name='name',
        value='<!DOCTYPE html> <html> <body> <h2>An ordered HTML list</h2> <ol> <li value=\"2\">Coffee</li> <li>Tea</li> <li>Milk</li> </ol> </body> </html>',
        custom_table_style='CustomTableAOP',
        ordered_list_style='1',
        unordered_list_style='2',
        use_tag_style=False,
        ignore_cell_margin=True,
        ignore_empty_p=False,
    )
    html_prop_expected = {
        'name': '<!DOCTYPE html> <html> <body> <h2>An ordered HTML list</h2> <ol> <li value=\"2\">Coffee</li> <li>Tea</li> <li>Milk</li> </ol> </body> </html>',
        'name_custom_table_style': 'CustomTableAOP',
        'name_ordered_list_style': '1',
        'name_unordered_list_style': '2',
        'name_use_tag_style': False,
        'name_ignore_cell_margin': True,
        'name_ignore_empty_p': False
    }
    assert html_prop.as_dict == html_prop_expected


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

def test_cell_style_property_docx_preserve_width():
    style = cop.elements.CellStyleDocx(
        width=10,
        preserve_total_width_of_table='true'
    )
    style_property = cop.elements.CellStyleProperty(
        name='name',
        value='value',
        cell_style=style
    )
    style_property_expected = {
        'name': 'value',
        'name_width': 10,
        'name_preserve_total_width_of_table': 'true'
    }
    assert style_property.as_dict == style_property_expected
    
def test_cell_style_border_property_docx():
    style = cop.elements.CellStyleDocx(
        border='double',
        border_top_color='red',
        border_diagonal_down_size=38,
        border_bottom='thick',
        border_bottom_color='#ff0000',
        border_bottom_size='10',
        border_right='wave',
        border_right_space=5
    )
    style_property = cop.elements.CellStyleProperty(
        name='name',
        value='value',
        cell_style=style
    )
    style_property_expected = {
        'name': 'value',
        'name_border': 'double',
        'name_border_top_color': 'red',
        'name_border_diagonal_down_size': 38,
        'name_border_bottom': 'thick',
        'name_border_bottom_color': '#ff0000',
        'name_border_bottom_size': '10',
        'name_border_right': 'wave',
        'name_border_right_space': 5
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
        text_rotation=45,
        wrap_text=True,
        width='auto',
        height=40,
        max_characters=60,
        height_scaling=0.75
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
        'name_text_rotation': 45,
        'name_wrap_text': True,
        'name_width': 'auto',
        'name_height': 40,
        'name_max_characters': 60,
        'name_height_scaling': 0.75
    }
    assert style_property.as_dict == style_property_expected


def test_autoLink():
    autoLink = cop.elements.AutoLink(
        name='autoLink',
        value='sample text with hyperlinks',
        font_color='red',
        underline_color='#ffffffff',
        preserve_tag_style = True
    )
    autoLink_expected = {
        'autoLink': 'sample text with hyperlinks',
        'autoLink_font_color': 'red',
        'autoLink_underline_color': '#ffffffff',
        'autoLink_preserve_tag_style': True
        
    }
    assert autoLink.as_dict == autoLink_expected


def test_hyperlink():
    hyperlink = cop.elements.Hyperlink(
        name='hyperlink',
        url='url',
        text='hyperlink_text',
        font_color='red',
        underline_color='#ffffffff',
        preserve_tag_style = 'yes'
    )
    hyperlink_expected = {
        'hyperlink': 'url',
        'hyperlink_text': 'hyperlink_text',
        'hyperlink_text_font_color': 'red',
        'hyperlink_text_underline_color': '#ffffffff',
        'hyperlink_preserve_tag_style': 'yes'
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
        'freeze_element_name': "C10"
    }
    assert freezeElement.as_dict == freezeElement_expected

def test_protect_element():
    protectElement = cop.elements.SheetProtection('protect_tag_name', 'password', True, False, True,
                                           'YES', False, True, False, True, 'YES', 'other passord', True, False, True, 'YES')
    protectElementExpected = {
        "protect_tag_name": "password",
        "protect_tag_name_allow_auto_filter": True,
        "protect_tag_name_allow_delete_columns": False,
        "protect_tag_name_allow_delete_rows": True,
        "protect_tag_name_allow_format_cells": "YES",
        "protect_tag_name_allow_format_columns": False,
        "protect_tag_name_allow_format_rows": True,
        "protect_tag_name_allow_insert_columns": False,
        "protect_tag_name_allow_insert_hyperlinks": True,
        "protect_tag_name_allow_insert_rows": "YES",
        "protect_tag_name_password": "other passord",
        "protect_tag_name_allow_pivot_tables": True,
        "protect_tag_name_allow_select_locked_cells": False,
        "protect_tag_name_allow_select_unlocked_cells": True,
        "protect_tag_name_allow_sort": "YES"
    }
    assert protectElement.as_dict == protectElementExpected

def test_insert_element():
    insertElement = cop.elements.Insert("fileToInsert","base64EncodedValue")
    insertElement_expected = {
        "fileToInsert":"base64EncodedValue",
    }
    assert insertElement.as_dict == insertElement_expected

def test_remove_txt_box():
    remove = cop.elements.Remove('greetings', False)
    remove_expected = {
        "greetings":False
    }
    assert remove.as_dict == remove_expected
    
def test_hide_slide_pptx():
    remove = cop.elements.HideSlide('product', True)
    remove_expected = {
        "product_hide": True
    }
    # for debug
    # print("Actual output of remove.as_dict:", remove.as_dict)
    assert remove.as_dict == remove_expected
    
def test_distribute():
    remove = cop.elements.Distribute('product_b', True)
    remove_expected = {
        "product_b__distribute": True
    }
    assert remove.as_dict == remove_expected
    
def test_embed_element():
    embedElement = cop.elements.Embed("fileToEmbed","base64EncodedValue")
    embedElement_expected = {
        "fileToEmbed":"base64EncodedValue"
    }
    assert embedElement.as_dict == embedElement_expected

def test_excel_insert_element():
    insertExcelElement = cop.elements.ExcelInsert('fileToInsert',"base64EncodedFile","base64icon",None,3,'2px','3px',None,3,'2px','50px')
    insertExcelElement_expected = {
        "fileToInsert":"base64EncodedFile",
        "fileToInsert_icon":"base64icon",
        "fileToInsert_fromCol":3,
        "fileToInsert_fromRowOff":"2px",
        "fileToInsert_fromColOff":"3px",
        "fileToInsert_toCol":3,
        "fileToInsert_toRowOff":'2px',
        "fileToInsert_toColOff":"50px"
    }
    assert insertExcelElement.as_dict == insertExcelElement_expected
    
def test_cell_validation():
    cellValidate = cop.elements.ValidateCell("tagName",True,"whole","0","100",False,"between",True,"Instructions","Insert a number between 0 and 100",True,"warning","Error Occurred","Number Out of Bound")
    expectedCellValidation = {
        "tagName_ignore_blank" : True,
        "tagName_allow" : "whole",
        "tagName_value1" : "0",
        "tagName_value2" : "100",
        "tagName_in_cell_dropdown" : False,
        "tagName_data" : "between",
        "tagName_show_input_message" : True,
        "tagName_input_title" : "Instructions",
        "tagName_input_message" : "Insert a number between 0 and 100",
        "tagName_show_error_alert" : True,
        "tagName_error_style" : "warning",
        "tagName_error_title" : "Error Occurred",
        "tagName_error_message" : "Number Out of Bound"
    }
    assert cellValidate.as_dict == expectedCellValidation
    

def run():
    test_property()
    test_cell_style_property_docx()
    test_cell_style_property_docx_preserve_width()
    test_cell_style_border_property_docx()
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
    # test_protect_element()
    test_insert_element()
    # test_embed_element()
    # test_excel_insert_element()
    # test_cell_validation()
    test_remove_txt_box()
    test_hide_slide_pptx()
    # COP charts get tested in test_charts.py


if __name__ == '__main__':
    run()
