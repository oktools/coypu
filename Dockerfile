FROM ubuntu
MAINTAINER Daniel H. Morgan <dhm@streamgardens.com>
WORKDIR /tmp
COPY requirements/requirements.txt /tmp/
COPY requirements/test.txt /tmp/
COPY requirements/dev.txt /tmp/
RUN apt-get update
RUN apt-get install -y gcc python-dev python-pip libjpeg-dev zlib1g zlib1g-dev \
                libtiff5 libfreetype6 git python-pillow python-dev musl-dev \
                bash python-lxml libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 \
                libffi-dev shared-mime-info

RUN pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/test.txt
RUN pip install -r /tmp/dev.txt

# docker run --link <mongo_container_id>:mongo -v $PWD:/quokka -t -i oktools/coypu /bin/bash
