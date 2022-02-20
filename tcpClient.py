import socket
import socket


def send_tcp_message(server, message):

    return response.decode();


if __name__ == '__main__':
    # ip = input('Enter IP address:')
    # port = int(input('Enter port: '))
    ip = '127.0.0.1'
    port = 12000
    server = (ip, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server)

    response = ''
    try:
        while True:
            message = client_socket.recv(1024)
            message = message.decode().upper()
            print(message)
            client_socket.sendall(message.encode())
    except:
        print('Relay server shut down!')
    finally:
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
