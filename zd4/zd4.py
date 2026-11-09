import http.client
from html.parser import HTMLParser
from urllib.parse import urljoin

HOST = "rokot.ibst.psu"
PATH = "/anatoly/"

class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for name, value in attrs:
                if name == "src":
                    self.images.append(value)

conn = http.client.HTTPConnection(HOST, 80)
conn.request("GET", PATH, headers={"Host": HOST})
html = conn.getresponse().read().decode("utf-8", "ignore")

parser = ImgParser()
parser.feed(html)

for i, src in enumerate(parser.images, 1):
    url = urljoin(f"http://{HOST}{PATH}", src)
    if url.startswith(f"http://{HOST}"):
        path = url[len(f"http://{HOST}"):]
        conn.request("GET", path, headers={"Host": HOST})
        data = conn.getresponse().read()
        with open(f"img_{i}.jpg", "wb") as f:
            f.write(data)
        print(f"Скачано: {src} -> img_{i}.jpg")
conn.close()
