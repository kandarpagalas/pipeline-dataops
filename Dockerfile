FROM apache/airflow:2.10.4
USER root
# RUN apt-get install -yqq build-essential libssl-dev libffi-dev 

USER airflow
RUN pip install --upgrade pip setuptools
ADD requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir 
