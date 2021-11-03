FROM gcr.io/webera/python

RUN groupadd -g 1000 app \
  && useradd -g app -m  -d /app -s /bin/sh -u 1000 app

USER app
WORKDIR /app

ENV ACCESS_LOG=${ACCESS_LOG:-/proc/1/fd/1}
ENV ERROR_LOG=${ERROR_LOG:-/proc/1/fd/2}
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

COPY .requirements.txt .

RUN python3 -m venv ${VIRTUAL_ENV} \
  && pip install -r .requirements.txt

COPY src .

ENTRYPOINT gunicorn \
  -b 0.0.0.0:8000 \
  -k uvicorn.workers.UvicornWorker \
  -w 4 \
  --access-logfile "$ACCESS_LOG" \
  --error-logfile "$ERROR_LOG" \
  main:app
