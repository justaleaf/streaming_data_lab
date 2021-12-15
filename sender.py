from sys import exit
import socket
import argparse
from time import sleep, time
from os.path import join, exists


parser = argparse.ArgumentParser(description='tcp sender')
parser.add_argument('--rate', type=float, default=1.0)
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--port', type=int, default=9999)

filename = join('data', 'scrapped', 'events.txt')
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((args.host, args.port))
s.listen(1)
while True:
    conn, addr = s.accept()
    try:
        i = 0
        with open(filename) as f:
            start = time()
            for line in f:
                out = line.encode('utf-8')
                i += 1
                conn.send(out)
                sleep(1 / args.rate)
            break
    except socket.error:
        pass
else:
    conn.close()