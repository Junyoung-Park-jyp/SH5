from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from openai import OpenAI

# 지출 내역 프롬프트
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# 지출 내역 카테고리 (트리플 어플 참고)
categories = ['숙소', '항공', '교통', '관광', '식비', '카페', '쇼핑', '기타']

@api_view(['GET'])
def api(request):
    if request.method == 'GET':
        payment = request.GET.get('keyword')

        cnt = 0
        while True:
            response = client.chat.completions.create(
                model='gpt-4',
                messages=[
                    {
                        'role': 'system',
                        'content': '당신은 여행 시 발생하는 결제 내역을 보고 특정 카테고리로 분류하는 도움을 주는 어시스트턴트입니다. ' + ', '.join(categories) + '"의 카테고리 중에서 하나를 선택해서 무조건 한 단어로만 대답해주세요.'
                    },
                    {
                        'role': 'user',
                        'content': payment
                    },
                ]
            )
            answer = response.choices[0].message.content
            cnt += 1

            if answer in categories:
                break
        return Response({'category': answer, 'count': cnt})
    return Response({'error': 'Invalid request method.'}, status=400)
