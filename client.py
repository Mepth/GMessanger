import socket, sys, threading, base64

room_ip = 'mc.hipixel.ru'
room_port = 48002

def main():
    try:
        sock = socket.socket()
        sock.connect((room_ip, room_port))
        print('You has bees successfulled connected to a chat room, get kaef')
        print('Hi, are you in my room to write here anything, all messages are encrypted and nobody can listen')
    except:
        print('Sorry, but this room is not working ((')
    threading.Thread(target=console,      args=(sock,)).start()
    threading.Thread(target=message_recv, args=(sock,)).start()

def console(sock):
    while 1:
        try:
            mes = input(' > \n')
            sock.send(base64.b64encode(bytes(mes, 'utf-8')))
        except:
            print('P2P server has been offed')
            sys.exit(0)
            exit()

def message_recv(sock):
    while 1:
        try:
            msg = sock.recv(1024)
            if msg == b'': break
            print('\n+ | ' + base64.b64decode(msg).decode('utf-8'))
        except:
            print('P2P server has been offed')
            sys.exit(0)
            exit()
main()