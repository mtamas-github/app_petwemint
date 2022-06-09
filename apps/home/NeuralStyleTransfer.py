import os
import logging
import datetime
from PIL import Image
from neuralstyletransfer.style_transfer import NeuralStyleTransfer
from .FileName import FileName
from .Thumbnail import Thumbnail

from django.conf import settings

CONTENT_WEIGHT = 100
STYLE_WEIGHT = 1
EPOCHS = 100
logger = logging.getLogger(__name__)
VERSION_OFFSET = 6  # this ist the offset as previouse styles already created

class NeuralStyle:

    def __init__(self, directory):
        self.style_dir = settings.STYLE_DIR
        self.dir = directory
        self.styles = []
        self.get_styles()

    def get_styles(self):

        if os.path.isdir(self.style_dir):
            for file in os.listdir(self.style_dir):
                self.styles.append(file)

    def generate_all(self, original):

        image_path = self.dir + '/' + original
        im = Image.open(image_path)
        exif = im.info['exif']
        fn = FileName(original)

        for key, style in enumerate(self.styles):
            print(key, style)

            logger.info('image: ' + original + ' neural style: ' + style + ' started at: ' + str(datetime.datetime.now()))
            version = key + VERSION_OFFSET
            nst = NeuralStyleTransfer()

            content_url = image_path
            style_url = self.style_dir + '/' + style
            nst.LoadContentImage(content_url, pathType='local')
            nst.LoadStyleImage(style_url, pathType='local')

            output = nst.apply(contentWeight=CONTENT_WEIGHT, styleWeight=STYLE_WEIGHT, epochs=EPOCHS)

            version_file_name = fn.new_version(version)
            version_file_path = self.dir + '/' + version_file_name

            output.save(version_file_path, exif=exif)
            th = Thumbnail(version_file_name, self.dir)
            th.gen_thumbnail()
            logger.info('image: ' + original + ' neural style: ' + style + ' finished at: ' + str(datetime.datetime.now()))
