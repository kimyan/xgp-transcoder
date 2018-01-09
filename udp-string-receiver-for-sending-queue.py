import socket
import stomp
import json

if __name__ == '__main__':

    udp_ip_address = "0.0.0.0"
    udp_port = 3011

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip_address, udp_port))

    print('Start UDP server.')

    conn = stomp.Connection()
    conn.start()
    conn.connect('admin', 'admin', wait=True)

    while True:
        data, addr = sock.recvfrom(1024)
        data_str = data.decode('ascii')
        print("Received data: {0}".format(data_str))

        json_dict = {
            'string': data_str
        }

        conn.send(body=json.dumps(json_dict), destination='/queue/udpstring')

    # conn.disconnect()
