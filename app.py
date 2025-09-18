from flask import Flask, request
import os, datetime

app = Flask(__name__)

LOG_PATH = "/logs/access.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def write_access(ip, path="/"):
    ts = datetime.datetime.utcnow().isoformat(timespec="microseconds") + "Z"
    line = f"{ts} | {ip} | {path}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()

@app.route("/", methods=["GET"])
def hello():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    write_access(ip, "/")
    return "<h1>Hello Container Apps World</h1><p>Your IP: {}</p>".format(ip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
