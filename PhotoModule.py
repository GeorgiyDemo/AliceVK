import requests, uuid
from PIL import Image, ImageDraw, ImageFont

def getfile(url):
	thisfilename = str(uuid.uuid4())+".jpg"
	r = requests.get(url, stream=True)
	with open(thisfilename, 'wb') as fd:
		for chunk in r.iter_content(2000):
			fd.write(chunk)
	return thisfilename

def DrawText(img_path, ttf_path):
	im = Image.open(img_path)
	W, H = im.size
	draw = ImageDraw.Draw(im)
	w, h = draw.textsize("KIP")
	draw.text(((W-w)/2,(H-h)/2), "KIP", font=ImageFont.truetype(ttf_path, 300))
	im.save(img_path)
