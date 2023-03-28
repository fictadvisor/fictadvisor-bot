# python version
ARG PYTHON_VERSION=3.11

# build stage
FROM python:${PYTHON_VERSION}-slim AS builder

ENV PATH /opt/venv/bin:$PATH
WORKDIR /opt
RUN python -m venv venv
RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root --only main

#run stage
FROM python:${PYTHON_VERSION}-slim

WORKDIR /opt
COPY --from=builder /opt/venv venv
ENV PATH /opt/venv/bin:$PATH
COPY app app

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]