data=reliable_recv(conn)
     file_data=base64.b64decode(data["image"])
    #with open("datadt.jpg",'wb') as file:
    #	file.write(file_data)

     image = Image.open(file_data)
     image.load()
     

     image.show()
	 return "<h1>HELLO</h1>"
