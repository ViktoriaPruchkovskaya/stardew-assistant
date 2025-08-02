FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.7.10 /uv /uvx /bin/
ADD . /app

WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock
RUN uv sync --locked

COPY . .


CMD ["uv", "run", "main.py"]