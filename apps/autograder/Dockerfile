FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG SIARENA_REF=main

WORKDIR /opt/autograder

RUN pip install --no-cache-dir "git+https://github.com/jparisu/sIArena.git@${SIARENA_REF}"

COPY apps/autograder/autograder.py /opt/autograder/autograder.py

WORKDIR /work

ENTRYPOINT ["python", "/opt/autograder/autograder.py"]
