import json
pydata={"name":"梅梅","age":20,"height":168,"gender":"女"}
jdata=json.dumps(pydata)
print(jdata)
py_explain=json.loads(jdata)
print(py_explain)