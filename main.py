import threading
import socket

hostname = "192.168.1.1"

connection_limit = threading.BoundedSemaphore(value = 5)
connection = threading.Semaphore(value = 1)
openports = []
def scan(ip, port):
    try:
        s = socket.socket()
        s.settimeout(3)
        addr = (ip, port)
        s.connect(addr)
        connection.acquire()
        print ('[+] %s Open Port : %d' % (ip, port))
        openports.append(port)
        s.close()
    except:
        connection.acquire()
        print ('[-] %s Close Port : %d' % (ip, port))
    finally:
        connection_limit.release()
        connection.release()
def main():
    for i in range(1, 10000):
        connection_limit.acquire()
        ip = socket.gethostbyname(hostname)
        port = i
        t = threading.Thread(target=scan, args=(ip, port))
        t.start()
    for i in openports:
        print i
if __name__ == '__main__':
    main()
