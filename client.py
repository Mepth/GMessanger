import socket, sys, threading, base64

room_ip = '127.0.0.1'
room_port = 48000

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
            mes = input(' > ')
            sock.send(encode(mes))
        except:
            print('P2P server has been offed')
            sys.exit(0)
            exit()

def message_recv(sock):
    while 1:
        try:
            msg = sock.recv(4096)
            if msg == b'': break
            print(decode(msg))
        except:
            print('P2P server has been offed')
            sys.exit(0)
            exit()

def encode(message):
    msg = base64.b64encode(bytes(message, 'utf-8')) + b'()' + base64.b64encode(bytes(message, 'utf-8'))
    msg = msg.decode('utf-8').replace('a', 'а').replace('b', 'б').replace('c', 'с').replace('p', 'р').replace('t', 'т').replace('o', 'о').replace('=', '*')
    msg = msg.encode()
    return msg

def decode(message):
    msg = message.decode('utf-8').split('()')[0].replace('а', 'a').replace('б', 'b').replace('с', 'c').replace('р', 'p').replace('т', 't').replace('о', 'o').replace('*', '=')
    msg1 = base64.b64decode(msg).decode('utf-8')
    return msg1

main()
