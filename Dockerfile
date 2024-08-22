# Python 3.10을 베이스 이미지로 사용
FROM python:3.10

# pip 업그레이드
RUN pip install --upgrade pip

# 작업 디렉토리를 /app/SOLoTrip으로 설정
WORKDIR /app/SOLoTrip

# requirements.txt를 복사하고 의존성 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 소스 코드를 컨테이너로 복사
COPY . .

# 컨테이너의 8000번 포트를 외부에 노출
EXPOSE 8000

# Gunicorn을 사용하여 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:application"]
