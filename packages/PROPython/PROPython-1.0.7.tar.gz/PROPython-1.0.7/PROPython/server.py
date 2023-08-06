import socket
from _thread import *
from PROPython.Objects import Player
from PROPython.Settings import *
import pickle
from PROPython import Language

class Server():
    def __init__(self, port, max_connections, players_server, players_instance):
        if max_connections > 2:
            if Language().get_language() == "ENGLISH":
                print("[ERROR] You cannot make max_connections greater than 2")
            elif Language().get_language() == "RUSSIAN":
                print("[ОШИБКА] Вы не можете сделать больше чем 2 подключения")
            max_connections = 2
        # Server addres
        server = 'localhost'  # Not recommended to change it to public addres

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((server, port))

        # Max connections (players)
        self.s.listen(max_connections)
        if Language().get_language() == "ENGLISH":
            print("[SERVER] Waiting for a connection, Server Started")
        elif Language().get_language() == "RUSSIAN":
            print("[СЕРВЕР] Ожидание подключения, сервер запущен")

        # Players that can created
        if players_server:
            for player_instance in players_instance:
                players.append(player_instance)

    def threaded_client(self, conn, player):
        conn.send(pickle.dumps(players[player]))
        reply = ""
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                players[player] = data

                if not data:
                    if Language().get_language() == "ENGLISH":
                        print("[SERVER] Disconnected")
                    elif Language().get_language() == "RUSSIAN":
                        print("[СЕРВЕР] Отключен")
                    break
                else:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]

                    if Language().get_language() == "ENGLISH":
                        print("[SERVER] Received: ", data)
                        print("[SERVER] Sending : ", reply)
                    elif Language().get_language() == "RUSSIAN":
                        print("[] Получено: ", data)
                        print("[] Отправлено: ", reply)

                conn.sendall(pickle.dumps(reply))
            except:
                break

        if Language().get_language() == "ENGLISH":
            print("[SERVER] Lost connection")
        elif Language().get_language() == "RUSSIAN":
            print("[СЕРВЕР] Потеряное соединение")
        conn.close()

    def start(self):
        self.currentPlayer = 0
        while True:
            conn, addr = self.s.accept()
            if Language().get_language() == "ENGLISH":
                print("[SERVER] Connected to:", addr)
            elif Language().get_language() == "RUSSIAN":
                print("[СЕРВЕР] Подключен к:", addr)

            start_new_thread(self.threaded_client, (conn, self.currentPlayer))
            self.currentPlayer += 1