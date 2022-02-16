# Install cloudofficeprint using  pip install cloudofficeprint
import cloudofficeprint as cop #Import the cloudofficeprint libary.
# Main object that holds the data
collection = cop.elements.ElementCollection()

# -----------------barcode----------
barcode = cop.elements.BarCode(
        name='barcode_name',
        data='cloudofficeprint',
        type='code128',
        extra_options='includetext guardwhitespace'
    )
collection.add(barcode)

# --------------------------qrcode-----------
qrcode = cop.elements.QRCode(
        name='qrcode_name',
        data='https://www.cloudofficeprint.com/index.html',
        type='qrcode'
    )
# you can add multiple options for qrcode using variable_name.options
# for ex:
# if variable name is qrcode 
# qrcode.logo('background Image') 

collection.add(qrcode)

# ---------------------wifi_qr_code------------
wifi = cop.elements.WiFiQRCode(
        name='wifi_code_name',
        ssid='test_wifi_network',
        wifi_encryption='WPA',
        wifi_password='my_wifi_password',
        wifi_hidden=False
    )
collection.add(wifi)

# ----------------------telephone_qr_code---------
telephone_number = cop.elements.TelephoneNumberQRCode(
        name='telephone_number_name',
        number='9823038377'
    )
collection.add(telephone_number)

# --------------------email_qr_code-----------
email = cop.elements.EmailQRCode(
        name='email_name',
        receiver='info@cloudofficeprint.com',
        cc='cc',
        bcc='bcc',
        subject='test subject',
        body='Hi there,\n I would like to know about cloudofficeprint.\nThank you\n'
    )
collection.add(email)

#---------------sms_qr_code----------------
sms = cop.elements.SMSQRCode(
        name='sms_qr_code',
        receiver='9823038377',
        sms_body='this is test message body'
    )
collection.add(sms)

# --------------url_qr_code --------------
url = cop.elements.URLQRCode(
        name='urlQr_code',
        url='https://www.cloudofficeprint.com/index.html'
    )
collection.add(url)

# ---------------v_card_qrcode------------
v_card = cop.elements.VCardQRCode(
        name='vcard_name',
        first_name='first_name',
        last_name='last_name',
        email='email',
        website='website'
    )
collection.add(v_card)

# ---------------me_card-------------
me_card = cop.elements.MeCardQRCode(
        name='me_card_name',
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
collection.add(me_card)

# -----------------geo_location----------
geolocation = cop.elements.GeolocationQRCode(
        name='geolocatin_qr_code_name',
        latitude='27.608683',
        longitude='85.360287',
        altitude='1400'
    )
collection.add(geolocation)

# ---------------event----------------
event = cop.elements.EventQRCode(
        name='event_qr_code_name',
        summary='summary',
        startdate='startdate',
        enddate='enddate'
    )
collection.add(event)

# configure server
# For running on localhost you do not need api_key else replace below "YOUR_API_KEY" with your api key.
server = cop.config.Server(
    "http://localhost:8010/",
    cop.config.ServerConfig(api_key = "YOUR_API_KEY")
)
# Create print job
# PrintJob combines template, data, server and an optional output configuration
printjob = cop.PrintJob(
    data=collection,
    server=server,
    template=cop.Resource.from_local_file("./data/template.docx"),
)
# Execute print job and save response to file
response = printjob.execute()
response.to_file("output/output")