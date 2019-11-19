import json
from datetime import datetime
from lib.user import User
from lib.Blood import Blood
from lib.Request import Request
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

class BloodSystem():
    requestSent = {}
    bloodTypes = ["A", "B", "AB", "O"]
    for type in bloodTypes:
        requestSent[type] = False

    def getRequestSent(self):
        return self.requestSent

    def updateRequestSent(self, type):
        self.requestSent[type] = True
        return self.requestSent

    def getFactoryBlood(self):
        factoryBlood = []
        with open(bloodDir, "r") as json_file:
            data = json.load(json_file)
        for b in data['blood']:
            if b['input_date'] != "":
                object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'],b['input_date'],b['test_status'],b['source'],b['id'],b['delivered_status'])
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

    def getBloodQuantitybyType(self): # may find a better algorithm for sorting
        blood = []
        for type in self.bloodTypes:
            blood.append(dict(type=type, quantity=self.getQuantity(type)))
        return blood


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
        for i in range(n):
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
