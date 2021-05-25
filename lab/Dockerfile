FROM jupyter/minimal-notebook:latest as builder
# FOR SPARK: FROM jupyter/pyspark-notebook:584f43f06586 as builder

COPY start.sh /start.sh

# ----------------------------------------------------------------------------
# PySpark
# NOTE: Enable this section if you need pyspark in Jupyter Labs and also
# change the base image (FROM)
# ----------------------------------------------------------------------------

# Install required Java libraries for Spark, and run pyspark at startup
# USER root
# RUN apt-get -y update && apt-get -y install curl && \
#     export HADOOP_VER=$(ls ${SPARK_HOME}/jars/hadoop-common-*.jar | sed -e 's/.*\([0-9].[0-9].[0-9]\).jar/\1/g') && \
#     cd "${SPARK_HOME}/jars" && \
#     # PostgreSQL
#     curl -O https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.19/postgresql-42.2.19.jar && \
#     # For AWS S3 and Minio
#     curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VER}/hadoop-aws-${HADOOP_VER}.jar && \
#     curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.375/aws-java-sdk-bundle-1.11.375.jar && \
#     # For Azure blob storage
#     curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-azure/${HADOOP_VER}/hadoop-azure-${HADOOP_VER}.jar && \
#     curl -O https://repo1.maven.org/maven2/com/microsoft/azure/azure-storage/8.6.6/azure-storage-8.6.6.jar && \
#     curl -O https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-util/9.3.24.v20180605/jetty-util-9.3.24.v20180605.jar && \
#     curl -O https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-util-ajax/9.3.24.v20180605/jetty-util-ajax-9.3.24.v20180605.jar && \
#     curl -O https://repo1.maven.org/maven2/org/wildfly/openssl/wildfly-openssl/1.0.4.Final/wildfly-openssl-1.0.4.Final.jar
# COPY start-pyspark.sh /start.sh

# ----------------------------------------------------------------------------

# Install python dependencies as root
USER root
RUN apt-get -y update && apt-get -y install \
  build-essential \
  libffi-dev \
  python3-dev \
  libssl-dev \
  cargo

ARG SERVICE_DIR=.
COPY ${SERVICE_DIR}/*.in /tmp/
RUN pip3 install --upgrade pip pip-tools
RUN pip-compile /tmp/requirements.in && \
    pip3 install -r /tmp/requirements.txt

# Create temp dir for notebooks at jovyan home dir
USER jovyan
RUN mkdir -p /home/jovyan/temp

# Start
CMD ["/start.sh"]
