FROM python:3.8.3-alpine

# 작업 디렉토리 생성
WORKDIR /app

# 필요한 패키지 설치
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    build-base \
    cargo \
    rust \
    jpeg-dev \
    zlib-dev

# pip, setuptools, wheel 업데이트
RUN python -m pip install --upgrade pip setuptools wheel

# requirements.txt 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . /app

# 실행 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
