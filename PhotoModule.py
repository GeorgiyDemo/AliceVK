import requests, uuid
from PIL import Image, ImageDraw, ImageFont

def getfile(url):
    thisfilename = str(uuid.uuid4()) + ".jpg"
    r = requests.get(url, stream=True)
    with open(thisfilename, 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)
    return thisfilename


def DrawText(img_path, ttf_path):
    im = Image.open(img_path)
    W, H = im.size
    draw = ImageDraw.Draw(im)
    txt = "KIP"
    fontsize = 100
    img_fraction = 0.85
    font = ImageFont.truetype(ttf_path, fontsize)
    while font.getsize(txt)[0] < img_fraction * im.size[0]:
        fontsize += 1
        font = ImageFont.truetype(ttf_path, fontsize)
    fontsize -= 1
    font = ImageFont.truetype(ttf_path, fontsize)

    draw.text((W / 10, H / 4), txt, font=font)
    im.save(img_path)
