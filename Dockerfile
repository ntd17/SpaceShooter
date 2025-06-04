FROM python:3.10-slim

# Instalações básicas
RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-17-jdk curl wget cmake \
    build-essential libffi-dev libssl-dev libsqlite3-dev \
    zlib1g-dev libbz2-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libreadline-dev liblzma-dev \
    libjpeg-dev libpng-dev locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Variáveis de ambiente
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PYTHONIOENCODING utf-8

# Instala Cython e Buildozer
RUN pip install --upgrade pip
RUN pip install Cython==0.29.36 buildozer==1.5.0

# Marca o python-for-android como seguro (evita erro de ownership)
RUN git config --global --add safe.directory /root/.buildozer/android/platform/python-for-android

# Clona python-for-android
RUN mkdir -p /root/.buildozer/android/platform/ && \
    cd /root/.buildozer/android/platform/ && \
    git clone https://github.com/kivy/python-for-android.git && \
    cd python-for-android && \
    git checkout v2023.02.10

WORKDIR /app
