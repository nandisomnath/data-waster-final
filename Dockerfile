FROM alpine

RUN apk add python3
RUN apk add py3-pip
RUN apk add py3-virtualenv

WORKDIR /workspace

COPY . /workspace

RUN python3 -m venv .venv

RUN /workspace/.venv/bin/pip install -r requirements.txt

CMD ["/workspace/.venv/bin/python3", "main.py"]
