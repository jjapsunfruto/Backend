# Python 3.8 Alpine 이미지 사용
FROM python:3.8.3-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 및 빌드 도구 설치
RUN apk add --no-cache \
    mariadb-connector-c-dev \
    build-base \
    musl-dev \
    cargo \
    rust \
    jpeg-dev \
    zlib-dev \
    libffi-dev \
    pkgconfig \
    gcc \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

# pip, setuptools, wheel 업데이트
RUN python -m pip install --upgrade pip setuptools wheel

# Rust 환경설정 (Rustup을 통해 Rust 설치)
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y --profile minimal && \
    /bin/sh -c "source $HOME/.cargo/env && rustup update && rustup default stable"

# requirements.txt 복사 후 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 소스 코드 복사
COPY . /app

# 불필요한 캐시 정리
RUN rm -rf /root/.cache/pip/*

# 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
