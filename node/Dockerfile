FROM ghcr.io/maxotta/kiv-dsa-vagrant-base-docker:latest

RUN yum -q -y install python3
RUN yum -q -y install python3-pip
RUN pip3 install flask

COPY src /opt/distributed_color_assigner

CMD /usr/bin/python3 /opt/distributed_color_assigner/main.py
