import json
from datetime import datetime
from lib.user import User
from lib.Blood import Blood
from lib.Request import Request
import json
import os
import ast
import operator

currDir = os.getcwd()
bloodDir = currDir + "/lib/textfiles/blood.json"
requestDir = currDir + "/lib/textfiles/request.json"
medicalFacilityDir = currDir + "/lib/textfiles/medicalFacility.json"
userDir = currDir + "/lib/textfiles/userData.json"

class UserSystem:
	vampireRequests = []

	def logout_user(self):
		with open(userDir, 'r') as f:
			datastore = json.load(f)
		for element in datastore["user"]:
			if element["login"] == "True":
				element["login"] = "False"
				with open(userDir, 'w') as f:
					f.write(json.dumps(datastore,indent= 4))
				print("HI YYYYY")
				return "You have successfully logged out"
		return ""

	def check_user(self, email, password,role):
		user = ""
		with open(userDir, 'r') as f:
			datastore = json.load(f)
		for element in datastore["user"]:
			if element["email"] == email and element["password"] == password and element["role"] == role:
				element["login"] = "True"
				with open(userDir, 'w') as f:
					f.write(json.dumps(datastore,indent= 4))
				return ""
			else:
				message = "You have entered an invalid email/password"
		return "You have entered an invalid email/password"

	def check_login(self):
		with open(userDir, 'r') as f:
			datastore = json.load(f)
			for element in datastore["user"]:
				if element["login"] == "True":
					return True
		return False

	def check_employeeLogin(self):
		with open(userDir, 'r') as f:
			datastore = json.load(f)
			for element in datastore["user"]:
				if element["login"] == "True" and element["role"] == "Employee":
					return True
		return False

	def getUsers(self):
			users = []
			with open(userDir,"r") as json_file:
				data = json.load(json_file)
			for u in data['user']:
				object = User(u['username'],u['email'],u['password'],u['name'],u['role'])
				users.append(object)
			return users

	def get_username(self):
		with open(userDir, 'r') as f:
			datastore = json.load(f)
		for element in datastore["user"]:
			if element["login"] == "True":
				return element["username"]

	def get_user_email(self):
		with open(userDir, 'r') as f:
			datastore = json.load(f)
			for element in datastore["user"]:
				if element["login"] == "True":
					return element["email"]
	
	def show_users(self):
		with open(userDir, "r") as user_database:
			user = json.load(user_database)
		return user["user"]

	def check_username_unique(self, username):
		users = self.show_users()
		for u in users:
			if username == u["username"]:
				return 1
		return 0

	def check_email_unique(self, email):
		users = self.show_users()
		for u in users:
			if email == u["email"]:
				return 1
		return 0

	def create_user(self,username,name,email, password,role):
		data = {
		"username":username,
		"email": email,
		"name": name,
		"password": password,
		"login": "True",
		"role":role,
		}
		with open(userDir, 'r') as f:
			datastore = json.load(f)
		datastore["user"].append(data)
		with open(userDir, "w") as file:
			json.dump(datastore, file,indent= 4)
		return ""

	
