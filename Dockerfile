FROM python:3.8.3-alpine

# 작업 디렉토리 생성
RUN mkdir /app
WORKDIR /app

# 필요한 패키지 설치
RUN apk add --no-cache mariadb-connector-c-dev build-base cargo

# pip 업그레이드 (setuptools는 pip에 의해 자동 설치됨)
RUN python -m pip install --upgrade pip

# requirements.txt 복사 및 설치
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 애플리케이션 소스 복사
COPY . /app

# 실행 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
