FROM python:3.8
LABEL org.opencontainers.image.source https://github.com/manuel-anton-satec/satec-notification-service
COPY . /app
WORKDIR /app

#Expose port 8000
EXPOSE 8000 

# set environment variables
#Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

#Install the dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", "127.0.0.1:8000" ]