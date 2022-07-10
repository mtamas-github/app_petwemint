# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - PetWeMint
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('save-pet', views.save_pet, name='save-pet'),

    path('gen_versions', views.gen_versions, name='gen_versions'),
    # path('buy/<pet>/<cert>', views.buy, name="buy"),

    path('media/<id>/<image>', views.images, name='images'),

    path('image_admin', views.image_admin, name='image_admin'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
