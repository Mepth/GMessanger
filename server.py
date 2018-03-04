import socket, threading, base64

clients = set()

ips, ports = '0.0.0.0', 48000

debug = True

def main():
    sock = socket.socket()
    sock.bind((ips, ports))
    sock.listen(4096)
    print('[INFO] OK Listen %s:%s' % (ips, str(ports)))
    while True:
        connect, addr = sock.accept()
        threading.Thread(target=client, args=(connect, addr,)).start()
        clients.add(connect)

def client(connect, addr):
    print('[INFO] %s Has been connected' % (addr[0]))
    while True:
        try:
            data = connect.recv(4096)
            if data == b'':
                clients.discard(connect)
                connect.close()
            print('[MESSAGE] ' + addr[0] + ' -> ' + decode(data))
            print('Debug: ' + str(data) + ' len: ' + str(len(data)))
            send_message_to_all(addr, decode(data))
        except:
            try:
                connect.close()
                clients.discard(connect)
            except: pass


def send_message_to_all(addr, msg):
    try:
        ip = addr[0].split('.')
        ip = ip[0] + '.*.*.' + ip[3]
        for cli in clients:
            cli.send(encode(ip + ' > ' + msg))
    except Exception as e:
        print('[AERROR] ' + e)
        clients.discard(cli)

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
