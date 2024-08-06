import openai
from django.shortcuts import render

from HICC_PROJECT.settings import env

openai.api_key = env('openai.api_key')

def translate(request):
    return render(request, 'mainapp/translate.html')

def summary(request):
    return render(request, 'mainapp/summary.html')

def pdfTranslate(request):
    return render(request, 'mainapp/pdfTranslate.html')



