FROM python:3.8.16-bullseye
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ARG PROJECT=/usr/src/app
WORKDIR ${PROJECT}
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry export \
        --without-hashes \
        --with docker \
        -f requirements.txt \
        -o requirements.txt \
    && pip install -r requirements.txt
