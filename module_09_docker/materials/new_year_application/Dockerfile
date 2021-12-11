FROM python:3.7.9-slim-stretch

RUN mkdir /new_year_application

COPY requirements.txt /new_year_application/

COPY app.py /new_year_application/

COPY templates /new_year_application/templates

COPY static /new_year_application/static

RUN python -m pip install -r /new_year_application/requirements.txt

WORKDIR /new_year_application

ENTRYPOINT ["python", "app.py"]