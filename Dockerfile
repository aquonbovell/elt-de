FROM apache/airflow:2.9.1

# Install dependencies
RUN pip install apache-airflow-providers-docker \
  && pip install apache-airflow-providers-http \
  && pip install apache-airflow-providers-airbyte

