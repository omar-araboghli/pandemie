FROM python:3.7

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/shared

COPY requirements.txt ./
RUN apt-get update
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 443

CMD [ "bash", "-c", "python ./tests/run.py && python ./app.py" ]