from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import fitz # PyMuPDF
from reportlab.pdfgen import canvas
from pptx import Presentation
from pptx.util import Inches
import openai
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt


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

        # PDF 파일을 읽기 위한 PyMuPDF 사용
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        translated_pdf = BytesIO()
        c = canvas.Canvas(translated_pdf)

        # 모든 페이지를 순회하여 번역 및 새로운 PDF 작성
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text()
            translated_text = translate_text(text)

            # Translate the text and write it to the new PDF
            c.drawString(72, 800, translated_text)  # 위치를 적절히 조정해야 할 수 있음
            c.showPage()

        c.save()
        translated_pdf.seek(0)

        # PDF를 클라이언트에 반환
        response = HttpResponse(translated_pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="translated.pdf"'
        return response

    return render(request, 'mainapp/pdftranslate.html')


def adjust_text_in_box(shape, translated_text):
    text_frame = shape.text_frame
    text_frame.clear()  # 기존 텍스트 삭제
    p = text_frame.add_paragraph()
    p.text = translated_text

    # 기본 폰트 크기와 스타일 설정
    if shape.text_frame.paragraphs and shape.text_frame.paragraphs[0].runs:
        first_run = shape.text_frame.paragraphs[0].runs[0]
        p.font.size = first_run.font.size or Pt(18)  # 기본 폰트 크기 설정
        p.font.bold = first_run.font.bold
        p.font.italic = first_run.font.italic
        p.alignment = shape.text_frame.paragraphs[0].alignment

    # 텍스트가 박스 안에 잘 맞지 않으면 글자 크기 줄이기
    while True:
        try:
            fit_result = text_frame.fit_text()
            if fit_result is None:
                break  # fit_text가 None을 반환하면 루프 종료

            # 텍스트가 잘 맞도록 조정
            if not fit_result and p.font.size and p.font.size.pt > 10:
                p.font.size = Pt(p.font.size.pt - 1)
            else:
                break  # 더 이상 줄일 수 없거나 텍스트가 맞으면 루프 종료

        except TypeError as e:
            print(f"TypeError encountered: {e}")
            break  # TypeError 발생 시 루프 종료

def pptTranslate(request):
    if request.method == 'POST' and request.FILES.get('ppt_file'):
        ppt_file = request.FILES['ppt_file']
        source_language = request.POST.get('source_language')
        target_language = request.POST.get('target_language')
        presentation = Presentation(ppt_file)
        translated_ppt = BytesIO()

        for slide in presentation.slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    original_text = shape.text.strip()
                    if original_text:
                        # 번역 함수에 선택된 언어를 전달
                        translated_text = translate_text(original_text, source_language, target_language)
                        adjust_text_in_box(shape, translated_text)
                    else:
                        # 텍스트가 없으면 텍스트 상자를 그대로 유지
                        pass

        presentation.save(translated_ppt)
        translated_ppt.seek(0)

        response = HttpResponse(translated_ppt,
                                content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        response['Content-Disposition'] = 'attachment; filename="translated.pptx"'
        return response

    return render(request, 'mainapp/ppttranslate.html')
