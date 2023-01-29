FROM python:3
RUN mkdir /opt/binance-api

COPY requirements.txt /opt/binance-api
COPY main.py /opt/binance-api
COPY config.json /opt/binance-api

WORKDIR /opt/binance-api

RUN cd /opt/binance-api && pip3 install  --no-cache-dir -r requirements.txt

RUN useradd -ms /bin/bash binance

RUN chown -Rf binance:binance /opt/binance-api

USER binance

CMD ["python", "./main.py"]