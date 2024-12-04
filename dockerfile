# 베이스 이미지로 Python 3.11을 사용합니다.
FROM python:3.11

# 작업 디렉토리를 설정합니다.
WORKDIR /src

# 필요한 파일들을 복사합니다.
COPY requirements.txt /src/requirements.txt

# 종속성을 설치합니다.
RUN pip install --no-cache-dir -r /src/requirements.txt

# 애플리케이션 파일들을 복사합니다.
COPY . /src

ENV PYTHONPATH=/src
# 포트를 설정합니다.
EXPOSE 8000

# FastAPI 애플리케이션을 실행합니다.
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["bash", "-c", "python app/migration.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

