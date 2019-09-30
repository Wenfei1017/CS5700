import _thread
import struct
import socket
import time

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_port = 8048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# return current time
def now():
    return time.ctime(time.time())

# Calculate the expression client sent
def calculate(s):
    stack = []
    num, op = 0, '+'
    for i in range(len(s)):
        if s[i].isdigit():
            num = num * 10 + int(s[i])
        else:
            calc_helper(stack, op, num)
            num, op = 0, s[i]
    calc_helper(stack, op, num)
    return str(sum(stack))


# Helper function of calculator
def calc_helper(stack, op, num):
    if op == '+':
        stack.append(num)
    elif op == '-':
        stack.append(-num)

def recvall(conn, bufsize):
    data = b''
    data += conn.recv(2)
    len = struct.unpack('!h', data)[0]
    for i in range(0, len):
        data += conn.recv(2)
        exp_len = struct.unpack('!h', data[-2:])[0]
        if exp_len <= bufsize:
            data += conn.recv(exp_len)
        else :
            data += conn.recv(bufsize) + conn.recv(exp_len - bufsize)
    return data

def process_data(data):
    ans = b''
    exp_num = struct.unpack('!h', data[0: 2])[0]
    pos = 2
    ans += struct.pack('!h', exp_num)
    for i in range(0, exp_num):
        exp_len = struct.unpack('!h', data[pos: pos + 2])[0]
        pos += 2
        exp = data[pos: pos + exp_len].decode('utf-8')
        pos += exp_len
        res = calculate(exp)
        print(exp + '=' + res)
        ans += struct.pack('!h', len(res))
        ans += res.encode('utf-8')
    return ans


def handler(connectin):
    bufsize = 16
    data = recvall(connectin, bufsize)
    ans = process_data(data)
    connectin.sendall(ans)
    connectin.close()


def main():
    # Get host name, IP address, and port number.
    host_name = 'localhost'
    print('hostname is', host_name)
    host_ip = socket.gethostbyname(host_name)
    print('host IP address is', host_ip)

    host_port = 8048

    # Make a TCP socket object.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to server IP and port number.
    s.bind((host_ip, host_port))

    # Start listen to incoming requests.
    s.listen(20)
    print('\nServer started. Waiting for connection...\n')

    while True:
        connection, address = s.accept()
        print('Server is connected by', address, 'at', time.ctime(time.time()))
        _thread.start_new(handler, (connection,))

if __name__ == "__main__":
    main()