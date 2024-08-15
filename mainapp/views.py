from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from pptx import Presentation
from pptx.util import Inches
import openai
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO

# OpenAI API 키 설정
openai.api_key = settings.OPENAI_API_KEY

def home(request):
    return render(request, 'mainapp/home.html')

def translate(request):
    if request.method == 'POST':
        english_text = request.POST.get('english_text')
        if not english_text:
            return JsonResponse({'translated_text': '텍스트가 비어 있습니다.'}, status=400)

        translated_text = translate_text(english_text)
        return JsonResponse({'translated_text': translated_text})
    return render(request, 'mainapp/translatesummary.html')

def translate_text(text):
    if not text.strip():
        return text  # 빈 텍스트는 번역하지 않고 그대로 반환

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a translation assistant that translates English text to Korean."},
                {"role": "user", "content": f"Translate the following text to Korean: {text}"}
            ],
            max_tokens=1024,
            temperature=0.5,
        )
        translated_text = response.choices[0].message['content'].strip()
        if not translated_text:
            return '번역 실패'  # 번역 결과가 빈 문자열일 경우
        return translated_text
    except Exception as e:
        print(f"Error: {e}")  # 에러를 로그에 출력
        return '번역 실패'


def summarize_text(korean_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a summary assistant that summarizes Korean text."},
                {"role": "user", "content": f"Summarize the following text in Korean: {korean_text}"}
            ],
            max_tokens=512,
            temperature=0.5,
        )
        summarized_text = response.choices[0].message['content'].strip()
        return summarized_text
    except Exception as e:
        print(f"Error: {e}")  # 에러를 로그에 출력
        return '요약 실패'

def translate_and_summarize(request):
    if request.method == 'POST':
        english_text = request.POST.get('english_text')
        if not english_text:
            return JsonResponse({'summarized_text': '텍스트가 비어 있습니다.'}, status=400)

        translated_text = translate_text(english_text)
        if translated_text == '번역 실패':
            return JsonResponse({'summarized_text': '번역 실패'}, status=400)

        summarized_text = summarize_text(translated_text)
        return JsonResponse({'summarized_text': summarized_text})
    return JsonResponse({'summarized_text': '잘못된 요청입니다.'}, status=400)

def summary(request):
    return render(request, 'mainapp/translatesummary.html')

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

def define_term(request):
    term = request.GET.get('term')
    if not term:
        return JsonResponse({'definition': '용어가 제공되지 않았습니다.'}, status=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an expert assistant that provides detailed definitions of technical terms."},
                {"role": "user", "content": f"Define the following term in Korean: {term}"}
            ],
            max_tokens=512,
            temperature=0.5,
        )
        definition = response.choices[0].message['content'].strip()
        return JsonResponse({'definition': definition})
    except Exception as e:
        print(f"Error: {e}")  # 에러를 로그에 출력
        return JsonResponse({'definition': '정의 실패'}, status=500)


def pptTranslate(request):
    if request.method == 'POST' and request.FILES.get('ppt_file'):
        ppt_file = request.FILES['ppt_file']

        # PPT 파일 읽기
        presentation = Presentation(ppt_file)
        translated_ppt = BytesIO()

        # 슬라이드를 순회하면서 텍스트 추출, 번역 및 업데이트
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    # 텍스트 추출 및 번역
                    original_text = shape.text.strip()
                    if original_text:  # 빈 문자열 확인
                        translated_text = translate_text(original_text)
                        shape.text = translated_text

        # 변경된 PPT 저장
        presentation.save(translated_ppt)
        translated_ppt.seek(0)

        # PPT를 클라이언트에 반환
        response = HttpResponse(translated_ppt,
        content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        response['Content-Disposition'] = 'attachment; filename="translated.pptx"'
        return response

    return render(request, 'mainapp/ppttranslate.html')
