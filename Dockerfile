FROM repo.bigdata.local/python:3.8-slim

LABEL MAINTAINER thoatkn

RUN mkdir -p ~/.cache/clip
WORKDIR /app
COPY  /install /usr/local
ADD . .

CMD ["python", "/app/api.py"]
