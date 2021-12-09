import socket
import os
 
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"
port = 12345
c_x="1001"
cou=0
opFile=open("clientop", "a")

Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	Server.bind((host, port))

except socket.error as e:
	print(str(e))

print("Server Listening on port " + str(port))

Server.listen(5)

def BinaryToDecimal(binary):
	string = int(binary, 2)
	return string

def binToStr(bin_data):
	str_data =''
	
	for i in range(0, len(bin_data), 8):
		temp_data = bin_data[i:i + 8]
		decimal_data = BinaryToDecimal(temp_data)
		str_data = str_data + chr(decimal_data)
	return str_data

def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def div(divident, divisor):
    pick = len(divisor)
    tmp = divident[0 : pick]
	
    while pick < len(divident):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick]
        else:
            tmp = xor('0'*pick, tmp) + divident[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)

    checkword = tmp
    return checkword


def ServerListner(cs):
	while True:
		try:
			msg = cs.recv(1024).decode()
			if(msg==''):
				break
		except Exception as e:
			print(f"Error: {e}")
			cs.close()
		else:
			# print(msg)
			remainder=div(msg, c_x)
			ind=0
			# print(remainder)
			var=0
			while ind<len(remainder):
				if remainder[ind]=='1':
					nak="NAK"
					# print(nak)
					cs.send(nak.encode())
					var=1
					break
				ind+=1
			if var==1:
				continue

			nak="success"
			cs.send(nak.encode())
			ind=len(remainder)
			ind+=len(c_x)-1
			pick=len(msg)-ind
			msg=msg[0:pick]
			msg=binToStr(msg)
			opFile.write(msg)
			for x in msg:
				if x=='~':
					break


if True:
	cs, caddr = Server.accept()
	print(f"[+] {caddr} connected to server.")
	ServerListner(cs)


cs.close()
Server.close()
