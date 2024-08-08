import openai
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

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
    return render(request, 'mainapp/translate.html')


def translate_text(english_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a translation assistant that translates English text to Korean."},
                {"role": "user", "content": f"Translate the following text to Korean: {english_text}"}
            ],
            max_tokens=1024,
            temperature=0.5,
        )
        translated_text = response.choices[0].message['content'].strip()
        return translated_text
    except Exception as e:
        print(f"Error: {e}")  # 에러를 로그에 출력
        return '번역 실패'


def summary(request):
    return render(request, 'mainapp/summary.html')


def pdfTranslate(request):
    return render(request, 'mainapp/pdfTranslate.html')
