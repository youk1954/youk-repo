import os, sys, datetime
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

ACCOUNT = os.environ["AZ_STORAGE_ACCOUNT"]           # youkconapps
CONTAINER = os.environ["AZ_BLOB_CONTAINER"]          # logs
PREFIX = os.environ.get("BLOB_PREFIX", "access")
APP = os.environ.get("APP_NAME", "app")

cred = DefaultAzureCredential()
svc = BlobServiceClient(account_url=f"https://{ACCOUNT}.blob.core.windows.net", credential=cred)
container = svc.get_container_client(CONTAINER)
try:
    container.create_container()
except Exception:
    pass  # 이미 있으면 무시

def get_blob_client():
    # 날짜별 폴더/파일명: YYYY/MM/DD/access-<app>.log
    date = datetime.datetime.utcnow().strftime("%Y/%m/%d")
    name = f"{date}/{PREFIX}-{APP}.log"
    bc = svc.get_blob_client(CONTAINER, name)
    try:
        bc.create_append_blob()
    except Exception:
        pass
    return bc

bc = get_blob_client()
for line in sys.stdin:
    data = (line.rstrip("\n") + "\n").encode("utf-8")
    try:
        bc.append_block(data)
    except Exception:
        # 블랍이 없거나 세션 만료 등 → 새로 확보 후 재시도
        bc = get_blob_client()
        bc.append_block(data)
