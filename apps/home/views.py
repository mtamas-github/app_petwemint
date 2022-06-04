# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .forms import UploadFileForm
from .Gallery import Gallery
from .ImageSearch import ImageSearch


@login_required(login_url="/login/")
def index(request):

    g = Gallery(request)
    photos = g.get_uploaded_thumbnails()

    context = {'segment': 'index', 'photos': photos}
    html_template = loader.get_template('home/index3.html')
    return HttpResponse(html_template.render(context, request))


def images(request, id, image):
    img_path = settings.MEDIA_DIR + '/' + id + '/' + image
    image_data = open(img_path, "rb").read()
    return HttpResponse(image_data, content_type="image/jpeg")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def file_upload(request):

    if request.FILES:
        g = Gallery(request)
        g.upload_file()
    return HttpResponseRedirect('/')

def image_admin(request):

    ids = []
    post = request.POST
    if "search" in post:
        i_s = ImageSearch({"search": post["search"]})
        ids = i_s.search()
    elif "download" in post:
        i_s = ImageSearch(
            {
                "download": post["download"],
                "filename": post["filename"]
            })
        i_s.download()
    context = {'segment': 'index', 'ids': ids}
    html_template = loader.get_template('admin/image_admin.html')
    return HttpResponse(html_template.render(context, request))
