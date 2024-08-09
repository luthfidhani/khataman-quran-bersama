FROM python:3.9-slim-bullseye

ENV APP_HOME /app
ENV APP_WORKERS 3
ENV PORT 8080

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt
CMD exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000