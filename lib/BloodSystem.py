import json
from datetime import datetime
from lib.user import User
from lib.Blood import Blood
from lib.Request import Request
from lib.Search import Search
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

    #load blood data and only retrieve blood with status 'added'
    def getFactoryBlood(self):
        factoryBlood = []
        with open(bloodDir, "r") as json_file:
            data = json.load(json_file)
        for b in data['blood']:
            if b['input_date'] != "":
                object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'],b['input_date'],b['test_status'],b['source'],b['id'],b['delivered_status'])
                factoryBlood.append(object)
        return factoryBlood

    #load blood data and only retrieve blood with status not being 'added'
    def  retrieveBloodAgain(self):
        deliveredBlood = []
        with open(bloodDir, "r") as json_file:
            data = json.load(json_file)
        for b in data['blood']:
            if b['input_date'] == "":
                object = Blood(b['donor_name'], b['type'], b['quantity'], b['expiry_date'], b['input_date'], b['test_status'], b['source'], b['id'],b['delivered_status'])
                deliveredBlood.append(object)
        return deliveredBlood

    #create and return a dict matching each blood type to their quantity using search
    def getAllQuantity(self):
        blood = self.getFactoryBlood()
        search = Search(blood)
        A = search.searchBloodType("A")
        B = search.searchBloodType("B")
        AB = search.searchBloodType("AB")
        O = search.searchBloodType("O")
        sumA = search.sumBloodQuantity(A)
        sumB = search.sumBloodQuantity(B)
        sumAB = search.sumBloodQuantity(AB)
        sumO = search.sumBloodQuantity(O)
        bloodTypeQuantity = {}
        bloodTypeQuantity["A"] = sumA
        bloodTypeQuantity["B"] = sumB
        bloodTypeQuantity["AB"] = sumAB
        bloodTypeQuantity["O"] = sumO
        return bloodTypeQuantity

    #get quantity for one particular blood type
    def getQuantity(self, type):
        sum = 0
        blood = self.getFactoryBlood();
        for b in blood:
            if b.type == type:
                sum = sum + int(b.quantity)
        return sum

    #create and return a dictionary of blood types and quantities that have below 1000ml left
    def getLowBlood(self,blood):
        low = {}
        for type in self.bloodTypes:
            if(self.hasLowBlood(blood, 1000, type)):
                low[type] = blood[type]
        return low

    #create and return a dictionary of blood types and quantities that have over 1000ml left
    def getNormalBlood(self,blood):
        low = {}
        for type in self.bloodTypes:
            if(self.hasLowBlood(blood, 1000, type) == False):
                low[type] = blood[type]
        return low

    #returns boolean and checks if given blood type is below 1000ml limit
    def hasLowBlood(self, blood, val, key):
        if (blood[key] < val):
                return True
        return False

    def getExpiredBlood(self):
        blood = self.getFactoryBlood()
        expiredBlood = []
        now = datetime.now()
        for b in blood:
            d = datetime.strptime(b.expiryDate, "%Y-%m-%d")
            if d < now:
                expiredBlood.append(b)
        return expiredBlood

    def getBloodQuantitybyType(self): # may find a better algorithm for sorting
        blood = []
        for type in self.bloodTypes:
            blood.append(dict(type=type, quantity=self.getQuantity(type)))
        return blood

    def deletefromBloodInventory(self, id):
        i = 0;
        with open(bloodDir, 'r') as f:
            datastore = json.load(f)
            for b in datastore['blood']:
                if b["id"] == id:
                    del datastore["blood"][i]
                    with open(bloodDir, 'w') as file:
                        file.write(json.dumps(datastore, indent = 4))
                i = i + 1

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
