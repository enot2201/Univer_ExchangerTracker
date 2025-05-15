FROM python:3.12

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .



EXPOSE 5672
EXPOSE 6379
EXPOSE 5555
EXPOSE 5432
EXPOSE 8000

ENV REDIS_HOST=reddis
ENV RABBIT_HOST=rabbit
ENV POSTGRESS_HOST=db


