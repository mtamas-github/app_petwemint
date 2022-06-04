import cv2
from .FileName import FileName


class GenerateArt:

    def __init__(self, img, directory):
        self.orig = img
        self.paints = {}
        self.fn = FileName(img)
        self._load_orig()

    def _load_orig(self):
        try:
            self.cv2 = cv2.imread(self.orig)
        except Exception as e:
            raise

    def oil_paint(self):

        self.paints["oil"] = {
            "img": cv2.xphoto.oilPainting(self.cv2, 7, 1)
        }

    def water_color(self):
        # sigma_s controls the size of the neighborhood. Range 1 - 200
        # sigma_r controls the how dissimilar colors within the neighborhood will be averaged.
        # A larger sigma_r results in large regions of constant color. Range 0 - 1
        self.paints["water"] = {
            "img": cv2.stylization(self.cv2, sigma_s=60, sigma_r=0.6)
        }

    def pencil_sketch(self):
        dst_gray, dst_color = cv2.pencilSketch(self.cv2, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        self.paints["pencil"] = {
            "img": dst_gray
        }

    def save(self):

        versions = self.fn.generate_names(self.paints)
        for t, img in versions.paints.items():
            path = img.get("path", None)
            img = img.get("img", None)
            if path is not None and img is not None:
                try:
                    cv2.imwrite(path, img)
                except IOError as e:
                    raise
