import qrcode
import sys
import os
import pyzbar.pyzbar
from PIL import Image

def decode_qr_code(codeImgPath):
    if not os.path.exists(codeImgPath):
        raise FileExistsError(codeImgPath)
    return pyzbar.pyzbar.decode(Image.open(codeImgPath))

ret = (decode_qr_code(i) for i in ("test.jpg", "test2.jpg", "test3.jpg"))
for r in ret:
    print(r)

sys.exit()