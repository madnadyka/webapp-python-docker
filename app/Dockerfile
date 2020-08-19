
FROM ubuntu:18.04
MAINTAINER Nadezhda Karpova <nadyka@bitaps.com>
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev \
    git
COPY requirements.txt .
RUN pip3 install --requirement requirements.txt
WORKDIR /
RUN mkdir config
RUN mkdir src
WORKDIR /src
ENTRYPOINT ["python3"]
CMD  ["main.py"]