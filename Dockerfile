FROM python:3
EXPOSE 5000
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python manage.py runserver --host 0.0.0.0 --port 5000