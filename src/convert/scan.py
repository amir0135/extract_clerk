import io
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError

def convert_scanfiles(file):
    try:
        images = convert_from_path(file, 300)  # 300 is the resolution in DPI
        extract = [pytesseract.image_to_string(img, lang='eng') for img in images]
        
        write_file = file.replace('.pdf', '.txt')
        with open(write_file, "w") as output:
            output.write('\n'.join(extract))
        return write_file
    except (PDFPageCountError, PDFSyntaxError) as e:
        print(f"Error processing {file}: {e}")
        return None
