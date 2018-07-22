# Use an official Python runtime as a parent image
FROM python:3.6.6-slim-jessie

# Install any needed packages specified in requirements.txt
WORKDIR /root
ADD .bashrc /root/
ADD Dockerfile /root/

# Note: odbc requires odbc.ini and odbcinst.ini. For vertica, need vertica.ini
# For kerberos, need keytab files
RUN apt-get update && apt-get install -y less mutt alien git emacs vim openssh-server openssh-client
RUN apt-get install -y build-essential unixodbc-dev

# install packages for ML
RUN pip install -U pip
RUN pip install --trusted-host pypi.python.org Cython
RUN pip install --trusted-host pypi.python.org scipy
RUN pip install --trusted-host pypi.python.org pandas jupyter scikit-learn tensorflow pyodbc

# AWS
RUN pip install --trusted-host pypi.python.org boto3 awscli

# install spacy
RUN pip install --trusted-host pypi.python.org spacy
RUN python -m spacy download en
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md
RUN python -m spacy download en_core_web_lg
RUN python -m spacy download en_vectors_web_lg

RUN git config --global user.name root
RUN git config --global user.email root@docker_myacct
RUN git config --global push.default simple

# expose jupyter notebook's port
EXPOSE 8888

# Define environment variable
ENV USER root
ENV HOME /root
WORKDIR /root/dev

# Run app.py when the container launches
#CMD jupyter notebook --ip=0.0.0.0 --allow-root
#CMD ["python", "app.py"]

