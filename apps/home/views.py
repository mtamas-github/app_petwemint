# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - PetWeMint
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from django.urls import reverse
from .forms import PetForm
from .Gallery import Gallery
from .ImageSearch import ImageSearch
from .models import Pet
from .forms import PetForm


@login_required(login_url="/login/")
def index(request):

    g = Gallery(request)
    photos = g.get_uploaded_thumbnails()
    pet_form = PetForm()
    pets = g.pets()
    certs = g.certs()

    context = {'segment': 'index', 'photos': photos, 'pet_form': pet_form, 'pets': pets, 'certs': certs}
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))


def images(request, id, image):
    img_path = settings.MEDIA_DIR + '/' + id + '/' + image
    image_data = open(img_path, "rb").read()
    return HttpResponse(image_data, content_type="image/jpeg")


def payment_success(request):
    # deal with nft
    pass


class CancelView(TemplateView):
    template_name = "cancel.html"

# @login_required(login_url="/login/")
# def buy(request, pet, cert):



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
def save_pet(request):

    post = request.POST
    file = request.FILES
    pf = PetForm(post, file)
    if pf.is_valid():
        g = Gallery(request)
        file_path = g.upload_file()
        pet = Pet()
        pet.name = pf.cleaned_data.get("name")
        pet.pet_type = pf.cleaned_data.get("type")
        pet.memorable = pf.cleaned_data.get("text_data")
        pet.image = file_path
        pet.user_id = request.user.id
        pet.save()
    else:
        print("form is invalid")

    return HttpResponseRedirect('/')


@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def gen_versions(request):

    post = request.POST
    if "image" in post:
        g = Gallery(request)
        g.generate_art(post["image"])
    return HttpResponseRedirect('/')

