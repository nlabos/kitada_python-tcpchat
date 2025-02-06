import PySimpleGUI as sg
import threading
import socket

def receive_messages(client_socket, window):
    """受信メッセージを処理する関数"""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                window["-OUTPUT-"].print(message)
            else:
                # サーバーが切断した場合
                window["-OUTPUT-"].print("[サーバーが切断されました]")
                break
        except OSError: 
            # ソケットが閉じられた場合
            break
    client_socket.close()


def draw(sock, window):
    """PySimpleGUIの描画を処理する関数"""
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
        
        if event == "-CONNECT-":
            try:
                server_ip = values["-SERVER_IP-"]
                port = int(values["-PORT-"])
                username = values["-USERNAME-"]
                if server_ip and port and username: 
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((server_ip, port))
        
                    client_socket.send(username.encode("utf-8"))
        
                    window["-OUTPUT-"].print(
                        f"[サーバーに接続しました: {server_ip}:{port}]"
                    )
                    window["-SERVER_IP-"].update(disabled=True)
                    window["-PORT-"].update(disabled=True)
                    window["-USERNAME-"].update(disabled=True)
        
                    # 受信スレッドを開始
                    receive_thread = threading.Thread(
                        target=receive_messages, args=(client_socket, window), daemon=True
                    )
                    receive_thread.start()
        
                    window["-CONNECT-"].update(disabled=True)
        
            except Exception as e:
                window["-OUTPUT-"].print(f"[エラー] {e}")
        
        elif event == "-SEND-" and client_socket:
            message = values["-MESSAGE-"]
            if message:
                try:
                    client_socket.send(f"{username}>> {message}".encode("utf-8"))
                except OSError:  # ソケットが閉じられた場合
                    window["-OUTPUT-"].print("[サーバーが切断されました]")
                    break

