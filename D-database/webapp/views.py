from flask import render_template,url_for,flash,redirect,request,Blueprint,current_app
from flask_login import login_user, current_user, logout_user , login_required
from webapp import db
from webapp.model import Image_Base
from flask_wtf.file import FileField
import os
from webapp.image_processing import *
from webapp.wlan_security import sniff
from webapp.forms import Upload
import numpy as np
import base64
from PIL import Image
from webapp.tunnel import reliable_recv,reliable_send,server
import json
from webapp.client import client
import socket
from .audio_processing import *
from PIL import Image
from .ip_sorter import ip_sorted

users = Blueprint('users',__name__)

@users.route("/",methods=['GET'])
def init():
	return render_template("redirecter.html")

@users.route("/home",methods=['GET','POST'])
def index():
	conn ,addr = server()
	data=reliable_recv(conn)
	print(data['name'])
	if len(data)>0:
		if data['command']!="send":
			shape = data["shape"]
			image = Image_Base(username="S7bhash",name=data["name"],image=data["image"],w=shape[0],h=shape[1],c=shape[2])
			db.session.add(image)
			db.session.commit()
			return redirect(url_for('users.uploaded'))
		else:
			image = Image_Base.query.filter_by(image_name=data['name'])
			dict = {"image":image}
			reliable_send(data['ip'],dict)
			return redirect(url_for('users.init'))

	return render_template('index.html')

@users.route('/upload',methods = ['GET','POST'])
def upload():
	upload = Upload()
	hostnames = ["192.168.43.237","192.168.43.238"]
	if upload.validate_on_submit():
		if upload.file.data:
			if upload.file.data.filename.split('.')[-1]!='mp3':
				peer_images = crop_image(upload.file.data)
				i=0
				for ip in hostnames:
					if ip != "192.168.43.238":
						print(ip)
						image_data=peer_images[i]
						shape = image_data.shape
						command="scjhhsacjbds"
						dict = {'name':upload.name.data,"command":command,"image":image_data,"shape":shape}
						reliable_send(ip,dict)
					else:
						image_data = peer_images[i]
						shape = image_data.shape
						image = Image_Base(name=upload.name.data,username="S7bhash",image=image_data,w=shape[0],h=shape[1],c=shape[2])
						db.session.add(image)
						db.session.commit()
					i+=1
				return redirect(url_for('users.shower'))
		else:
			return "ERROR!"
			# else:
			# 	peer_audio = audio_split(upload.image.data)
			# 	for ip in hostnames:
			# 		if ip != socket.gethostname():
			# 			image_data = img2arr(peer_images[i])
			# 			shape = image_data.shape
			# 			client(ip,command,shape,image_data)
			# 		else:
			# 			image_data = img2arr(peer_images[:-1])
			# 			shape = image_data.shape
			# 			image = Image_Base(name=upload.name.data,username="S7bhash",image=image_data.tostring(),w=shape[0],h=shape[1],c=shape[2])
			# 			db.session.add(image)
			# 			db.session.commit()
			# 	return redirect(url_for('users.next'))

	return render_template('image_upload.html',form=upload)

@users.route('/uploaded',methods=['GET','POST'])
def uploaded():
	return "<h1>Uploaded</h1>"

@users.route('/signup',methods=['GET','POST'])
def signup():
	form = SignUp()
	if form.validate_on_submit():
		f = open('data.txt','w+')
		f.writelines(form.email.data)
		f.writeline("\n")
		f.writeline(form.username.data)
		f.writeline(form.password.data)
		return redirect(url_for('users.home'))
	return render_template('signup.html')


@users.route('/image/<name>',methods=['GET'])
def image(name):
	hostnames = ["192.168.43.237","192.168.43.238"]
	i=0
	images = []
	for ip in hostnames:
		if ip != "192.168.43.238":
			print(ip)
			command="send"
			dict = {'name':name,"command":"send",'ip':"192.168.43.238"}
			reliable_send(ip,dict)
			conn,addr = server()
			data=reliable_recv(conn)
			data['image']
			img = arr2img(data['image'],data['width'],data['height'],data['color'],data['image_name'])
			images.append(img)
			images.append(img)
			img.show()

		else:
			print("local!")
			image = Image_Base.query.filter_by(image_name=name).first()
			img = arr2img(image.image,image.width,image.height,image.color,image.image_name)
			images.append(img)
			images.append(img)
			img.show()
		i+=1
	final_image = join_image(images,1600,1024)
	final_image.show()

	return render_template('next.html')
@users.route('/show',methods=['GET','POST'])
def shower():
	image = Image_Base.query.filter_by(image_name='sajdas').first()
	img = arr2img(image.image,image.width,image.height,image.color,image.image_name)
	images = [img,img,img,img]
	final_image = join_image(images,1600,1024)
	final_image.show()
