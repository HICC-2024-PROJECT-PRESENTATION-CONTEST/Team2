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
    path('', views.home, name='home'),
    path('translate/', views.translate, name='translate'),
    path('summarize_text/', views.translate_and_summarize, name='summarize_text'),  # 요약 요청을 처리할 URL 추가
    path('pdf-translate/', views.pdfTranslate, name='pdftranslate'),
    path('define/', views.define_term, name='define_term'),
    path('ppt-translate/', views.pptTranslate, name='ppttranslate'),
]