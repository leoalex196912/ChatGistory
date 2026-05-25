import xmlrpc.client, time, os

s = xmlrpc.client.ServerProxy("http://127.0.0.1:9875", allow_none=True)
code = r"""
import sys, FreeCAD, os
with open(r"C:\Users\LEONID\AppData\Local\Temp\freecad_info.txt", "w") as f:
    f.write("PYTHON:" + sys.executable + chr(10))
    f.write("FREECAD_HOME:" + FreeCAD.getHomePath() + chr(10))
    f.write("USER_APPDATA:" + FreeCAD.getUserAppDataDir() + chr(10))
    f.write("VERSION:" + str(FreeCAD.Version()) + chr(10))
"""
s.execute_code(code)
time.sleep(2)
p = r"C:\Users\LEONID\AppData\Local\Temp\freecad_info.txt"
print(open(p).read() if os.path.exists(p) else "not written yet")
