import os
from PIL import Image

DEFAULT_THUMBNAIL_WIDTH = 150

class Thumbnail:

    def __init__(self, media_dir, image):
        if os.path.isdir(media_dir):
            self.media_dir = media_dir
        else:
            raise Exception(f"Directory does not exist:{media_dir}")

        self.orig = image
        self.orig_full_path = self._full_path(self.orig)

    def _full_path(self, img):
        return self.media_dir + '/' + img

    def gen_thumbnail(self, th_img, width=DEFAULT_THUMBNAIL_WIDTH):
        # generate a thumbnail from an image
        th_full = self._full_path(th_img)
        img = Image.open(self.orig_full_path)
        w_percent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)
        img.save(th_full)
