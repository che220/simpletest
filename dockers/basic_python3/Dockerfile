# Use an official Python runtime as a parent image
FROM python:3.6.6-slim-jessie

# Install any needed packages specified in requirements.txt
WORKDIR /root
ADD .bashrc /root/
ADD Dockerfile /root/

WORKDIR /root/bin
ADD train /root/bin/

RUN apt-get update && apt-get install -y less alien vim build-essential

# install packages for ML
RUN pip install --trusted-host pypi.python.org Cython
RUN pip install --trusted-host pypi.python.org scipy
RUN pip install --trusted-host pypi.python.org scikit-learn

# AWS
RUN pip install --trusted-host pypi.python.org boto3 awscli

# expose jupyter notebook's port
EXPOSE 8888

# Define environment variable
ENV USER=root
ENV HOME=/root
ENV PATH="/root/bin:${PATH}"

#ENTRYPOINT ["/root/bin/train"]

