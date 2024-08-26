import requests

# url = 'https://www.ailabapi.com/api/image/effects/ai-anime-generator'

# payload={'type': 'boy-5'}
# files=[
#   ('image',('file',open('./test.jpg','rb'),'application/octet-stream'))
# ]
# headers = {
#   'ailabapi-api-key': ''
# }

# response = requests.request("POST", url, headers=headers, data=payload, files=files)

# print(response.text)

headers = {
  'ailabapi-api-key': ''
}

# 요청할 URL
url = 'https://www.ailabapi.com/api/common/query-async-task-result'

# 쿼리 파라미터 설정
params = {
    'task_id': '1724684240869.f4fb03a8-b905-e5cc-1713-c9707476d209'
}

# GET 요청 보내기
response = requests.get(url, headers=headers, params=params)

# 응답 상태 코드와 내용 출력
print(response.text)
