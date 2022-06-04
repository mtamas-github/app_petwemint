# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path

class ImageAdmin(admin.AdminSite):
    def get_urls(self):
        urls = super(ImageAdmin, self).get_urls()
        my_urls = [
            path('image_admin/', self.image_admin),
        ]
        return my_urls + urls

    def image_admin(self, request):
        # ...
        context = dict(
           # Include common variables for rendering the admin template.
           self.each_context(request),
           # Anything else you want in the context...
           key="oifid",
        )
        return TemplateResponse(request, "admin/image_admin.html", context)