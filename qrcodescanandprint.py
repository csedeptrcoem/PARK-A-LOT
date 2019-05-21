
#from qrtools import QR
#myCode = QR(data=u"My sample text")
import pyqrcode
import qrtools
import pyzbar
#qr = pyqrcode.create("5")
#qr.png("emp5.png", scale=6)


from PIL import Image
from pyzbar.pyzbar import decode
data = decode(Image.open('emp5.png'))
print(data)
a=''.join(map(str,data))
b=a[15:16]
print(b)