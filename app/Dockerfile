FROM python:3.8
LABEL org.opencontainers.image.source https://github.com/manuel-anton-satec/satec-notification-service
COPY . /app
WORKDIR /app

# set environment variables
##Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

#Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]