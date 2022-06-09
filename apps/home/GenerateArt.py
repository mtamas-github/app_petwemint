import cv2
import numpy as np
import logging
import datetime
from .FileName import FileName
from .NeuralStyleTransfer import NeuralStyle
from .Thumbnail import Thumbnail

logger = logging.getLogger(__name__)

VERSIONS = {
    1: "oil",
    2: "water",
    3: "pencil",
    4: "pencil_color",
    5: "cartoon",
    6: "sepia"
}

class GenerateArt:

    def __init__(self, img_name, directory):
        self.dir = directory
        self.orig = img_name
        self.paints = {}
        self.fn = FileName(img_name)
        self._load_orig()

    def _load_orig(self):
        try:
            #self.cv2 = io.imread(self.dir + '/' + self.orig)
            self.image_loaded = cv2.imread(self.dir + '/' + self.orig)
        except Exception as e:
            raise

    def filters(self):
        logger.info('image: ' + self.orig + ' transfer style: oil started at: ' + str(datetime.datetime.now()))
        self.oil_paint()
        logger.info('image: ' + self.orig + ' transfer style: water started at: ' + str(datetime.datetime.now()))
        self.water_color()
        logger.info('image: ' + self.orig + ' transfer style: pencil started at: ' + str(datetime.datetime.now()))
        self.pencil_sketch()
        logger.info('image: ' + self.orig + ' transfer style: cartoon started at: ' + str(datetime.datetime.now()))
        self.cartoon()
        logger.info('image: ' + self.orig + ' transfer style: sepia started at: ' + str(datetime.datetime.now()))
        self.sepia()
        self.save()

    def edge_mask(self, img, line_size, blur_value):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, blur_value)
        edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size,
                                      blur_value)
        return edges

    def color_quantization(self, img, k):
        # Transform the image
        data = np.float32(img).reshape((-1, 3))

        # Determine criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

        # Implementing K-Means
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result

    def neural_style(self):
        # generate all neural style transfer
        nst = NeuralStyle(self.dir)
        nst.generate_all(self.orig)

    def oil_paint(self):

        self.paints["oil"] = cv2.xphoto.oilPainting(self.image_loaded, 12, 1)

    def water_color(self):
        # sigma_s controls the size of the neighborhood. Range 1 - 200
        # sigma_r controls the how dissimilar colors within the neighborhood will be averaged.
        # A larger sigma_r results in large regions of constant color. Range 0 - 1
        self.paints["water"] = cv2.stylization(self.image_loaded, sigma_s=90, sigma_r=0.5)

    def pencil_sketch(self):
        #dst_gray, dst_color = cv2.pencilSketch(self.image_loaded, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
        dst_gray, dst_color = cv2.pencilSketch(self.image_loaded, sigma_s = 110, sigma_r = 0.9, shade_factor = 0.02)
        self.paints["pencil"] = dst_gray
        self.paints["pencil_color"] = dst_color

    def cartoon(self):
        line_size = 7
        blur_value = 7
        total_color = 9

        img = self.image_loaded

        edges = self.edge_mask(img, line_size, blur_value)

        img = self.color_quantization(img, total_color)
        blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
        self.paints["cartoon"] = cartoon

    def sepia(self):
        sepia = self.generate_sepia()
        self.paints["sepia"] = sepia

    def generate_sepia(self):
        img = self.image_loaded
        img_sepia = np.array(img, dtype=np.float64)  # converting to float to prevent loss
        img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                                        [0.349, 0.686, 0.168],
                                                        [0.393, 0.769,
                                                         0.189]]))  # multipying image with special sepia matrix
        img_sepia[np.where(img_sepia > 255)] = 255  # normalizing values greater than 255 to 255
        img_sepia = np.array(img_sepia, dtype=np.uint8)
        return img_sepia

    def save(self):

        for version, style in VERSIONS.items():
            version_file = self.fn.new_version(version)
            path = self.dir + '/' + version_file
            img = self.paints[style]
            if path is not None and img is not None:
                try:
                    cv2.imwrite(path, img)
                    print(version_file, self.dir)
                    th = Thumbnail(version_file, self.dir)
                    th.gen_thumbnail()
                except IOError as e:
                    raise
