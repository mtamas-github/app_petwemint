
from neuralstyletransfer.style_transfer import NeuralStyleTransfer

nst = NeuralStyleTransfer()

content_url = 'https://i.ibb.co/6mVpxGW/content.png'
style_url = 'https://i.ibb.co/30nz9Lc/style.jpg'
nst.LoadContentImage(content_url, pathType='url')
nst.LoadStyleImage(style_url, pathType='url')

output = nst.apply(contentWeight=1000, styleWeight=0.01, epochs=600)

from PIL import Image
output.save('output.jpg')