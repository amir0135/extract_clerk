import io
from PIL import Image
import pytesseract
from wand.image import Image as wi

def convert_scanfiles(file):
    pdf_file = wi(filename=file, resolution=300)
    images = pdf_file.convert('jpeg')

    image_blobs = [img.make_blob('jpeg') for img in images.sequence]

    extract = [pytesseract.image_to_string(Image.open(io.BytesIO(blob)), lang='eng') for blob in image_blobs]

    write_file = file.replace('.pdf', '.txt')
    with open(write_file, "w") as output:
        output.write('\n'.join(extract))
    return write_file
