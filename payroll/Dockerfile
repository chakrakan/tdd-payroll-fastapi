# pull official base image
FROM python:3.9.6-slim-buster

# make working directory if !exists
RUN mkdir -p /usr/src/app

# set environment variables
ENV WORK_DIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set workdir
WORKDIR ${WORK_DIR}

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get -y install libmagic1 \
    && apt-get clean

# install pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Copy pipenv files
COPY Pipfile Pipfile.lock ${WORK_DIR}

# sync dependencies
RUN pipenv sync --system --dev --pre

# grab everything from payroll folder and push to container's payroll folder
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
