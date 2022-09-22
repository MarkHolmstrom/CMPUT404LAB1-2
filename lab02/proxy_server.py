# Code taken from CMPUT 404 Fall 2022 Lab 2 code examples and CMPUT 404 Winter 2022 Lab videos
#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    host = 'www.google.com'
    port = 80
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
    
        #QUESTION 3
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s1.bind((HOST, PORT))
        #set to listening mode
        s1.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s1.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            
                remote_ip = get_remote_ip(host)
                
                s2.connect((remote_ip, port))
                print(f'Socket Connected to {host} on ip {remote_ip}')
                
                p = Process(target=handle_proxy, args=(addr, conn, s2))
                p.daemon = True
                p.start()
                print("Started process ", p)
            
            conn.close()

def handle_proxy(addr, conn, s2):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    s2.sendall(send_full_data)

    s2.shutdown(socket.SHUT_WR)

    data = s2.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    conn.send(data)                

if __name__ == "__main__":
    main()

