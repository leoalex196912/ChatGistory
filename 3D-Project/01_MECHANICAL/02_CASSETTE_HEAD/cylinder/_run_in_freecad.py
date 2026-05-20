"""Run the Cylinder V3.0 macro inside FreeCAD via XML-RPC (port 9875)."""
import xmlrpc.client

MACRO = r"C:\3D-Project\01_MECHANICAL\02_CASSETTE_HEAD\cylinder\freecad_macros\CSM_V3_Cylinder_V3_0.FCMacro"

code = r'''
import FreeCAD
for n in list(FreeCAD.listDocuments().keys()):
    try:
        FreeCAD.closeDocument(n)
    except Exception:
        pass
path = r"{MACRO}"
exec(compile(open(path, encoding="utf-8").read(), path, "exec"), {{"__name__": "__main__"}})
'''.format(MACRO=MACRO)

s = xmlrpc.client.ServerProxy("http://127.0.0.1:9875", allow_none=True)
r = s.execute_code(code)
print(r.get("message", r) if isinstance(r, dict) else r)
