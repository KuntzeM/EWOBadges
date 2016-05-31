
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from kuntze.resource import resource_path

def createTextImage(text, font_name='arial', text_color=(0, 0, 0, 255), glow_color=(255, 255, 255, 128)):

    font = ImageFont.truetype(resource_path('misc/fonts/'+font_name + '.ttf'), 300)

    line_width, line_height = font.getsize(text)
    img = Image.new('RGBA', (line_width+100, line_height+100), (0, 0, 0, 0))
    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)

    x = (img_width/2.0)-(line_width/2.0)
    y = (img_height/2.0)-(line_height/2.0)
    j = 0
    for i in (5, 7, 10):
        tmp = Image.new('RGBA', (line_width+100, line_height+100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(tmp)
        draw.text((x-i, y), text, font=font, fill=glow_color)
        draw.text((x+i, y), text, font=font, fill=glow_color)
        draw.text((x, y-i), text, font=font, fill=glow_color)
        draw.text((x, y+i), text, font=font, fill=glow_color)

        if j > 0:
            tmp = tmp.filter(ImageFilter.GaussianBlur(j*3))
        img = Image.alpha_composite(img, tmp)
        j +=1

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(9)
    draw = ImageDraw.Draw(img)
    draw.text((x, y), text, font=font, fill=text_color)

    #img.save(save_name+'.png')

    return img