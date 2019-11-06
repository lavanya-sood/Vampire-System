import json
from datetime import datetime
#from .employee import Employee
#from .blood import Blood
#from .deliveredBlood import DeliveredBlood
#from .medicalFacility import MedicalFacility
#from .requests import Requests
from lib.Blood import Blood
import json
import os
import ast
import operator

currDir = os.getcwd()
bloodDir = currDir + "/lib/textfiles/blood.json"
requestDir = currDir + "/lib/textfiles/request.json"
employeeDir = currDir + "/lib/textfiles/employees.json"
medicalFacilityDir = currDir + "/lib/textfiles/medicalFacility.json"

class VampireSystem:
	employees = []
	deliveredBlood = []
	factoryBlood = []
	validBlood = []
	expiredBlood = []
	medicalFacilities = []
	vampireRequests = []
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

	def loadJson(self): #split into get respective functions
		with open(employeeDir, "r") as json_file:
			data = json.load(json_file)
			getEmployees(data['employee'])
		with open('blood.json') as json_file:
			data = json.load(json_file)
			getBlood(data['blood'])
		with open('medicalFacility.json') as json_file:
			data = json.load(json_file)
			getMedicalFacility(data['facility'])
		with open('requests.json') as json_file:
			data = json.load(json_file)
			getRequests(data['requests'])


	def addEmployee(self, object):
		employees.append(object)

	def addDeliveredBlood(self, object):
		deliveredBlood.append(object)


	def addFactoryBlood(self, object):
		factoryBlood.append(object)


	def addValidBlood(self, object) :
		validBlood.append(object)


	def addExpiryBlood(self, object) :
		expiredBlood.append(object)


	def addMedicalFacilities(self, object) :
		medicalFacilities.append(object)


	def addVampireRequests(self, object) :
		vampireRequests.append(object)


	def getEmployees(self, data) :
		for e in data:
			object = Employee(e['email'], e['password'])
			addEmployee(object);


	def getDeliveredBlood(self) :
		deliveredBlood = []
		with open(bloodDir, "r") as json_file:
			data = json.load(json_file)
		for b in data['blood']:
			if b['test_status'] != "added":
				object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'], b['input_date'], b['test_status'], b['source'], b['id'])
				deliveredBlood.append(object)
		return deliveredBlood

	def updateBloodStatus(self, blood, newStatus):
		with open(bloodDir, 'r') as f:
			datastore = json.load(f)
			for element in datastore["blood"]:
				if element["id"] == blood.id:
					element['test_status'] = newStatus
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
			if b['test_status'] == "added":
					object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'], b['input_date'], b['test_status'], b['source'], b['id'])
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


	def getRequests(self, data) :
		for r in data:
			object = Requests(m['name'], m['type'], m['quantity'])
			if (m['name'] == 'VampireCompany') :
				addVampireRequests(object)
			else:
				sortRequests(object)



	def sortRequests(self, object) :
		for m in self._medicalFacilities:
			if (m.getName() == object.getName()) :
				m.addRequest(object)
				return;


	def resetBlood(self) :
		validBlood = []
		expiredBlood = []
		sortBlood()

	def getDate(self, date) :
	    return datetime.datetime.strptime(date, "%d/%m/%Y").date()


	def sortBlood(self) :
		for b in factoryBlood:
			expiry = getDate(b.getExpiry())
			curr = datetime.date(datetime.now())
			if (curr >= expiry) :
				addExpiredBlood(b)
			else :
				addValidBlood(b)


	def getBloodTypes(self) :
	    return {'A+': 0, 'A-': 0, 'AB+': 0, 'AB-': 0, 'B+': 0, 'B-': 0, 'O+': 0, 'O-': 0}

	#def calculateAllBloodType(self) :
	#	blood = getBloodTypes()
	#	for k in blood.keys():
    #        blood[k] = calculateFactoryBloodType(k)
	#	return blood

	def calculateFactoryBloodType(self, bloodType) :
		sum = 0;
		for b in factoryBlood:
		    if (bloodType == b.getType()) :
		        sum += b.getQuantity()

		return sum


	def findLowBloodTypes(self) :
		blood = calculateAllBloodType()
		lowBlood = {}
		for k in blood.keys():
		    if blood[k] < 500:
		        lowBlood[k] = blood[k]
		return lowBlood


	def calculateValidBloodType(self, bloodType) :
		sum = 0;
		for b in validBlood:
		    if (bloodType == b.getType()) :
		        sum += b.getQuantity()

		return sum;


	def makeRequest(self, bloodtype, quantity, sent) :
		object = Requests(sent, bloodtype, quantity)
		if (sent == 'VampireCompany') :
			addVampireRequests(object)
		else:
			sortRequests(object)

	def getOldestFactoryBlood(self, bloodList) :
		minimum = getDate(bloodList['added'])
		minIndex = 0
		i = 0
		for b in bloodList:
		    date = getDate(b.getAdded())
		    if (date < minimum) :
		        minimum = date
		        minIndex = i
		    i = i + 1
		return minIndex


    #def getOldestExpiry(self, bloodList):
    #    minimum = getDate(bloodList['expiry'])
	#	minIndex = 0
	#	i = 0
	#	for b in bloodList:
	#	    date = getDate(b.getExpiry())
	#	    if (date < minimum) :
	#	        minimum = date
	#	        minIndex = i

	#	    i = i + 1

	#	return minIndex


	#def sortFactoryBloodByAdded(self) :
	 #   sortedList = []
	 #   bloodList = self._factoryBlood
#		for (i = 0; i < len(self._factoryBlood); i++):
#		    oldestIndex = getOldestFactoryBlood(bloodList)
#		    sortedList.append(self._factoryBlood[oldestIndex])
#		    del bloodList[oldestIndex]
#
#		return sortedList


	#def sortFactoryBloodByExpiry(self) :
	#	sortedList = []
	#	bloodList = self._factoryBlood
	#	for (i = 0; i < len(self._factoryBlood); i++) :
	#	    oldestIndex = getOldestExpiry(bloodList)
	#	    sortedList.append(self._factoryBlood[oldestIndex])
	#	    del bloodList[oldestIndex]
#
#		return sortedList


	#def sortFactoryBloodTypeByQuantity(self) :
    #    '''blood = calculateAllBloodType()'''
    #    pass


	def removeFactoryBlood(self) :
		pass


	def removeExpiredBlood(self) :
		pass


	def removeValidBlood(self) :
		pass


	def removeMedicalFacility(self, name) :
		pass


	def searchBloodType(self, bloodtype) :
		pass


	def searchBloodExpiry(self, start, end) :
		pass


	def searchBloodVolume(self, min, max) :
		pass


	def getEmployees(self) :
	    return employees


	def getValidBlood(self) :
	    return validBlood


    #def getExpiredBlood(self) :
	#	return self._expiredBlood


    #def getMedicalFacilities(self):
    #    return self._medicalFacilities


    #def getVampireRequests(self) :
    #    return self._vampireRequests
