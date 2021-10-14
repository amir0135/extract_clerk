import io
from PIL import Image
import pytesseract
from wand.image import Image as wi

''''
This file takes a scanned file and converts it to a txt file.
Is pretty sensitive to dark parts in the scanned file
'''


def convert_scanfiles(file):
	pdfFile = wi(filename = file, resolution = 300)
	image = pdfFile.convert('jpeg')

	imageBlobs = []

	#save images for themselves
	for img in image.sequence:
		imgPage = wi(image = img)
		imageBlobs.append(imgPage.make_blob('jpeg'))

	#extract text out
	extract = []

	# for imgBlob in imageBlobs:
	for i in range(len(imageBlobs)):
		image = Image.open(io.BytesIO(imageBlobs[i]))
		text = pytesseract.image_to_string(image, lang = 'eng')
		extract.append(text)

	#write it to a txt file so we can load it in 'extract.py' and sort
	write_file = file.replace('.pdf','.txt')
	with open(write_file, "w") as output:
		for line in extract:
			output.write(line)
	return output


# convert_scanfiles('test_files/testnew.pdf')
# import time
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))