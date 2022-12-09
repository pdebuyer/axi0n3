FROM python:3.9-slim

WORKDIR /home/

RUN apt-get update && apt-get upgrade && apt-get -y install libpq-dev gcc

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "axione.api:app", "--reload", "--host", "0.0.0.0"]
