FROM python:3.12

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt;

RUN pytest tests/;

EXPOSE 8000
