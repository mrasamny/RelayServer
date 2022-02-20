import os
import re
import socket
import selectors


def get_ip(ifaces=['wlan1', 'eth0', 'wlan0']):
    if isinstance(ifaces, str):
        ifaces = [ifaces]
    for iface in list(ifaces):
        search_str = f'ifconfig {iface}'
        result = os.popen(search_str).read()
        com = re.compile(r'(?<=inet )(.*)(?= netmask)', re.M)
        ipv4 = re.search(com, result)
        if ipv4:
            ipv4 = ipv4.groups()[0]
            return ipv4
    return ''


def start_tcp_server(ip,port):
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((ip, port))
    tcp_server_socket.listen(1)
    tcp_server_socket.setblocking(False);
    print(f"The TCP server is ready on ({ip}, {port}).")
    return tcp_server_socket


def start_udp_server(ip, port):
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((ip, port))
    udp_server_socket.setblocking(False);
    print(f"The UDP server is ready on ({ip}, {port}).")
    return udp_server_socket


def accept_tcp_connection(tcp_server):
    tcp_connection_socket, addr = tcp_server.accept()
    tcp_connection_socket.setblocking(True)
    print(f"Accepted connection from {addr}!")
    return tcp_connection_socket, addr


def send_receive(tcp_socket, udp_socket):
    # TODO: get message from udp_socket
    # TODO: send message to tcp_socket for processing
    # TODO: if an exception is raised, then send a 'NOT_READY' message to udp_socket
    # TODO: otherwise read message from tcp_socket and relay back to udp_socket
    pass  # replace this line with your code


if __name__ == "__main__":
    sel = selectors.DefaultSelector()
    # Get IP address from user
    ip = input('Enter an IP address (return for localhost):')
    if len(ip.strip()) < 1:
        ip = '127.0.0.1'
    # start up tcp and udp servers and register them with selectors
    tcp_server = start_tcp_server('127.0.0.1', 12000)
    sel.register(tcp_server, selectors.EVENT_READ, data='TCP_ACCEPT')
    udp_server = start_udp_server('127.0.0.1', 12000)
    sel.register(udp_server, selectors.EVENT_READ, data='UDP')

    try:
        tcp_client_socket = None
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data == 'TCP_ACCEPT':
                    if tcp_client_socket is not None:  # client disconnected - close connection properly
                        tcp_client_socket.shutdown(socket.SHUT_RDWR)
                        tcp_client_socket.close()
                    tcp_client_socket, addr = accept_tcp_connection(key.fileobj)
                    try:  # try sending to and receiving a greeting from tcp client
                        tcp_client_socket.sendall("hello".encode())
                        greet = tcp_client_socket.recv(1024)
                        print(f'GREETING: {greet.decode()}!')
                    except Exception as e:  # if exception occurs, then stop server
                        print(e)
                        raise Exception
                elif key.data == 'UDP':
                    # send message from UDP client to TCP client for processing and return
                    # response from TCP client to UDP client
                    udp_client_socket = key.fileobj
                    send_receive(tcp_client_socket, udp_client_socket)
    except Exception as e:
        sel.close()
        print(e)