import os
from PIL import Image
from django.conf import settings

DEFAULT_THUMBNAIL_WIDTH = 150

class Thumbnail:

    def __init__(self,  image, directory):
        self.media_dir = directory
        self.orig = image
        self.orig_full_path = self._full_path(self.orig)

    def _full_path(self, img):
        return self.media_dir + '/' + img

    def th_name(self):
        return self.orig.replace("_o_", "_t_")

    def gen_thumbnail(self, width=None):
        # generate a thumbnail from an image
        if not width:
            width = int(DEFAULT_THUMBNAIL_WIDTH)
        img = Image.open(self.orig_full_path)
        print(img.info)
        if "exif" in img.info:
            exif = img.info['exif']
        else:
            exif = None
        w_percent = (width / img.size[0])
        hsize = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)
        th_full = self._full_path(
            self.th_name()
        )
        if exif:
            img.save(th_full, exif=exif)
        else:
            img.save(th_full)