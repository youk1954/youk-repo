from flask import Flask, request
import datetime, os

app = Flask(__name__)
LOG_FILE = "/logs/access.log"
os.makedirs("/logs", exist_ok=True)

@app.route("/")
def hello():
    # Container Apps는 L7 프록시 뒤라서 X-Forwarded-For 헤더에 클라이언트 IP가 옴
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    now = datetime.datetime.utcnow().isoformat()
    line = f"{now} | {client_ip} | {request.path}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    return "<h1>Hello Container Apps World</h1><p>Your IP: {}</p>".format(client_ip)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
