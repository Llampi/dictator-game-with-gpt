FROM --platform=$BUILDPLATFORM python:3.12-alpine AS builder
EXPOSE 8000
EXPOSE 80
WORKDIR /app 
RUN apk update && \
    apk add --no-cache build-base

#COPY requirements_base.txt /app
#RUN pip3 install -r requirements_base.txt --no-cache-dir
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN pip install pandas
COPY . /app 
CMD ["otree", "runprodserver", "8000"]

