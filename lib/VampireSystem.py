import json
from datetime import datetime
from lib.user import User
from lib.Blood import Blood
from lib.Request import Request
from lib.BloodSystem import BloodSystem
import json
import os
import ast
import operator
from datetime import date

currDir = os.getcwd()
bloodDir = currDir + "/lib/textfiles/blood.json"
requestDir = currDir + "/lib/textfiles/request.json"
medicalFacilityDir = currDir + "/lib/textfiles/medicalFacility.json"
userDir = currDir + "/lib/textfiles/userData.json"


class VampireSystem:
	employees = []
	deliveredBlood = []
	factoryBlood = []
	validBlood = []
	expiredBlood = []
	medicalFacilities = []
	vampireRequests = []

	requested_id = []
	users = []
	requestSent = {}
	bloodTypes = ["A", "B", "AB", "O"]
	for type in bloodTypes:
		requestSent[type] = False


	def __init__(self):
		pass

	def getRequestSent(self):
		return self.requestSent

	def updateRequestSent(self, type):
		self.requestSent[type] = True
		return self.requestSent

	# def logout_user(self):
	# 	with open(userDir, 'r') as f:
	# 		datastore = json.load(f)
	# 	for element in datastore["user"]:
	# 		if element["login"] == "True":
	# 			element["login"] = "False"
	# 			with open(userDir, 'w') as f:
	# 				f.write(json.dumps(datastore,indent= 4))
	# 			print("HI YYYYY")
	# 			return "You have successfully logged out"
	# 	return ""
	#
	#
	# def check_user(self, email, password):
	# 	user = ""
	# 	with open(userDir, 'r') as f:
	# 		datastore = json.load(f)
	# 	for element in datastore["user"]:
	# 		if element["email"] == email and element["password"] == password:
	# 			element["login"] = "True"
	# 			with open(userDir, 'w') as f:
	# 				f.write(json.dumps(datastore,indent= 4))
	# 			return ""
	# 		else:
	# 			message = "You have entered an invalid email/password"
	# 	return "You have entered an invalid email/password"
	#
	# def check_login(self):
	# 	with open(userDir, 'r') as f:
	# 		datastore = json.load(f)
	# 		for element in datastore["user"]:
	# 			if element["login"] == "True":
	# 				return True
	# 	return False
	#
	# def check_employeeLogin(self):
	# 	with open(userDir, 'r') as f:
	# 		datastore = json.load(f)
	# 		for element in datastore["user"]:
	# 			if element["login"] == "True" and element["role"] == "Employee":
	# 				return True
	# 	return False
	#
	# def getEmployees(self, data) :
	# 	for e in data:
	# 		object = Employee(e['email'], e['password'])
	# 		addEmployee(object);
	#
	# def getUsers(self):
	# 	users = []
	# 	with open(userDir,"r") as json_file:
	# 		data = json.load(json_file)
	# 	for u in data['user']:
	# 		object = User(u['username'],u['email'],u['password'],u['name'],u['role'])
	# 		users.append(object)
	# 	return users
	#
	# def get_username(self):
	# 	with open(userDir, 'r') as f:
	# 		datastore = json.load(f)
	# 	for element in datastore["user"]:
	# 		if element["login"] == "True":
	# 			return element["username"]
	#
	# def get_user_email(self):
	# 	with open(userDir, 'r') as f:
	# 		datastore = json.load(f)
	# 		for element in datastore["user"]:
	# 			if element["login"] == "True":
	# 				return element["email"]

	def getDeliveredBlood(self) :
		deliveredBlood = []
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['blood']:
			if b['input_date'] == "":
				object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'], b['input_date'], b['test_status'], b['source'], b['id'],b['delivered_status'])
				deliveredBlood.append(object)
		return deliveredBlood

	def updateBloodStatus(self, blood, newStatus) :
		with open(bloodDir, 'r') as f:
			datastore = json.load(f)
			for element in datastore["blood"]:
				if element["id"] == blood.id:
					element['test_status'] = newStatus
					with open(bloodDir, 'w') as file:
						file.write(json.dumps(datastore, indent = 4))


	def updateInputDate(self, blood) :
		date = str(datetime.date(datetime.now()))
		with open(bloodDir, 'r') as f:
			datastore = json.load(f)
			for element in datastore["blood"]:
				if element["id"] == blood.id:
					element['input_date'] = date
					with open(bloodDir, 'w') as file:
						file.write(json.dumps(datastore, indent = 4))

	# def getTestedBlood(self) :
	# 	deliveredBlood = self.getDeliveredBlood()
	# 	testedBlood = []
	# 	for b in deliveredBlood:
	# 		if b.testStatus== "tested":
	# 			testedBlood.append(b)
	# 	return testedBlood
	#
	# def getNotTestedBlood(self) :
	# 	deliveredBlood = self.getDeliveredBlood()
	# 	notTestedBlood = []
	# 	for b in deliveredBlood:
	# 		if b.testStatus == "not-tested":
	# 			notTestedBlood.append(b)
	# 	return notTestedBlood


	# def getMedicalFacility(self, data) :
	# 	for m in data:
	# 		object = MedicalFacility(m['name'])
	# 		addMedicalFacility(object)

	def updateDeliveredStatus(self, mf_req, newStatus) :
		#remove the req and chg status of blood
		blood_id = mf_req.blood_list
		req_id = mf_req.id
		i = 0
		if newStatus == "yes":
			with open(bloodDir, 'r') as f:
				datastore = json.load(f)
				for element in datastore["blood"]:
					if (element["id"] in blood_id):
						datastore["blood"].remove(element)
						#element['delivered_status'] = newStatus
						with open(bloodDir, 'w') as file:
							file.write(json.dumps(datastore, indent = 4))
		with open(requestDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['request']:
			if b['id'] == req_id:
				b['status'] = newStatus
				with open(requestDir, 'w') as file:
					file.write(json.dumps(data, indent = 4))
	# check if request can be fulfilled
	def checkRequest(self,type,quantity,id):
		factoryBlood = BloodSystem().getFactoryBlood()
		count = 0
		today = date.today()
		datenow = today.strftime("%Y-%m-%d")
		list = []
		# get blood that matches the exact amount
		for n in factoryBlood:
			if (n.type == type and n.quantity == quantity and n.id not in id
			and n.expiryDate > datenow and n.deliveredStatus != "yes"):
				id.append(n.id)
				list.append(n)
		# get the blood with latest expiry date
		newlist = []
		if len(list) > 0:
			min = list[0].expiryDate
			newlist.append(list[0].id)

		for n in list:
			if n.expiryDate < min:
				newlist.clear()
				min = n.expiryDate
				newlist.append(n.id)
		if len(list) > 0:
			return "yes",id,newlist

		# calculate how many packets needed
		req_qtt = quantity
		for n in factoryBlood:
				if (n.type == type and req_qtt >= n.quantity and n.id not in id
					and req_qtt > 0 and n.expiryDate > datenow and n.deliveredStatus != "yes"):
					count = count + 1;
					req_qtt = req_qtt - n.quantity
					id.append(n.id)
					list.append(n.id)
		if (count > 0 and req_qtt == 0):
			return "yes",id,list
		return "no",id,list
	#
	# def getMedicalFacilityRequests(self) :
	# 	mf_requests = []
	# 	id = []
	# 	with open(requestDir, "r") as json_file:
	# 		data = json.load(json_file)
	# 	for b in data['request']:
	# 		if (b['status'] == ""):
	# 			fulfil,id,list = self.checkRequest(b['type'], b['quantity'],id)
	# 			print (list)
	# 			object = Request(b['medical_facility'], b['type'], b['quantity'], fulfil,list,b['id'])
	# 			mf_requests.append(object)
	# 	return mf_requests
	#
	# # def sortRequests(self, object) :
	# 	for m in self._medicalFacilities:
	# 		if (m.getName() == object.getName()) :
	# 			m.addRequest(object)
	# 			return;

	# def calculateFactoryBloodType(self, bloodType) :
	# 	sum = 0;
	# 	factoryBlood = BloodSystem().getFactoryBlood()
	# 	for b in factoryBlood:
	# 	    if (bloodType == b.type) :
	# # 	        sum += int(b.quantity)
	# # 	return sum
	#
	# def findLowBloodTypes(self) :
	# 	blood = calculateAllBloodType()
	# 	lowBlood = {}
	# 	for k in blood.keys():
	# 	    if blood[k] < 500:
	# 	        lowBlood[k] = blood[k]
	# 	return lowBlood
	#
	# def makeRequest(self, bloodtype, quantity, sent) :
	# 	object = Requests(sent, bloodtype, quantity)
	# 	if (sent == 'VampireCompany') :
	# 		addVampireRequests(object)
	# 	else:
	# 		sortRequests(object)

	# def searchBloodType(self, bloodtype) :
	# 	results = []
	# 	factoryBlood = BloodSystem().getFactoryBlood()
	# 	for blood in factoryBlood:
	# 	    if blood.type == bloodtype:
	# 	        results.append(blood)
	# 	return results
	#
	# def searchBloodExpiry(self, start, end) :
	# 	startYear = start[:4]
	# 	startMonth = start[5:7]
	# 	startDay = start[8:]
	# 	endYear = end[:4]
	# 	endMonth = end[5:7]
	# 	endDay = end[8:]
	# 	newStart = startYear + startMonth + startDay
	# 	newStart = int(newStart)
	# 	newEnd = endYear + endMonth + endDay
	# 	newEnd = int(newEnd)
	# 	results = []
	# 	factoryBlood =  BloodSystem().getFactoryBlood()
	# 	for blood in factoryBlood:
	# 	    year = blood.expiryDate[:4]
	# 	    month = blood.expiryDate[5:7]
	# 	    day = blood.expiryDate[8:]
	# 	    date = year + month + day
	# 	    date = int(date)
	# 	    if (date >= newStart and date <= newEnd):
	# 	        results.append(blood)
	# 	return results
	#
	# def searchBloodVolume(self, minimum, maximum) :
	#     minimum = int(minimum)
	#     maximum = int(maximum)
	#     results = {}
	#     for b in self.bloodTypes:
	#         sum = self.calculateFactoryBloodType(b)
	#         if ( sum >= minimum and sum <= maximum):
	#             results[b] = sum
	#     return results
