import http.client
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

HOST = "rokot.ibst.psu"
PATH = "/anatoly/"

class LinkImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.images = [], []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and "href" in d: self.links.append(d["href"])
        elif tag == "img" and "src" in d: self.images.append(d["src"])

def download_img(src, base_path, name):
    url = urljoin(f"http://{HOST}{base_path}", src)
    if url.startswith(f"http://{HOST}"):
        path = url[len(f"http://{HOST}"):]
        conn = http.client.HTTPConnection(HOST, 80)
        conn.request("GET", path, headers={"Host": HOST})
        with open(name, "wb") as f:
            f.write(conn.getresponse().read())
        conn.close()
        print(f" Скачано: {src} -> {name}")

conn = http.client.HTTPConnection(HOST, 80)
conn.request("GET", PATH, headers={"Host": HOST})
html = conn.getresponse().read().decode("utf-8", "ignore")
conn.close()

p = LinkImgParser()
p.feed(html)
for i, img in enumerate(p.images, 1):
    download_img(img, PATH, f"main_{i}.jpg")

for j, link in enumerate(p.links, 1):
    url = urljoin(f"http://{HOST}{PATH}", link)
    if urlparse(url).netloc == HOST:
        path = url[len(f"http://{HOST}"):]
        print(f"Переход: {path}")
        conn = http.client.HTTPConnection(HOST, 80)
        conn.request("GET", path, headers={"Host": HOST})
        sub_html = conn.getresponse().read().decode("utf-8", "ignore")
        conn.close()

        sub_p = LinkImgParser()
        sub_p.feed(sub_html)
        for k, img in enumerate(sub_p.images, 1):
            download_img(img, path, f"sub{j}_{k}.jpg")
