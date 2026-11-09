import http.client

HOST = "rokot.ibst.psu"
PATH = "/anatoly/"

conn = http.client.HTTPConnection(HOST, 80, timeout=10)

conn.request("GET", PATH, headers={
    "Host": HOST,
    "User-agent": "PY prog"
})

r = conn.getresponse()

print("Proto:", r.version)
print("Code:", r.status)
print("Status:", r.reason)

print("Headers")
print(r.headers)

print("body")
body = r.read()
print(body.decode("utf-8", errors="replace"))

conn.close()

with open("index.html", "wb") as f:
    f.write(body)
print("\n[+]  страница сохранена в индекс штмл")
