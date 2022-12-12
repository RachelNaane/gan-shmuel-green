FROM python:alpine3.17

WORKDIR /app
COPY . .
RUN pip install -r req.txt

ENTRYPOINT ["python3", "ci.py"]