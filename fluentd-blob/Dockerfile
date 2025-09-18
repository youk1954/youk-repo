FROM fluent/fluentd:v1.16-debian

USER root

# Python + venv 설치
RUN apt-get update && apt-get install -y python3-full python3-venv && rm -rf /var/lib/apt/lists/*

# 가상환경 생성 및 패키지 설치
RUN python3 -m venv /opt/pyenv \
 && /opt/pyenv/bin/pip install --upgrade pip \
 && /opt/pyenv/bin/pip install azure-identity azure-storage-blob

# Fluentd 설정 & 업로더 스크립트 복사
COPY fluentd.conf /fluentd/etc/fluentd.conf
COPY upload_to_blob.py /uploader/upload_to_blob.py

# 버퍼/업로더 디렉터리 권한
RUN mkdir -p /buffers && chown -R fluent:fluent /buffers /uploader

# 가상환경을 PATH에 등록
ENV PATH="/opt/pyenv/bin:${PATH}"

USER fluent

