import os
from django.conf import settings
from PIL import Image

DEFAULT_THUMBNAIL_WIDTH = 150

# gallery directory: media
# each user has a directory inside media. The name of directory is the user_id like: media/12
# file name patterns:
# original uploaded files:
# upl_o_1.jpg
# first 3 characters: type
#     which can be: upl, gen or nft
# fifth character is size where o is the original size, t is the thumbnail size
# first number is the number of original uploaded file
# second number is the generated file version number
# example:
#   upl_o_1_1.jpg  - original file
#   upl_t_1_1.jpg  - thumbnail of original file
#   gen_o_1_1.jpg  - first generated art for the first uploaded file normal size
#   gen_t_1_1.jpg  - first generated art for the first uploaded file thumbnail size
#   gen_o_1_2.jpg  - second generated art for the first uploaded file normal size
#   gen_t_1_2.jpg  - second generated art for the first uploaded file thumbnail size

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
        wpercent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)
        img.save(th_full)


class Gallery:

    def __init__(self, request):
        self.id = request.user.id
        self.files_uploads = request.FILES
        self.upload_dir = settings.MEDIA_DIR + "/" + str(self.id)
        self.upload_link = settings.MEDIA_LINK + "/" + str(self.id)
        self.images = {}
        self._load_dir()

    def _load_dir(self):
        # read the directory and load file names in a dictionary by file types
        imgs = {
            "upl": {},
            "gen": {},
            "nft": {}
        }
        if os.path.isdir(self.upload_dir):
            for file in os.listdir(self.upload_dir):
                fl = file.split(".")
                el = fl[0].split("_")
                file_type = el[0]
                i_or_t = el[1]
                orig_version = el[2]
                gen_version = el[3]
                if i_or_t not in imgs[file_type]:
                    imgs[file_type][i_or_t] = {}
                if orig_version not in imgs[file_type][i_or_t]:
                    imgs[file_type][i_or_t][orig_version] = {}
                imgs[file_type][i_or_t][orig_version][gen_version] = file

        self.images = imgs

    def get_uploaded_thumbnails(self):
        thumbs = []
        ts = self.images["upl"].get("t")
        if ts:
            for i_id in ts:
                for l_i in ts[i_id]:
                    thumbs.append(self.upload_link + '/' + ts[i_id][l_i])
        return thumbs

    def _next_id(self):
        # calculate the next available file id for upload name
        upl = self.images.get("upl", None)
        max_digit = 0
        if upl:
            o = upl.get("o", None)
            if o:
                for key, value in o.items():
                    digit = int(key)
                    if digit > max_digit:
                        max_digit = digit
        max_digit = max_digit + 1
        return str(max_digit)

    def _upload_file_name(self, v_id):
        if not os.path.isdir(self.upload_dir):
            os.makedirs(self.upload_dir, exist_ok=True)
        return 'upl_o_' + v_id + '_' + v_id + '.jpg'

    @staticmethod
    def _th_file_name(file_name):
        # create thumbnail filename from uploaded filename
        return file_name.replace("_o_", "_t_")

    def generate_thumbnail(self, img):
        t = Thumbnail(self.upload_dir, img)
        t.gen_thumbnail(self._th_file_name(img))

    def upload_file(self):
        # get the uploaded file from the post request data
        # save it in the directory
        # then generate thumbnail
        f = self.files_uploads.get("photo_upload", None)
        if f:
            next_id = self._next_id()
            new_file_name = self._upload_file_name(next_id)
            with open(self.upload_dir + '/' + new_file_name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
            self.generate_thumbnail(new_file_name)
