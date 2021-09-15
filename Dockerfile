FROM python:3.9.5

WORKDIR /funyjane

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /src