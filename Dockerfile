FROM python:3.8
LABEL org.opencontainers.image.source https://github.com/manuel-anton-satec/satec-notification-service
COPY . /app
WORKDIR /app
#Install the dependencies
RUN pip install -r requirements.txt

RUN cd src

CMD [ "python", "manage.py", "runserver" ]