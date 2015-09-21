import requests
import os
import zipfile

# if odi.zip doesn't exist, download it
if not os.path.isfile('odis.zip'):
	print 'Downloading odis.zip from www.cricsheet.org...'
	ODI_URL = 'http://cricsheet.org/downloads/odis.zip'

	r = requests.get(ODI_URL, stream = True)

	with open('odis.zip', 'wb') as f:
		for chunk in r.iter_content(chunk_size = 1024):
			if chunk:
				f.write(chunk)
				f.flush()
	print "Created odis.zip"

# make folder for all the play-by-play 
if not os.path.exists('all_odis'):
	os.makedirs('all_odis')

# unzip odi.zip into a folder called odis
print 'Extracting ball-by-ball for all games'
with open('odis.zip', 'rb') as zf:
	z = zipfile.ZipFile(zf)
	for name in z.namelist():
		outfile = open('all_odis/{}'.format(name), 'wb')
		outfile.write(z.read(name))
		outfile.close()

print "Done"