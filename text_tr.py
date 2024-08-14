import os
from groq import Groq

# Groq API 입력
client = Groq(api_key="my_api_key")

def translate_text(text):
    if not text:
        return {"error": "Missing required text"}

    # Groq 챗봇 설정하기
    prompt = f"Translate the following text from English to Korean: {text}"
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional translator. Translate the following text to fluent and natural Korean."},
            {"role": "user", "content": prompt},
        ],
        # 모델 mixtral 선택
        model="mixtral-8x7b-32768",
        temperature=0.3,  # 창의성 허락수준
        max_tokens=1024,  # 최대 토큰수
        top_p=1.0,  # 샘플링시 상위값 가져올 확률
        stop=None,  # api 답변 중지 시점
        stream=False  # 스트림 형식으로 response 전달
    )

    # 결과 출력하기
    translated_text = chat_completion.choices[0].message.content.strip()
    return {"translated_text": translated_text}

# 사용자 입력 받기
text = input("Enter the text to translate from English to Korean: ")

# 번역 수행
result = translate_text(text)

# 번역 결과 출력
if "error" in result:
    print(result["error"])
else:
    print("Translated Text:", result["translated_text"])
