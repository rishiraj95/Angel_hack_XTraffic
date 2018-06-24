import socket
import select
import sys
import geocoder
import requests
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
   # print(read_sockets)

    for socks in read_sockets:

        if socks == server:
            message = socks.recv(2048)
            print(message.decode())
        else:
            message = str(sys.stdin.readline())
            if message=="Report Accident\n" or message=="REPORT ACCIDENT\n" or message=="report accident\n" or message=="Report accident\n":
                choice=input("Press '1' to use your location\nPress '2' to manually enter coordinates")
                if choice=='1':
                    while True:
                        send_url = 'http://freegeoip.net/json'
                        r = requests.get(send_url)
                        j = json.loads(r.text)
                        lat = j['latitude']
                        lon = j['longitude']
                        gloc = geocoder.google([lat, lon], method='reverse')
                        if gloc.ok==True:
                            break
                        else:
                            continue
                        
                    
                    try:
                        accident_message="Accident reported at <" +"lat = " + str(lat) +">, <lon = " +str(lon)+">\n" +gloc.city+", "+gloc.state+", "+gloc.country+" \n" 
                        server.send(accident_message.encode())
                        sys.stdout.write("<You>")
                        sys.stdout.write(accident_message)
                        sys.stdout.flush()
                                                 
                                
                    except:
                        print("Connection Failed")
                        sys.exit(0)
                elif choice=='2':
                    while True:
                        try:
                            lat=float(input("Please enter latitude in range 41 - 47"))
                            lon=float(input("Please enter longitude -71 - -77"))
                            break
                        except:
                            print("Invalid Input...Try again")
                            continue
                    gloc = geocoder.google([lat, lon], method='reverse')
                    try:
                        if gloc.ok==False:
                            print("Unable to fetch location for given coordinates")
                        else:
                            accident_message="Accident reported at <" +"lat = " + str(lat) +">, <lon = " +str(lon)+">\n" +gloc.city+", "+gloc.state+", "+gloc.country+" \n" 
                            server.send(accident_message.encode())
                            sys.stdout.write("<You>")
                            sys.stdout.write(accident_message)
                            sys.stdout.flush()
                    except:
                        print("Connection Failed")
                        sys.exit(0)

                else:
                    print("Invalid Input...Try again")
                    continue
                    

                
            else:
                server.send(message.encode())
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()

server.close()
