import socket


def send_udp_message(server, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(message.encode(), server)
    response, server_address = client_socket.recvfrom(1048)
    return response.decode()


if __name__ == '__main__':
    # ip = input('Enter IP address:')
    # port = int(input('Enter port: '))
    ip = '127.0.0.1'
    port = 12000
    response = ''
    while response != 'shutdown':
        message = input('Enter message: ')
        response = send_udp_message((ip, port), message)
        print(f'RESPONSE: {response}')
