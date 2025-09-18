FROM fluent/fluentd:v1.16-debian
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 install azure-identity azure-storage-blob
# Fluentd 설정 & 업로더 스크립트 복사
COPY fluentd.conf /fluentd/etc/fluentd.conf
COPY upload_to_blob.py /uploader/upload_to_blob.py
# 버퍼/업로더 디렉터리 권한
RUN mkdir -p /buffers && chown -R fluent:fluent /buffers /uploader
USER fluent
