FROM python:3.7-slim-buster
WORKDIR /opt/journeys
RUN mkdir -p /opt/journeys

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/journeys/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/journeys/

EXPOSE 4000
ENTRYPOINT [ "python" ]
CMD ["serve.py"]
