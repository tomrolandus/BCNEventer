FROM python:3
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
ADD . /code
CMD echo "127.0.0.1  localhost" > /etc/hosts; python manage.py runserver --host 0.0.0.0 --port 5000