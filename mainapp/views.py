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
    return render(request, 'mainapp/translatesummary.html')

def translate_text(english_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a translation assistant that translates English text to Korean."},
                {"role": "user", "content": f"Translate the following text to Korean: {english_text}"}
            ],
            max_tokens=1024,
            temperature=0.5,
        )
        translated_text = response.choices[0].message['content'].strip()
        print(translated_text)
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