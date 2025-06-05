import socket
import threading
import os
import random

HOST = '127.0.0.1'
PORT = 12345
CONFIG_DIR = "configuratii"
clients = {}  # name -> conn
lock = threading.Lock()

current_board = []
hit_heads = set()
TOTAL_AIRPLANES = 3

def alege_configuratie():
    fisiere = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.txt')]
    fisier_ales = random.choice(fisiere)
    print(f"[SERVER] Configuratie aleasa: {fisier_ales}")
    with open(os.path.join(CONFIG_DIR, fisier_ales)) as f:
        lines = [list(line.strip()) for line in f if line.strip()]
    return lines

def broadcast(msg):
    for conn in clients.values():
        try:
            conn.sendall(msg.encode())
        except:
            continue

def verifica_lovitura(linie, coloana):
    global current_board
    simbol = current_board[linie][coloana]
    if simbol in {'A', 'B', 'C'}:
        cap = (linie, coloana)
        if cap not in hit_heads:
            hit_heads.add(cap)
            return 'X'
        return '1'
    elif simbol in {'1', '2', '3'}:
        return '1'
    else:
        return '0'

def handle_client(conn, addr):
    name = None
    try:
        while True:
            conn.sendall(b"Introdu un nume unic: ")
            proposed_name = conn.recv(1024).decode().strip()
            with lock:
                if proposed_name and proposed_name not in clients:
                    name = proposed_name
                    clients[name] = conn
                    break
                else:
                    conn.sendall(b"Numele este deja folosit.\n")

        conn.sendall(f"Bun venit, {name}!\n".encode())
        print(f"[+] {name} conectat de la {addr}")

        while True:
            conn.sendall(b">> Introdu coordonate (ex: 3 4) sau 'exit': ")
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode().strip()

            if message.lower() == 'exit':
                break

            try:
                linie, coloana = map(int, message.split())
                if 0 <= linie < 10 and 0 <= coloana < 10:
                    rezultat = verifica_lovitura(linie, coloana)
                    conn.sendall(f"Rezultat: {rezultat}\n".encode())

                    if rezultat == 'X':
                        if len(hit_heads) == TOTAL_AIRPLANES:
                            broadcast(f"\n>>> {name} a doborât toate avioanele și a câștigat runda!\n")
                            # Resetăm jocul
                            hit_heads.clear()
                            current_board[:] = alege_configuratie()
                            broadcast(f"[SERVER] O nouă rundă a început! Continuați să trageți.\n")

                else:
                    conn.sendall(b"Coordonate invalide. Foloseste valori intre 0 si 9.\n")
            except:
                conn.sendall(b"Format invalid. Introdu 2 numere separate prin spatiu.\n")
    finally:
        if name:
            with lock:
                del clients[name]
            print(f"[-] {name} deconectat.")
        conn.close()

def main():
    #global current_board
    current_board[:] = alege_configuratie()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Ascult pe {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
