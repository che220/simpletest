# Use latest ubuntu
FROM ubuntu:latest

# Install any needed packages specified in requirements.txt
WORKDIR /root
ADD train /root/

#RUN apt-get update && apt-get install -y vim

# Define environment variable
ENV USER=root
ENV HOME=/root
ENV PATH="/root:${PATH}"
