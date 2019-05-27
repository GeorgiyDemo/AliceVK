import requests, uuid

def getfile(url):
	thisfilename = str(uuid.uuid4())+".jpg"
	r = requests.get(url, stream=True)
	with open(thisfilename, 'wb') as fd:
		for chunk in r.iter_content(2000):
			fd.write(chunk)
	return thisfilename

def DrawText(path):
	im = Image.open(path)
	draw = ImageDraw.Draw(im)
