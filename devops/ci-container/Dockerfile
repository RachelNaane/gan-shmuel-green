FROM python:alpine3.17

VOLUME [ "/var/run/docker.sock:/var/run/docker.sock" ]
RUN apk add docker && apk add docker-compose 
WORKDIR /app
COPY . .
RUN pip install -r req.txt
RUN  apk add bash && apk add git && apk add curl 
RUN git clone https://github.com/RachelNaane/gan-shmuel-green.git
ENTRYPOINT ["python3", "ci.py"]