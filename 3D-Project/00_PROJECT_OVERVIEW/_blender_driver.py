"""Blender MCP driver -- send code to Blender on port 9876.
Server returns one JSON line without trailing newline, so we read until
the socket has been idle for ~0.5s after first bytes."""
import socket, json, sys, time

HOST, PORT = "127.0.0.1", 9876

def send(code, recv_timeout=120):
    s = socket.create_connection((HOST, PORT), timeout=recv_timeout)
    payload = json.dumps({"type": "execute_code", "params": {"code": code}})
    s.sendall((payload + "\n").encode())
    s.settimeout(recv_timeout)
    buf = b""
    # Read until idle for >0.5s after first chunk
    last = time.time()
    while True:
        try:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            last = time.time()
            if buf.endswith(b"\n"):
                break
        except socket.timeout:
            break
        # idle break
        if buf and (time.time() - last) > 0.5:
            break
    s.close()
    try:
        msg = json.loads(buf.decode())
    except Exception:
        return {"raw": buf.decode(errors="replace")}
    return msg

if __name__ == "__main__":
    code_path = sys.argv[1]
    with open(code_path, encoding="utf-8") as f:
        code = f.read()
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    r = send(code, recv_timeout=timeout)
    print(json.dumps(r, indent=2)[:4000])
