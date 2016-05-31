from PIL import Image
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from kuntze.createTextImage import createTextImage


def oneBadge(c, background_path, name_text, left_text, right_text, badge_width=9*cm, badge_height=6*cm, font_name='arial'):

    font_size = 60
    offset = (0, 0)
    left_logo = createTextImage(left_text, font_name=font_name)
    right_logo = createTextImage(right_text, font_name=font_name)

    background_image = Image.open(background_path, 'r')
    if badge_width is None:
        badge_width = background_image.size[0]
    if badge_height is None:
        aspect_ratio = background_image.size[1]/background_image.size[0]
        badge_height = badge_width*aspect_ratio

    c.drawImage(background_path, offset[0], offset[1], width=badge_width, height=badge_height)# preserveAspectRatio=True)

    text_width = stringWidth(name_text, font_name, font_size)

    while text_width > 0.8*badge_width:
        font_size -= 5
        text_width = stringWidth(name_text, font_name, font_size)

    c.setFont(font_name, font_size)
    c.drawCentredString(offset[0]+(badge_width/2), offset[1]+0.8*(badge_height/2), name_text)

    tmp_width, tmp_height = left_logo.size
    aspect = tmp_width/tmp_height
    tmp_height = 0.2*badge_height
    tmp_width = 1.5*aspect*tmp_height
    c.drawImage(ImageReader(left_logo), offset[0]+0.13*badge_width, offset[1]+badge_height-tmp_height, height=tmp_height, width=tmp_width, mask='auto')

    tmp_width, tmp_height = right_logo.size
    aspect = tmp_width/tmp_height
    tmp_height = 0.2*badge_height
    tmp_width = 1.5*aspect*tmp_height
    c.drawImage(ImageReader(right_logo), badge_width - tmp_width, offset[1]+badge_height-tmp_height, height=tmp_height, width=tmp_width, mask='auto')

    c.showPage()