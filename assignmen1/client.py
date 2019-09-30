import struct
import socket

# connect socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = '127.0.0.1'
server_port = 8048


# test function
def create_test(expressions):
	res = b''
	res += struct.pack('!h', len(expressions))
	for i in range(0, len(expressions)):
		res += struct.pack('!h', len(expressions[i]))
		res += expressions[i].encode('utf-8')
	return res


def recvall(connection, bufsize):
    result = b''
    while True:
        data = connection.recv(bufsize)
        result += data
        if len(data) < bufsize:
            break
    return result


# print data
def print_res(rec):
	num = struct.unpack('!h', rec[0: 2])[0]
	pos = 2
	for i in range(0, num):
		len = struct.unpack('!h', rec[pos: pos + 2])[0]
		pos += 2
		result = rec[pos: pos + len]
		pos += len
		print(result.decode('utf-8'))


def main():
    bufsize = 16
    s.connect((server_ip, server_port))
    print('Connected to server ', server_ip, ':', server_port)
    expressions = ['3+12', '3+5-3-2+301-1', '6+7', '8+11-5', '1+1', '1-1']
    result = create_test(expressions)
    print(result);
    s.sendall(result)
    data = recvall(s, bufsize)
    print("data is")
    print_res(data)
    s.close()

if __name__ == "__main__":
    main()