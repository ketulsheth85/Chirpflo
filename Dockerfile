FROM python:3.8.3

ENV APP_ROOT /src
ENV CONFIG_ROOT /config

RUN apt-get update
RUN apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev

RUN pip install --upgrade pip
RUN pip list --outdated

RUN mkdir ${CONFIG_ROOT}
COPY requirements.txt ${CONFIG_ROOT}/requirements.txt
RUN pip install -r ${CONFIG_ROOT}/requirements.txt

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}/webapp

ADD . ${APP_ROOT}

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


