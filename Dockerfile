# syntax=docker/dockerfile:1

FROM python:3.11.6-bullseye

WORKDIR /home/

COPY . .

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]