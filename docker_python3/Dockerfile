# Use an official Python runtime as a parent image
FROM python:3.6.6-slim-jessie

# Install any needed packages specified in requirements.txt
WORKDIR /root
ADD .bashrc /root/

RUN apt-get update && apt-get install -y less mutt alien git emacs vim openssh-server openssh-client
RUN apt-get install -y build-essential unixodbc-dev

ADD Dockerfile /root/
RUN pip install --trusted-host pypi.python.org Cython
RUN pip install --trusted-host pypi.python.org scipy
RUN pip install --trusted-host pypi.python.org pandas jupyter scikit-learn tensorflow pyodbc

RUN git config --global user.name root
RUN git config --global user.email root@docker_myacct
RUN git config --global push.default simple

# Make port 8888 available to the world outside this container
# EXPOSE 8888

# Define environment variable
ENV USER root
ENV HOME /root
WORKDIR /root/dev

# Run app.py when the container launches
#CMD jupyter notebook --ip=0.0.0.0 --allow-root
#CMD ["python", "app.py"]

