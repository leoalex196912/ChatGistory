"""Open V3 .blend in running Blender, no viewport frame."""
import socket, json, time

code = r'''
import bpy, os
path = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_Assembly_V3.blend"
if os.path.exists(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    print("OPENED. Objects:", len(bpy.data.objects))
else:
    print("NOT FOUND:", path)
'''

s = socket.create_connection(("127.0.0.1", 9876), timeout=60)
s.sendall((json.dumps({"type": "execute_code", "params": {"code": code}}) + "\n").encode())
s.settimeout(30)
buf = b""
last = time.time()
while True:
    try:
        c = s.recv(65536)
        if not c: break
        buf += c
        last = time.time()
        if buf.endswith(b"\n"): break
    except socket.timeout:
        break
    if buf and (time.time() - last) > 1.0:
        break
s.close()
print(buf.decode(errors="replace")[:800])
