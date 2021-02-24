import qrcode
import os
import pyzbar.pyzbar
from PIL import Image

def decode_qr_code(codeImgPath):
    if not os.path.exists(codeImgPath):
        raise FileExistsError(codeImgPath)
    return pyzbar.pyzbar.decode(Image.open(codeImgPath))

ret = decode_qr_code("name.jpg")
print(ret)