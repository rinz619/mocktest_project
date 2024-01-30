from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from website import views
app_name = 'website'

urlpatterns = [
    path('',views.index.as_view(),name='index'),
    ]