# Use an official Python runtime as a parent image
FROM ubuntu:18.04
RUN ln -fs /usr/share/zoneinfo/America/Chicago /etc/localtime

# Install any needed packages specified in requirements.txt
RUN apt-get update
RUN apt-get install -y python3.6 python3-pip less alien vim build-essential git emacs

# install packages for ML
RUN pip3 install --trusted-host pypi.python.org Cython spicy scikit-learn jupyter pandas opencv-python

# AWS
RUN pip3 install --trusted-host pypi.python.org boto3 awscli

# caffe
RUN apt-get install -y caffe-cpu

# Define environment variable
ENV USER=root
ENV HOME=/root
ENV PATH="/root/bin:${PATH}"
WORKDIR /

#ENTRYPOINT ["/root/bin/train"]

