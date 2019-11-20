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
	#blood =

	def __init__(self,blood):
		self._blood = blood

	def getDeliveredBlood(self) :
		deliveredBlood = []
		for b in self._blood:
			if b.inputDate == "":
				deliveredBlood.append(b)
		return deliveredBlood

	def updateBloodStatus(self, blood, newStatus) :
		with open(bloodDir, 'r') as f:
			datastore = json.load(f)
		for element in datastore["blood"]:
			if element["id"] == blood.id:
				element['test_status'] = newStatus
				with open(bloodDir, 'w') as file:
					file.write(json.dumps(datastore, indent = 4))
				break


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


	def getMedicalFacilityRequests(self) :
		mf_requests = []
		id = []
		with open(requestDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['request']:
			if (b['status'] == ""):
				fulfil,id,list = BloodSystem().checkRequest(b['type'], b['quantity'],id)
				print (list)
				object = Request(b['medical_facility'], b['type'], b['quantity'], fulfil,list,b['id'])
				mf_requests.append(object)
		return mf_requests
