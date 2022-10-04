from threading import Thread
import requests
import socketserver
import time
import socket
import src.receiver as receiver


def send_post_request(IP,PORT, result, TCP_server=None):
    time.sleep(5)
    result.append(requests.post(f"http://{IP}:{str(PORT)}/", data="TEST", timeout=10))
    if TCP_server:
        TCP_server.shutdown()

def test_http_post_response():
    PORT = 8000
    IP = "localhost"
    HANDLER = receiver.learning_http_handler

    with socketserver.TCPServer((IP, PORT), HANDLER) as httpd:
        print(f"Serving at ip {IP} and port {PORT}")
        response = []
        t = Thread(target=send_post_request, args=(IP, PORT, response, httpd,))
        t.start()
        httpd.serve_forever()
        t.join()

        assert response[0].status_code == 200

def test_http_post_capture():
    # TEST_STR = b"Hello"
    # CLIENT = ("192.168.1.1", 8080)
    # SERVER = ("localhost", 8080)
    # SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SOCK.bind(SERVER)
    # t = Thread(target=send_post_request, args=(SERVER[0], SERVER[0], [],))
    # t.start()
    # SOCK.listen(2)
    # SOCKET, addr = SOCK.accept()
    # t.join()

    # handler = receiver.learning_http_handler(SOCKET, CLIENT, SERVER)
    # #handler.headers.add_header("content-length", len(TEST_STR))
    # data = handler.do_POST()
    # assert data == TEST_STR
