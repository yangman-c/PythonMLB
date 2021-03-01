from wand.image import Image
import sys

def convert_pdf_to_jpg(filename):
    img = Image(filename=filename, resolution=(520, 500))
    print('pages = ', len(img.sequence))
    converted = img.convert('jpg')
    converted.compression_quality = 25
    converted.save(filename='image/page.jpeg')

convert_pdf_to_jpg("ATIJ00ICTP20B005069L.pdf.PDF")

sys.exit()
