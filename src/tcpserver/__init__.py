import socket
import threading
from tcpserver.client import handle_client


def main():
    """メイン関数"""
    host = "127.0.0.1"
    port = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print((host, port))
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"[サーバーが起動しました: {host}:{port}]")

    clients = {}

    while True:
        try:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address, clients),
                daemon=True,
            )
            client_thread.start()
        except KeyboardInterrupt:
            print(f"プログラムを強制終了しました")
            break
