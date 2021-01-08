# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from app import scrape

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('user-management', views.user_management, name='user_management'),
    path('user-profile', views.user_profile, name='user_profile'),

    # scraping function
    path('scrape_data', scrape.scrape_data),

    # scraping function
    path('scrape_name', scrape.scrape_name),
    path('scrape_city', scrape.scrape_city),

    path('upload_photo', views.upload_photo),

    path('update_profile', views.update_profile),

    path('del_user', views.del_user),
    # Matches any html file
    re_path(r'csv_files/.*\.*', views.down, name='download'),
    # path('csv_files/^.*\.*', views.down, name='down')

]
