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
	blood = []


	def __init__(self,blood):
		self._blood = blood

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

	def getMedicalFacilityRequests(self) :
		mf_requests = []
		id = []
		with open(requestDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['request']:
			if (b['status'] == ""):
				fulfil,id,list = self.checkRequest(b['type'], b['quantity'],id)
				print (list)
				object = Request(b['medical_facility'], b['type'], b['quantity'], fulfil,list,b['id'])
				mf_requests.append(object)
		return mf_requests
