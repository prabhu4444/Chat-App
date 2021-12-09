import socket 
import random 

clientSocket = socket.socket()
connected = False
c_x="1001"

host = "localhost"
port = 12345
errorYN=0

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

def serverConnect():
	global errorYN
	print("waiting for connection")
	try:
		clientSocket.connect((host, port))
	except socket.error as e:
		print(str(e))

	print("connected, reading from client's input file")

	ipFile=open("clientip", "r+")
	entireMsg = ipFile.read()
	frames=[]
	while len(entireMsg)%8!=0:
		entireMsg+=' '
	for i in range (0, len(entireMsg)-8, 8):
		temps=entireMsg[i:i+8]
		frames.append(temps)
		
	index=0
	print(f"number of frames in input: {len(frames)}")
	countEframes={}

	for entMsg in frames:
		binMsg = ''.join(format(ord(i), '08b') for i in entMsg)
		p_x=binMsg
		p_x+=((len(c_x)-1)*"0")
		remainder=div(p_x, c_x)
		encoded=p_x+remainder
		# print(encoded)

		# print(f"done reading frame {index}... waiting for server's response")

		# print(div(encoded, c_x))
		while True:
			errorYN=random.randint(0, 100)%2

			toSend=encoded
			ind=random.randint(0,len(toSend)-1)
			if errorYN==0:
				temp=list(toSend)
				if temp[ind]=='1':
					temp[ind]='0'
				else:
					temp[ind]='1'
				toSend="".join(temp)

			try:
				clientSocket.send(toSend.encode())
			except socket.error as e:
				clientSocket.close()
				break
			else:
				try:	
					message = clientSocket.recv(1024).decode()
				except socket.error as e:
					clientSocket.close()
					break
				else:
					if message=="NAK":
						if index not in countEframes:
						    countEframes[index]=1
						else:
							countEframes[index]+=1
						continue
					else:
						break
		index+=1

	print(f"frequency of retransmitted frames: ")
	print(countEframes)
	print("written content in clientop, disconnecting...")
	clientSocket.close()



if True:
	print("To connect to the server press c and q to quit the program")
	a = input()

	if a.lower() == "c":
		connected = True
		serverConnect()





