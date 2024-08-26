from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from openai import OpenAI

# 환경 변수나 설정 파일에서 API 키를 가져오는 것이 안전합니다.

# openai.api_key = OPENAI_API_KEY

@api_view(['GET'])
def api(request):
    if request.method == 'GET':
        client = OpenAI(api_key=OPENAI_API_KEY)
        # user_input = request.POST.get('user_input')
        user_input = 'Hello'

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                    },
            ]
        )
        answer = response.choices[0].message.content
        print(answer)
        return JsonResponse({'response': answer})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
