import socket
import threading
import time
import config
import functions
import logging
import queue


class Server:
    def __init__(self):
        self.q = queue.Queue()
        self.s = functions.get_free_tcp_port()
        self.s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)
        threading.Thread(target=self.start_server).start()
        threading.Thread(target=self.start_udp_server).start()
        threading.Thread(target=self.start_client).start()

    def start_server(self):
        # print(config.TCP_PORT)
        with self.s:
            self.s.listen(1)
            running = True
            while running:
                # print(' in TCP server loop')
                try:

                    client, addr = self.s.accept()
                    config.server_has_client = True
                    print(str(addr) + " connected to the TCP server")
                    data = client.recv(1024)
                    print("TCP server got the msg " + data.decode())
                    logging.info(f'TCP server got the msg {data.decode()}')

                    if config.client_has_server:
                        new_data = functions.PutMistakeInMsg(data.decode())
                        self.q.put(new_data.encode())
                        logging.info(f'TCP server change the msg to {new_data}')
                        logging.info(f'we in rx-on-tx-on')
                    else:
                        print(10 * '--------')
                        print(f'TCP server ending the game with :  {data.decode()}')
                        logging.info(f'we in rx-on-tx-off')
                        print(10 * '--------')
                        client.close()
                        config.server_has_client = False
                        running = False

                except socket.timeout:
                    continue

    def start_udp_server(self):
        self.s_udp.bind((config.IP, config.UDP_PORT))
        with self.s_udp:
            running = True
            while running:
                try:
                    data, addr = self.s_udp.recvfrom(1024)
                    print(str(addr) + " connected to the UDP server")
                    self.s_udp.sendto(str(config.TCP_PORT).encode(), addr)
                except socket.timeout:
                    continue

    def start_client(self):

        try:
            time.sleep(5)
            self.client_udp.sendto(b"kill me", (config.IP, config.UDP_PORT + 1))
            from_server, addr = self.client_udp.recvfrom(4096)
            print(from_server)

            with self.client_tcp:
                self.client_tcp.connect((config.IP, int(from_server.decode())))
                config.client_has_server = True

                while True:
                    if not config.server_has_client:
                        self.q.put(input("what would you tell the world? : ").encode())

                    if not self.q.empty():
                        self.client_tcp.send(self.q.get())



        except socket.timeout:
            pass
        except OSError:
            pass


if __name__ == '__main__':
    config.UDP_PORT = int(input("give me udp port: "))
    Server()
