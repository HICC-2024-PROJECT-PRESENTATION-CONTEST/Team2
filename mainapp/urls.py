"""
URL configuration for HICC_PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainapp import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 루트 URL (기본 페이지)
    path('translate/', views.translate, name='translate'),  # 번역 페이지
    path('summary/', views.summary, name='summary'),
    path('pdf-translate/', views.pdfTranslate, name='pdftranslate'),
]
