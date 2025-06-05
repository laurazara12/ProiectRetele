import socket

HOST = '127.0.0.1'
PORT = 12345

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    while True:
        data = sock.recv(1024).decode()
        print(data, end='')

        if "Introdu un nume unic" in data:
            name = input()
            sock.sendall(name.encode())
        elif "Bun venit" in data:
            break
        elif "Numele este deja folosit" in data:
            continue

    try:
        while True:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(data, end='')
            if ">>" in data:
                msg = input()
                sock.sendall(msg.encode())
                if msg.lower() == "exit":
                    break
    finally:
        sock.close()

if __name__ == "__main__":
    main()
