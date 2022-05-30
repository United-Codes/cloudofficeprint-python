import cloudofficeprint as cop


def test_image():
    image = cop.elements.Image(
        name='image1',
        source='url_source',
        max_width=50,
        max_height=45,
        alt_text='alt_text',
        wrap_text='wrap_text',
        rotation=45,
        transparency=50,
        url='url',
        width=30,
        height=25,
        maintain_aspect_ratio=True,
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
        'image1_height': 25,
        'image1_maintain_aspect_ratio': True
    }
    assert image.as_dict == image_expected


def run():
    test_image()


if __name__ == '__main__':
    run()
