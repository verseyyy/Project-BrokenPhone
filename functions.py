import socket
from struct import pack
import random

import config
from config import *
import logging


def get_free_tcp_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    findPort = None
    for port in range(6005, 7001):
        try:
            sock.bind(('0.0.0.0', port))
            config.TCP_PORT = port
            return sock

        except:
            continue
    return findPort


def ip_to_byte(strIp):
    return b''.join(map(lambda x: pack('B', int(x)), strIp.split('.')))


def byte_to_ip(binaryIp):
    return '.'.join(map(str, binaryIp))


def random_num_size_N_digit(N):
    range_start = 10 ** (N - 1)
    range_end = 10 ** N - 1
    return random.randint(range_start, range_end)


def build_offer(request):
    offer = bytearray()
    offer.extend(MY_NAME.encode())
    offer.extend(request[16:20])
    offer.extend(ip_to_byte(IP))
    offer.extend(MAIN_PORT.to_bytes(2, byteorder='big'))
    return offer


def build_request():
    rand_num = random_num_size_N_digit(4)
    request = f'{MY_NAME}{rand_num}'
    return request.encode()


def extract_offer(offer):
    # return name,rnd_num, ip, port
    name = offer[:16].decode()
    rnd_num = offer[16:20].decode()
    ip = offer[20:24].decode()
    port = offer[24:26].decode()
    return name, rnd_num, ip, port


def extract_request(request):
    # return name ,rnd_num
    name = request[:16].decode()
    rnd_num = request[16:20].decode()
    return name, rnd_num


def PutMistakeInMsg(msg):
    st = msg
    ind = random.randint(0, len(st) - 1)
    newSt = st[:ind] + chr(ord(st[ind]) + 1) + st[ind + 1:]
    return newSt


def writeRequest(request, operation='Sending'):
    print(10 * '--------')
    name, rnd_num = extract_request(request)
    logging.info(f'{operation} Request:')
    logging.info(f'name: {name} rnd_num: {rnd_num}')
    logging.info(f'********************************************')
    print(f'{operation} Request:')
    print(f'name: {name} rnd_num: {rnd_num}')
    print(10 * '--------')


def writeOffer(offer, operation='Sending', fromIp=None):
    pass
