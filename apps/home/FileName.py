

class FileName:

    def __init__(self, file_name):
        self.file_name = file_name
        self.structure = {}
        self.name_split()

    def name_split(self):
        # file name pattern: {type}_{size}_{origv}_{genv}.jpg
        # example: upl_o_1_1.jpg
        fl = self.file_name.split(".")
        el = fl[0].split("_")
        self.structure = {
            "type": el[0],
            "size": el[1],
            "fileno": el[2],
            "version": el[3]
        }

    def generate_names(self, versions):
        return versions

    def new_version(self, version_number):
        return "gen_o_" + self.structure["fileno"] + '_' + str(version_number) + ".jpg"

