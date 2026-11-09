import socketserver

STUDENTS = {
    "андриянов": "Миша",
    "бахтигозин": "Ильдар",
    "глуханюк": "Иван",
    "горбунов": "Миша",
    "деханов": "Ярик",
    "кашеваров": "Дима",
    "лакин": "Егор",
    "логинов": "Староста",
    "мошкин": "Рома",
    "нефедов": "Антон",
    "потешкин": "Влад",
    "сараева": "Софья",
}

class MyUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        data = self.rfile.readline().decode("utf-8").strip().lower()
        if not data:
            return

        print(f"{self.client_address} ввёл фамилию: {data}")

        if data == "созонов":
            answer = "Созонову нельзя. Студент отчислен.\n"
        elif data in STUDENTS:
            answer = f"Привет, {STUDENTS[data]}\n"
        else:
            answer = "Такого в группе нет\n"

        self.wfile.write(answer.encode("utf-8"))


class MyUDPServer(socketserver.UDPServer):
    allow_reuse_address = True   # чтобы порт не оставался занятым после Ctrl+C


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 7778
    with MyUDPServer((HOST, PORT), MyUDPHandler) as server:
        print(f"UDP-сервер запущен на {HOST}:{PORT}")
        print("Для остановки нажмите Ctrl+C")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен")
