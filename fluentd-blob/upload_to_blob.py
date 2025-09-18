import os, time, datetime, sys
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.core.exceptions import ResourceExistsError, ServiceRequestError, ClientAuthenticationError

LOG_FILE = os.getenv("LOG_PATH", "/logs/access.log")
ACCOUNT  = os.environ["AZ_STORAGE_ACCOUNT"]
CONTAINER= os.environ["AZ_BLOB_CONTAINER"]
APP_NAME = os.getenv("APP_NAME", "app")
CLIENT_ID= os.getenv("AZURE_CLIENT_ID")  # UAMI clientId

# AAD (Managed Identity)
credential = DefaultAzureCredential(managed_identity_client_id=CLIENT_ID)
svc = BlobServiceClient(account_url=f"https://{ACCOUNT}.blob.core.windows.net", credential=credential)

def ensure_container():
    try:
        svc.create_container(CONTAINER)
        print(f"[INFO] created container: {CONTAINER}")
    except Exception:
        pass

def blob_name_for_now():
    now = datetime.datetime.utcnow()
    # 날짜 단위로 파일 구분
    return f"logs/{now:%Y/%m/%d}/access-{APP_NAME}.log"

def ensure_append_blob(bc: BlobClient):
    try:
        bc.create_append_blob()
        print(f"[INFO] created append blob: {bc.blob_name}")
    except ResourceExistsError:
        pass

def tail_lines(path):
    # 파일이 생길 때까지 대기
    while not os.path.exists(path):
        print(f"[INFO] waiting for log file: {path}")
        time.sleep(1)

    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)  # 기존 내용은 건너뛰고 새 라인부터
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line

def main():
    print("[INFO] uploader starting")
    ensure_container()

    current_blob = None
    bc = None

    for line in tail_lines(LOG_FILE):
        try:
            name = blob_name_for_now()
            if name != current_blob:
                current_blob = name
                bc = svc.get_blob_client(CONTAINER, current_blob)
                ensure_append_blob(bc)
            bc.append_block(line)
        except (ServiceRequestError, ClientAuthenticationError) as e:
            print(f"[WARN] transient error: {e}", file=sys.stderr)
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            time.sleep(2)

if __name__ == "__main__":
    main()
