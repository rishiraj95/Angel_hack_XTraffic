import socket
import sys
import signal
import select
from _thread import *




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()


IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
print('Starting Server...\n')

server.listen(10)
print('Server Active\n')
list_of_clients=[]

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def clientthread(conn,addr):
    disp_str="Welcome to XTraffic"
    conn.send(disp_str.encode())
    while True:
        try:
           byte_message=conn.recv(2048)
           message=byte_message.decode()
           if message:
               print("<" + addr[0] + "> " + message)
               message_to_send = "<" + addr[0] + "> " + message
               broadcast(message_to_send,conn)
                #prints the message and address of the user who just sent the message on the server terminal
           else:
               remove(conn)
        
        except KeyboardInterrupt:
            sys.exit(0)

        except:
            continue



while True:
    try:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(addr[0]+" connected")
        start_new_thread(clientthread,(conn,addr))

    except KeyboardInterrupt:
        sys.exit(0)

    except:
        sys.exit(0)
    
conn.close()
server.close()


        
