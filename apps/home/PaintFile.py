from os.path import dirname, abspath, isdir, join
import random
import string

DEFAULT_IMAGE_DIR = join(dirname(dirname(abspath(__file__))), "images")


class PaintFile:

    def __init__(self, paints, orig):
        """
        Generate file names
        :param paints: dict
        """
        self.paints = paints
        self._naming()

    def _naming(self):
        for t, paint in self.paints.items():
            self.paints[t]["path"] = f"{DEFAULT_IMAGE_DIR}/{t}_{self._rand_name()}.png"

    @staticmethod
    def _rand_name():
        all_chars = string.ascii_letters + string.digits
        return ''.join(random.choices(all_chars, k=14))