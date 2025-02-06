import socket
import threading


def handle_client(client_socket, address, clients):
    """クライアントごとの処理"""
    print(f"[新しいクライアントが接続しました: {address}]")
    username = client_socket.recv(1024).decode("utf-8")  # ユーザー名を受信
    clients[client_socket] = username

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"[{address}] {message}")
                broadcast(message, client_socket, clients)
            else:
                # クライアントが切断した場合
                print(f"[クライアントが切断しました: {address}]")
                del clients[client_socket]
                client_socket.close()
                break
        except OSError:  # クライアントが切断した場合
            print(f"[クライアントが切断しました: {address}]")
            del clients[client_socket]
            client_socket.close()
            break
        except KeyboardInterrupt:
            print(f"プログラムを強制終了しました")
            break


def broadcast(message, sender_socket, clients):
    """全クライアントにメッセージをブロードキャスト"""
    for client_socket, username in clients.items():
        try:
            client_socket.send(message.encode("utf-8"))
        except OSError:  # 送信失敗時の処理
            print(f"[クライアントへの送信に失敗しました: {clients[client_socket]}]")
            del clients[client_socket]
            client_socket.close()
