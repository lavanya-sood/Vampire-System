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


	def check_user(self, email, password):
		user = ""
		with open(userDir, 'r') as f:
			datastore = json.load(f)
		for element in datastore["user"]:
			if element["email"] == email and element["password"] == password:
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

	def getEmployees(self, data) :
		for e in data:
			object = Employee(e['email'], e['password'])
			addEmployee(object);

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

	def getDeliveredBlood(self) :
		deliveredBlood = []
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['blood']:
			if b['input_date'] == "":
				object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'], b['input_date'], b['test_status'], b['source'], b['id'])
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

	def getTestedBlood(self) :
		deliveredBlood = self.getDeliveredBlood()
		testedBlood = []
		for b in deliveredBlood:
			if b.testStatus== "tested":
				testedBlood.append(b)
		return testedBlood

	def getNotTestedBlood(self) :
		deliveredBlood = self.getDeliveredBlood()
		notTestedBlood = []
		for b in deliveredBlood:
			if b.testStatus == "not-tested":
				notTestedBlood.append(b)
		return notTestedBlood

	def getFactoryBlood(self) :
		factoryBlood = []
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['blood']:
			if b['input_date'] != "":
				object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'],
				b['input_date'],b['test_status'],b['source'],b['id'])
				factoryBlood.append(object)
		return factoryBlood

	def getLowBlood(self):
		dict = {}
		for type in self.bloodTypes:
			if (int(self.getQuantity(type)) < 3000):
				dict[type] = self.getQuantity(type)
		return dict

	def getNormalBlood(self):
		dict = {}
		for type in self.bloodTypes:
			if (int(self.getQuantity(type)) >= 3000):
				dict[type] = self.getQuantity(type)
		return dict

	def getQuantity(self, type):
		sum = 0
		blood = self.getFactoryBlood();
		for b in blood:
			if b.type == type:
				sum = sum + int(b.quantity)
		return sum

	def getMedicalFacility(self, data) :
		for m in data:
			object = MedicalFacility(m['name'])
			addMedicalFacility(object)

	# check if request can be fulfilled
	def checkRequest(self,type,quantity,id):
		factoryBlood = self.getFactoryBlood()
		for n in factoryBlood:
			if (n.type == type and n.quantity >= quantity and n.id not in id):
				id.append(n.id)
				return "yes",id
		return "no",id

	def getMedicalFacilityRequests(self) :
		mf_requests = []
		id = []
		with open(requestDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['request']:
			fulfil,id = self.checkRequest(b['type'], b['quantity'],id)
			object = Request(b['medical_facility'], b['type'], b['quantity'], fulfil)
			mf_requests.append(object)
			print (id)
		return mf_requests

	def sortRequests(self, object) :
		for m in self._medicalFacilities:
			if (m.getName() == object.getName()) :
				m.addRequest(object)
				return;

	def calculateFactoryBloodType(self, bloodType) :
		sum = 0;
		factoryBlood = self.getFactoryBlood()
		for b in factoryBlood:
		    if (bloodType == b.type) :
		        sum += int(b.quantity)
		return sum

	def findLowBloodTypes(self) :
		blood = calculateAllBloodType()
		lowBlood = {}
		for k in blood.keys():
		    if blood[k] < 500:
		        lowBlood[k] = blood[k]
		return lowBlood

	def makeRequest(self, bloodtype, quantity, sent) :
		object = Requests(sent, bloodtype, quantity)
		if (sent == 'VampireCompany') :
			addVampireRequests(object)
		else:
			sortRequests(object)

	def searchBloodType(self, bloodtype) :
		results = []
		factoryBlood = self.getFactoryBlood()
		for blood in factoryBlood:
		    if blood.type == bloodtype:
		        results.append(blood)
		return results

	def searchBloodExpiry(self, start, end) :
		startYear = start[:4]
		startMonth = start[5:7]
		startDay = start[8:]
		endYear = end[:4]
		endMonth = end[5:7]
		endDay = end[8:]
		newStart = startYear + startMonth + startDay
		newStart = int(newStart) 
		newEnd = endYear + endMonth + endDay
		newEnd = int(newEnd) 
		results = []
		factoryBlood = self.getFactoryBlood()
		for blood in factoryBlood:
		    year = blood.expiryDate[:4]
		    month = blood.expiryDate[5:7]
		    day = blood.expiryDate[8:]
		    date = year + month + day
		    date = int(date)
		    if (date >= newStart and date <= newEnd):
		        results.append(blood)
		return results

	def searchBloodVolume(self, minimum, maximum) :
	    minimum = int(minimum)
	    maximum = int(maximum)
	    results = {}
	    for b in self.bloodTypes:
	        sum = self.calculateFactoryBloodType(b)
	        if ( sum >= minimum and sum <= maximum):
	            results[b] = sum
	    return results

	def getExpiredBlood(self):
		expiredBlood = []
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		now = datetime.now()	
		for b in data['blood']:
			d = datetime.strptime(b["expiry_date"], "%Y-%m-%d")
			if d < now:
				expiredBlood.append(b)	
		return expiredBlood

	def sortBloodbyType(self): # may find a better algorithm for sorting
		blood = []
		typeA = []
		typeB = []
		typeAB = []
		typeO = []
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['blood']:	
			if b["type"] == "A":
				typeA.append(b)
			elif b["type"] == "B":	
				typeB.append(b)
			elif b["type"] == "AB":	
				typeAB.append(b)	
			elif b["type"] == "O":	
				typeO.append(b)	
		return typeA + typeB + typeAB + typeO	

	def sortBloodbyQuantity(self):
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		blood = data['blood']	
		n = len(blood)
		for i in range(n) :
			for j in range(0, n-i-1):
				if blood[j]["quantity"] > blood[j+1]["quantity"] :
					blood[j], blood[j+1] = blood[j+1], blood[j]
		return blood


	def sortBloodbyExpiryDate(self):
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		blood = data['blood']	
		n = len(blood)
		for i in range(n) :
			for j in range(0, n-i-1):
				if blood[j]["expiry_date"] > blood[j+1]["expiry_date"] :
					blood[j], blood[j+1] = blood[j+1], blood[j]
		return blood	

	def sortBloodbyAddedDate(self):
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		blood = data['blood']	
		n = len(blood)
		for i in range(n) :
			for j in range(0, n-i-1):
				if blood[j]["input_date"] > blood[j+1]["input_date"] :
					blood[j], blood[j+1] = blood[j+1], blood[j]
		return blood

	def deletefromBloodInventory(self, index):
		with open(bloodDir, 'r') as f:
			datastore = json.load(f)
			del datastore["blood"][index]
			
			with open(bloodDir, 'w') as file:
				file.write(json.dumps(datastore, indent = 4))
