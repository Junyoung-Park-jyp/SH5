import requests
import json
import time


AILAB_API_KEY = ''

# 20 credits
def portrait_animation(img_path: str) -> str:
    url = 'https://www.ailabapi.com/api/portrait/effects/portrait-animation'

    payload = {
        'type': 'pixar_plus',
        }
    files = [
        ('image', ('file', open(img_path, 'rb'), 'application/octet-stream'))
        ]
    headers = {
        'ailabapi-api-key': AILAB_API_KEY
        }
    
    response = requests.request('POST', url, headers=headers, data=payload, files=files)
    image_url = json.loads(response.text).get('data').get('image_url')
    return image_url


# 10 credits
def ai_anime_generator(img_path: str) -> str:
    url_post = 'https://www.ailabapi.com/api/image/effects/ai-anime-generator'

    payload = {
        'index': 0,  # Vintage Comic
        # 'index': 1,  # 3D Fairy Tale
        }
    files = [
        ('image', ('file', open(img_path, 'rb'), 'application/octet-stream'))
        ]
    headers = {
        'ailabapi-api-key': AILAB_API_KEY
        }
    
    response_post = requests.request('POST', url_post, headers=headers, data=payload, files=files)

    return json.loads(response_post.text).get('task_id')


def get_result(task_id: str) -> str:
    url_get = 'https://www.ailabapi.com/api/common/query-async-task-result'

    headers = {
        'ailabapi-api-key': AILAB_API_KEY
    }
    params = {
        'task_id': task_id
    }

    while True:
        response_get = requests.request('GET', url_get, headers=headers, params=params)
        response_json = json.loads(response_get.text)

        task_status = response_json.get('task_status')
        if task_status == 2:
            image_url = response_json.get('data').get('result_url')
            return image_url
        elif task_status == 1:
            print('Task is still processing.')
            time.sleep(5)


# print(portrait_animation('./test.JPG'))
print(get_result(ai_anime_generator('./test.JPG')))