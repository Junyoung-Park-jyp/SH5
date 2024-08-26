from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from openai import OpenAI

@api_view(['GET'])
def api(request):
    if request.method == 'GET':
        payment = request.GET.get('payment')

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        response = client.chat.completions.create(
            model='gpt-4',
            messages=[
                {
                    'role': 'system',
                    'content': '당신은 결제 내역을 보고 "카페", "외식", "생필품" "쇼핑" 등과 같은 특정 카테고리로 분류하는 도움을 주는 어시스트턴트입니다. 대답은 무조건 하나의 단어로만 해주세요.'
                },
                {
                    "role": "user",
                    "content": payment
                },
            ]
        )
        answer = response.choices[0].message.content
        return Response({'category': answer})
    return Response({'error': 'Invalid request method.'}, status=400)
