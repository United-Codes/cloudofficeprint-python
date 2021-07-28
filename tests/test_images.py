import apexofficeprint as aop


def test_image_base64():
    image = aop.elements.ImageBase64(
        name='image1',
        base64str='base64str',
        max_width=50,
        max_height=45,
        alt_text='alt_text',
        wrap_text='wrap_text',
        rotation=45,
        transparency=50,
        url='url',
        width=30,
        height=25
    )
    image_expected = {
        'image1': 'base64str',
        'image1_max_width': 50,
        'image1_max_height': 45,
        'image1_alt_text': 'alt_text',
        'image1_wrap_text': 'wrap_text',
        'image1_rotation': 45,
        'image1_transparency': 50,
        'image1_url': 'url',
        'image1_width': 30,
        'image1_height': 25
    }
    assert image.as_dict == image_expected


def test_image_url():
    image = aop.elements.ImageUrl(
        name='image1',
        url_source='url_source',
        max_width=50,
        max_height=45,
        alt_text='alt_text',
        wrap_text='wrap_text',
        rotation=45,
        transparency=50,
        url='url',
        width=30,
        height=25
    )
    image_expected = {
        'image1': 'url_source',
        'image1_max_width': 50,
        'image1_max_height': 45,
        'image1_alt_text': 'alt_text',
        'image1_wrap_text': 'wrap_text',
        'image1_rotation': 45,
        'image1_transparency': 50,
        'image1_url': 'url',
        'image1_width': 30,
        'image1_height': 25
    }
    assert image.as_dict == image_expected


def run():
    test_image_base64()
    test_image_url()


if __name__ == '__main__':
    run()