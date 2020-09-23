import socket,base64


def server():
    listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    listener.bind((socket.gethostname(),1234))
    listener.listen(0)
    connections=[]
    while len(connections)<2:
        conn ,addr = listener.accept()
        connections.append((conn))

    return (conn,addr)
