import socket, string

flag = 'flag{'

while flag[-1] != "}":
    
    for i in string.printable[:94]:
        payload = (flag + i).encode()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.20.10", 1337))
        s.send(payload + b'\n')
        r = (s.recv(1028)).decode().strip('\n')
       
        if len(r) <= 106:
            flag += i
            print(flag, end="\r")
