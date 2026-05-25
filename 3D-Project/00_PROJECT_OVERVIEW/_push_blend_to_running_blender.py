"""Push the V3 .blend into the user's running Blender via MCP (port 9876)."""
import socket, json, time

HOST, PORT = "127.0.0.1", 9876
BLEND_PATH = r"C:\Users\LEONID\Downloads\CSM_V3_GitHub_Ready\csm-v3-repo\CSM_V3_ASSEMBLY\full_assembly\renders\CSM_V3_Assembly_V3.blend"

code = f'''
import bpy
import os

path = r"{BLEND_PATH}"
print("Opening:", path)
if not os.path.exists(path):
    print("ERROR: file not found")
else:
    bpy.ops.wm.open_mainfile(filepath=path)
    print("Opened. Frame viewport on assembly...")
    bpy.ops.object.select_all(action="SELECT")
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for region in area.regions:
                if region.type == "WINDOW":
                    with bpy.context.temp_override(area=area, region=region):
                        bpy.ops.view3d.view_selected()
                    for space in area.spaces:
                        if space.type == "VIEW_3D":
                            space.shading.type = "MATERIAL"
                    break
            break
    bpy.ops.object.select_all(action="DESELECT")
    print("Done. Scene loaded with", len(bpy.data.objects), "objects.")
'''

s = socket.create_connection((HOST, PORT), timeout=60)
s.sendall((json.dumps({"type": "execute_code", "params": {"code": code}}) + "\n").encode())
s.settimeout(60)
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
print(buf.decode(errors="replace")[:600])
