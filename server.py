import socket, threading, base64

clients = []

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
        clients.append(connect)

def client(connect, addr):
    print('[INFO] %s Has been connected' % (addr[0]))
    while True:
        try:
            data = connect.recv(4096)
            if data == b'':
                clients.remove(connect)
                break
            print('[MESSAGE] ' + addr[0] + ' -> ' + base64.b64decode(data).decode('utf-8'))
            print('Debug: ' + str(data) + ' len: ' + str(len(data)))
            send_message_to_all(addr, data.decode('utf-8'))
        except: pass

def send_message_to_all(addr, msg):
    try:
        with open('messages.log', 'a') as logf:
            logf.write(addr[0] + ' -> ' + base64.b64decode(msg).decode('utf-8') + '\n')
        for cli in clients:
            cli.send(msg.encode())
    except Exception as e:
        print('[AERROR] ' + e)
        clients.remove(cli)

main()