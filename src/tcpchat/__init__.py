import PySimpleGUI as sg
from tcpchat.client import draw



def main():
    """メイン関数"""
    sg.theme("DarkBlue3")

    layout = [
        [sg.Text("サーバーIP:"), sg.Input(default_text="127.0.0.1", key="-SERVER_IP-")],
        [sg.Text("ポート番号:"), sg.Input(default_text="5000", key="-PORT-")],
        [sg.Text("ユーザー名:"), sg.Input(key="-USERNAME-")],
        [sg.Button("接続", key="-CONNECT-")],
        [sg.Output(size=(80, 20), key="-OUTPUT-")],
        [
            sg.Input(key="-MESSAGE-", do_not_clear=False),
            sg.Button("送信", key="-SEND-"),
        ],
    ]

    window = sg.Window("チャットクライアント", layout)
    client_socket = None

    draw(client_socket, window)

    if client_socket:
        client_socket.close()

    window.close()

