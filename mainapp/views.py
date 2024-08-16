import openai
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from io import BytesIO
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from pptx import Presentation

# OpenAI API 키 설정
openai.api_key = settings.OPENAI_API_KEY

def home(request):
    return render(request, 'mainapp/home.html')

def translate(request):
    if request.method == 'POST':
        source_language = request.POST.get('source_language')
        target_language = request.POST.get('target_language')
        text = request.POST.get('text')

        if not text:
            return JsonResponse({'translated_text': '텍스트가 비어 있습니다.'}, status=400)

        translated_text = translate_text(text, source_language, target_language)
        return JsonResponse({'translated_text': translated_text})
    return render(request, 'mainapp/translatesummary.html')

def translate_text(text, source_language, target_language):
    if not text.strip():
        return text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": f"You are a translation assistant that translates {source_language} text to {target_language}."},
                {"role": "user", "content": f"Translate the following text from {source_language} to {target_language}: {text}"}
            ],
            max_tokens=1024,
            temperature=0.5,
        )
        translated_text = response.choices[0].message['content'].strip()
        if not translated_text:
            return '번역 실패'
        return translated_text
    except Exception as e:
        print(f"Error: {e}")
        return '번역 실패'

def summarize_text(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if not text:
            return JsonResponse({'summary': '텍스트가 비어 있습니다.'}, status=400)

        summarized_text = get_summary(text)
        return JsonResponse({'summary': summarized_text})
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

def get_summary(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a summary assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text: {text}"}
            ],
            max_tokens=512,
            temperature=0.5,
        )
        summarized_text = response.choices[0].message['content'].strip()
        return summarized_text
    except Exception as e:
        print(f"Error: {e}")
        return '요약 실패'

def define_term(request):
    term = request.GET.get('term')
    if not term:
        return JsonResponse({'definition': '용어가 제공되지 않았습니다.'}, status=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an expert assistant that provides detailed definitions of technical terms in Korean."},
                {"role": "user", "content": f"Define the following term in Korean: {term}"}
            ],
            max_tokens=512,
            temperature=0.5,
        )
        definition = response.choices[0].message['content'].strip()
        return JsonResponse({'definition': definition})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'definition': '정의 실패'}, status=500)


def pdfTranslate(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']

        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        translated_pdf = BytesIO()
        c = canvas.Canvas(translated_pdf)

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            translated_text = translate_text(text, 'en', 'ko')

            c.drawString(72, 800, translated_text)
            c.showPage()

        c.save()
        translated_pdf.seek(0)

        response = HttpResponse(translated_pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="translated.pdf"'
        return response

    return render(request, 'mainapp/pdftranslate.html')

def pptTranslate(request):
    if request.method == 'POST' and request.FILES.get('ppt_file'):
        ppt_file = request.FILES['ppt_file']

        presentation = Presentation(ppt_file)
        translated_ppt = BytesIO()

        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    original_text = shape.text.strip()
                    if original_text:
                        translated_text = translate_text(original_text, 'en', 'ko')
                        shape.text = translated_text

        presentation.save(translated_ppt)
        translated_ppt.seek(0)

        response = HttpResponse(translated_ppt,
        content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        response['Content-Disposition'] = 'attachment; filename="translated.pptx"'
        return response

    return render(request, 'mainapp/ppttranslate.html')
