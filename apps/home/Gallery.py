import os
import json
from django.conf import settings
# from .GenerateArt import GenerateArt
from .FileName import FileName
from .Thumbnail import Thumbnail
from .models import Pet, NFTPrepared


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
                fn = FileName(file)
                size = fn.structure["size"]
                type = fn.structure["type"]
                fileno = fn.structure["fileno"]
                version = fn.structure["version"]
                if size not in imgs[type]:
                    imgs[type][size] = {}
                if fileno not in imgs[type][size]:
                    imgs[type][size][fileno] = {}
                imgs[type][size][fileno][version] = file

        self.images = imgs

    def get_uploaded_thumbnails(self):
        thumbs = []
        ts = self.images["upl"].get("t")
        if ts:
            for i_id in ts:
                for l_i in ts[i_id]:
                    thumbs.append(
                        {'src': self.upload_link + '/' + ts[i_id][l_i],
                        'name': ts[i_id][l_i],
                        'orig': ts[i_id][l_i].replace("_t_", "_o_")
                        }
                    )
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
        t = Thumbnail(img, self.upload_dir)
        t.gen_thumbnail()

    def generate_art(self, image):
        # gen = GenerateArt(image, self.upload_dir)
        # gen.filters()
        # gen.neural_style()
        pass

    def pets(self):
        pets = []
        db_pets = Pet.objects.filter(user_id=self.id).values()
        for pet in Pet.objects.filter(user_id=self.id).values():
            print(pet)
            pets.append(
                {'id': pet["id"],
                 'name': pet["name"],
                 'image': pet["image"],
                 'text': pet["text_data"],
                 'thumbnail_url': self.thumbnail_url(pet["image"])
                 }
            )
        print(pets)
        return pets

    def thumbnail_url(self, name):
        print(name)
        th = Thumbnail(name, settings.MEDIA_LINK + "/" + str(self.id))
        return th.th_name()

    def certs(self):
        certs = []
        for cert in NFTPrepared.objects.filter(user_id=self.id):
            certs.append(
                {'name': cert["name"],
                 'image': cert["image"],
                 'text': cert["text_data"]}
            )
        return certs

    def upload_file(self):
        # get the uploaded file from the post request data
        # save it in the directory
        # then generate thumbnail
        f = self.files_uploads.get("image", None)
        if f:
            next_id = self._next_id()
            new_file_name = self._upload_file_name(next_id)
            with open(self.upload_dir + '/' + new_file_name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
            self.generate_thumbnail(new_file_name)
            return self.upload_link + '/' + new_file_name
        else:
            return None
