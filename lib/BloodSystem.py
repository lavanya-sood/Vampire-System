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

class BloodSystem():
	bloodTypes = ["A", "B", "AB", "O"]

	def getFactoryBlood(self):
		factoryBlood = []
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['blood']:
			if b['input_date'] != "":
				object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'],b['input_date'],b['test_status'],b['source'],b['id'],b['delivered_status'])
				factoryBlood.append(object)
		return factoryBlood

	# def updateDeliveredStatus(self,id):
	# 	with open(bloodDir, "r") as json_file:
	# 		data = json.load(json_file)
	# 	for b in data['blood']:
	# 		if b['id'] == id:
	# 			b['delivered_status'] = "yes"

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

	def getExpiredBlood(self):
		expiredBlood = []
		# with open(bloodDir, "r") as json_file:
		# 	data = json.load(json_file)
		data = self.getFactoryBlood()
		now = datetime.now()
		for b in data:
			d = datetime.strptime(b.expiryDate, "%Y-%m-%d")
			if d < now:
				expiredBlood.append(b)
		return expiredBlood

	def getBloodQuantitybyType(self): # may find a better algorithm for sorting
		blood = []
		for type in self.bloodTypes:
			blood.append(dict(type=type, quantity=self.getQuantity(type)))
		return blood


	def deletefromBloodInventory(self, index):
		with open(bloodDir, 'r') as f:
			datastore = json.load(f)
			del datastore["blood"][index]

			with open(bloodDir, 'w') as file:
				file.write(json.dumps(datastore, indent = 4))
