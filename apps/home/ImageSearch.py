import requests
from urllib import request

from django.conf import settings

ART_IMAGE_API = "https://collectionapi.metmuseum.org/public/collection/v1/"
SEARCH_URL = "search"
IMAGE_DETAILS_URL = "objects/"
MAX_OBJECTS = 25

class ImageSearch:

    def __init__(self, request_data):
        self.request_data = request_data

    def search(self):
        search = self.request_data["search"]
        search_url = ART_IMAGE_API + SEARCH_URL + "?q=" +search
        data = self.call(search_url)
        if "objectIDs" in data:
            links = self.get_links(data["objectIDs"])
            return links
        else:
            return False

    def get_links(self, ids):
        links = []
        count = 1
        for id in ids:
            link = self.get_link(id)
            link["id"] = count
            if link:
                links.append(link)
                count = count + 1
                if count >= MAX_OBJECTS:
                    break
        return links

    def get_link(self, id):
        object_url = ART_IMAGE_API + IMAGE_DETAILS_URL + str(id)
        details = self.call(object_url)
        if "primaryImage" in details and "primaryImageSmall" in details:
            return {
                "small": details["primaryImageSmall"],
                "large": details["primaryImage"],
                "filename": details["primaryImage"].split("/")[-1]
            }
        else:
            return None

    def call(self, url):
        resp = requests.get(url=url)
        return resp.json()

    def download(self):
        download_url = self.request_data.get("download")
        download_file_name = self.request_data.get("filename")
        download_path = settings.STYLE_DIR + '/' + download_file_name

        if download_url and download_file_name:
            request.urlretrieve(download_url, download_path)



