from django.contrib import admin
from django.urls import path, include
from mainapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('translate_text/', views.translate, name='translate_text'),
    path('summary/', views.summarize_text, name='summary'),  # 요약 요청을 처리할 URL
    path('define/', views.define_term, name='define_term'),
    path('ppt-translate/', views.pptTranslate, name='ppttranslate'),
]
