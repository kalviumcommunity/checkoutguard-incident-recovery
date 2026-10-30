import json,os,uuid
from datetime import datetime,timezone
from http.server import BaseHTTPRequestHandler,HTTPServer
release=os.environ["RELEASE"]
assert release in ["2026.10.2","2026.10.1"]
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        rid=str(uuid.uuid4())
        if self.path=="/health":code,body=200,{"status":"alive","release":release}
        elif self.path=="/checkout":
            code=503 if release=="2026.10.2" else 200
            body={"status":"unavailable" if code==503 else "accepted","release":release,"request_id":rid}
            event={"timestamp":datetime.now(timezone.utc).isoformat(),"level":"error" if code==503 else "info","message":"checkout rejected: release inventory adapter configuration incompatible" if code==503 else "checkout accepted","request_id":rid,"release":release,"status":code}
            print(json.dumps(event),flush=True)
        else:code,body=404,{"error":"not found"}
        self.send_response(code);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(json.dumps(body).encode())
HTTPServer(("0.0.0.0",8080),Handler).serve_forever()
