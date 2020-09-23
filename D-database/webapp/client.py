import socket,json,base64

def client(ip,command,shape,image_data,name):
	connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connection.connect((ip,12345))
	dictionary = {"command":command,"name":name,"shape":command,"image":image_data}
	json_data=json.dumps(dictionary)
	connection.send(bytes(json_data,"utf-8"))

#client("192.168.31.135","asdsd",(124,554,54),"asdsad","sadas")
