FROM python:3.12.7-slim-bookworm AS builder

ARG TZ=America/New_York

RUN pip install requests python-kasa \
    && pip cache purge

FROM python:3.12.7-slim-bookworm

ARG TZ=America/New_York
ARG PYVER=3.12

COPY --from=builder /usr/local/lib/python$PYVER/site-packages/ /usr/local/lib/python$PYVER/site-packages/

RUN mkdir /app
COPY ./app.py /app
RUN chmod 755 /app/app.py

ENTRYPOINT [ "python3", "-u", "/app/app.py" ]
