from socket import AF_INET, socket, SOCK_STREAM
import select 
import sys 
  
server = socket(AF_INET, SOCK_STREAM)

IP_address = str('127.0.0.1') if len(sys.argv) < 2 else str(sys.argv[1])
Port = int(9999) if len(sys.argv) else int(sys.argv[2])
server.connect((IP_address, Port)) 
  
while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            sys.stdout.write(message.decode("utf8"))
            sys.stdout.flush()
        else:
            message = sys.stdin.readline()
            server.send(bytes(message, "utf8"))
            sys.stdout.write("")
            sys.stdout.flush()
