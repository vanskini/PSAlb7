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

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write("Введите фамилию: ".encode("utf-8"))
        self.wfile.flush()
        surname = self.rfile.readline().decode("utf-8").strip().lower()
        print(f"{self.client_address} ввёл фамилию: {surname}")

        if surname == "созонов":
            answer = "Созонову нельзя. Студент отчислен.\n"
        elif surname in STUDENTS:
            answer = f"Привет, {STUDENTS[surname]}\n"
        else:
            answer = "Такого в группе нет\n"

        self.wfile.write(answer.encode("utf-8"))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 7777
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"TCP-сервер запущен на {HOST}:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен")
