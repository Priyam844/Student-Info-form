# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.10
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# Home IS created: gunicorn 26 needs $HOME/.gunicorn for its control socket.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

# Install dependencies (cached unless requirements.txt changes).
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
# .env and db.sqlite3 are excluded by .dockerignore - pass env at runtime.
COPY . .

# Build static assets (Django admin CSS/JS) into /app/staticfiles.
# Runs as root during build; files are world-readable for appuser.
RUN python manage.py collectstatic --noinput

# Switch to the non-privileged user to run the application.
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--worker-tmp-dir", "/tmp", "config.wsgi:application"]
