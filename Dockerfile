FROM python:2
MAINTAINER Mike Heijmans <parabuzzle@gmail.com>

EXPOSE 8000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY gdax_exporter.py gdax_exporter.py

CMD [ "python", "./gdax_exporter.py" ]