FROM python:3.8-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# RUN apk update && apk add build-base linux-headers
RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN addgroup -S appuser && adduser -S appuser -G appuser
WORKDIR /home/appuser
USER appuser

COPY . .

ENTRYPOINT [ "gunicorn", "-w", "4", "-b", "0.0.0.0", "app:app" ]