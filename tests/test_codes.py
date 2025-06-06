import cloudofficeprint as cop


def test_barcodes():
    """Test class BarCode, a subclass of class Code"""
    barcode = cop.elements.BarCode(
        name='name',
        data='data',
        type='ean13',
        height=50,
        width=50,
        errorcorrectlevel='L',
        url='url',
        rotation=45,
        background_color='red',
        padding_width=25,
        padding_height=25,
        extra_options='includetext guardwhitespace'
    )
    barcode_expected = {
        'name': 'data',
        'name_type': 'ean13',
        'name_height': 50,
        'name_width': 50,
        'name_errorcorrectlevel': 'L',
        'name_url': 'url',
        'name_rotation': 45,
        'name_background_color': 'red',
        'name_padding_width': 25,
        'name_padding_height': 25,
        'name_extra_options': 'includetext guardwhitespace'
    }
    assert barcode.as_dict == barcode_expected


def test_qr_code():
    """Test styling options for qr-code class"""
    qr = cop.elements.QRCode(
        name='name',
        data='data',
        type='qrcode'
    )

    qr.set_dotscale(0.5)
    qr.set_logo('logo')
    qr.set_background_image('background_image')
    qr.set_color_dark('color_dark')
    qr.set_color_light('color_light')
    qr.set_logo_width('logo_width')
    qr.set_logo_height('logo_height')
    qr.set_logo_background_color('logo_background_color')
    qr.set_quiet_zone(2)
    qr.set_quiet_zone_color('quiet_zone_color')
    qr.set_background_image_alpha(0.5)
    qr.set_po_color('po_color')
    qr.set_pi_color('pi_color')
    qr.set_po_tl_color('po_tl_color')
    qr.set_pi_tl_color('pi_tl_color')
    qr.set_po_tr_color('po_tr_color')
    qr.set_pi_tr_color('pi_tr_color')
    qr.set_po_bl_color('po_bl_color')
    qr.set_pi_bl_color('pi_bl_color')
    qr.set_timing_v_color('timing_v_color')
    qr.set_timing_h_color('timing_h_color')
    qr.set_timing_color('timing_color')
    qr.set_auto_color(False)
    qr.set_auto_color_dark('auto_color_dark')
    qr.set_auto_color_light('auto_color_light')

    qr_expected = {
        'name': 'data',
        'name_type': 'qrcode',
        'name_qr_dotscale': 0.5,
        'name_qr_logo': 'logo',
        'name_qr_background_image': 'background_image',
        'name_qr_color_dark': 'color_dark',
        'name_qr_color_light': 'color_light',
        'name_qr_logo_width': 'logo_width',
        'name_qr_logo_height': 'logo_height',
        'name_qr_logo_background_color': 'logo_background_color',
        'name_qr_quiet_zone': 2,
        'name_qr_quiet_zone_color': 'quiet_zone_color',
        'name_qr_background_image_alpha': 0.5,
        'name_qr_po_color': 'po_color',
        'name_qr_pi_color': 'pi_color',
        'name_qr_po_tl_color': 'po_tl_color',
        'name_qr_pi_tl_color': 'pi_tl_color',
        'name_qr_po_tr_color': 'po_tr_color',
        'name_qr_pi_tr_color': 'pi_tr_color',
        'name_qr_po_bl_color': 'po_bl_color',
        'name_qr_pi_bl_color': 'pi_bl_color',
        'name_qr_timing_v_color': 'timing_v_color',
        'name_qr_timing_h_color': 'timing_h_color',
        'name_qr_timing_color': 'timing_color',
        'name_qr_auto_color': False,
        'name_qr_auto_color_dark': 'auto_color_dark',
        'name_qr_auto_color_light': 'auto_color_light',
    }
    assert qr.as_dict == qr_expected


def test_qr_code_wifi():
    wifi = cop.elements.WiFiQRCode(
        name='name',
        ssid='ssid',
        wifi_encryption='WPA',
        wifi_password='password',
        wifi_hidden=False
    )
    wifi_expected = {
        'name': 'ssid',
        'name_type': 'qr_wifi',
        'name_wifi_password': 'password',
        'name_wifi_encryption': 'WPA',
        'name_wifi_hidden': False
    }
    assert wifi.as_dict == wifi_expected


def test_qr_code_telephone():
    telephone_number = cop.elements.TelephoneNumberQRCode(
        name='name',
        number='+32_test_number'
    )
    telephone_number_expected = {
        'name': '+32_test_number',
        'name_type': 'qr_telephone'
    }
    assert telephone_number.as_dict == telephone_number_expected


def test_qr_code_email():
    email = cop.elements.EmailQRCode(
        name='name',
        receiver='receiver',
        cc='cc',
        bcc='bcc',
        subject='subject',
        body='body'
    )
    email_expected = {
        'name': 'receiver',
        'name_type': 'qr_email',
        'name_email_cc': 'cc',
        'name_email_bcc': 'bcc',
        'name_email_subject': 'subject',
        'name_email_body': 'body'
    }
    assert email.as_dict == email_expected


def test_qr_code_sms():
    sms = cop.elements.SMSQRCode(
        name='name',
        receiver='receiver',
        sms_body='sms_body'
    )
    sms_expected = {
        'name': 'receiver',
        'name_type': 'qr_sms',
        'name_sms_body': 'sms_body'
    }
    assert sms.as_dict == sms_expected


def test_qr_code_url():
    url = cop.elements.URLQRCode(
        name='name',
        url='url'
    )
    url_expected = {
        'name': 'url',
        'name_type': 'qr_url'
    }
    assert url.as_dict == url_expected


def test_qr_code_v_card():
    v_card = cop.elements.VCardQRCode(
        name='name',
        first_name='first_name',
        last_name='last_name',
        email='email',
        website='website'
    )
    v_card_expected = {
        'name': 'first_name',
        'name_type': 'qr_vcard',
        'name_vcard_last_name': 'last_name',
        'name_vcard_email': 'email',
        'name_vcard_website': 'website'
    }
    assert v_card.as_dict == v_card_expected


def test_qr_code_me_card():
    me_card = cop.elements.MeCardQRCode(
        name='name',
        first_name='first_name',
        last_name='last_name',
        nickname='nickname',
        email='email',
        contact_primary='contact_primary',
        contact_secondary='contact_secondary',
        contact_tertiary='contact_tertiary',
        website='website',
        birthday='birthday',
        notes='notes'
    )
    me_card_expected = {
        'name': 'first_name',
        'name_type': 'qr_me_card',
        'name_me_card_last_name': 'last_name',
        'name_me_card_nickname': 'nickname',
        'name_me_card_email': 'email',
        'name_me_card_contact_primary': 'contact_primary',
        'name_me_card_contact_secondary': 'contact_secondary',
        'name_me_card_contact_tertiary': 'contact_tertiary',
        'name_me_card_website': 'website',
        'name_me_card_birthday': 'birthday',
        'name_me_card_notes': 'notes'
    }
    assert me_card.as_dict == me_card_expected


def test_qr_code_geolocation():
    geolocation = cop.elements.GeolocationQRCode(
        name='name',
        latitude='latitude',
        longitude='longitude',
        altitude='altitude'
    )
    geolocation_expected = {
        'name': 'latitude',
        'name_type': 'qr_geolocation',
        'name_geolocation_longitude': 'longitude',
        'name_geolocation_altitude': 'altitude'
    }
    assert geolocation.as_dict == geolocation_expected


def test_qr_code_event():
    event = cop.elements.EventQRCode(
        name='name',
        summary='summary',
        startdate='startdate',
        enddate='enddate'
    )
    event_expected = {
        'name': 'summary',
        'name_type': 'qr_event',
        'name_event_startdate': 'startdate',
        'name_event_enddate': 'enddate'
    }
    assert event.as_dict == event_expected


def run():
    test_barcodes()
    test_qr_code()
    test_qr_code_wifi()
    test_qr_code_telephone()
    test_qr_code_email()
    test_qr_code_sms()
    test_qr_code_url()
    test_qr_code_v_card()
    test_qr_code_me_card()
    test_qr_code_geolocation()
    test_qr_code_event()


if __name__ == '__main__':
    run()
