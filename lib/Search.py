class Search():
    
    def __init__(self, factoryBlood):
        self._factoryBlood = factoryBlood
    
    def sumBloodQuantity(self, bloodType):
	    amount = 0
	    i = 0
	    while i < len(bloodType):
	        amount += bloodType[i].quantity
	        i += 1
	    return amount
	
    def sortBloodExpiry(self, blood):
        i = len(blood) - 1
        while i > 0:
            j = 0
            while j < i:
                startYear = blood[j].expiryDate[:4]
                startMonth = blood[j].expiryDate[5:7]
                startDay = blood[j].expiryDate[8:]
                endYear = blood[j + 1].expiryDate[:4]
                endMonth = blood[j + 1].expiryDate[5:7]
                endDay = blood[j + 1].expiryDate[8:]
                newStart = startYear + startMonth + startDay
                newStart = int(newStart)
                newEnd = endYear + endMonth + endDay
                newEnd = int(newEnd)
                if newStart > newEnd:
                    blood[j], blood[j+1] = blood[j+1], blood[j]
                j += 1
            i -= 1

    def sortBloodVolume(self, blood):
        sortedDict = sorted(blood, key=blood.get)

    def findLowerLimitExpiry(self, blood, start):
        minimum = len(blood)
        i = 0
        while i < len(blood):
            startYear = blood[i].expiryDate[:4]
            startMonth = blood[i].expiryDate[5:7]
            startDay = blood[i].expiryDate[8:]
            newStart = startYear + startMonth + startDay
            newStart = int(newStart)
            if newStart >= start:
                minimum = i
                break
            i += 1
        return minimum

    def findLowerLimitVolume(self, blood, start):
        minimum = len(blood)
        i = 0
        for key, value in blood.items():
            if value >= int(start):
                minimum = i
                break
            i += 1
        return minimum

    def findUpperLimitExpiry(self, blood, end):
        maximum = len(blood)
        i = 0
        while i < len(blood):
            endYear = blood[i].expiryDate[:4]
            endMonth = blood[i].expiryDate[5:7]
            endDay = blood[i].expiryDate[8:]
            newEnd = endYear + endMonth + endDay
            newEnd = int(newEnd)
            if newEnd > end:
                maximum = i
                break
            i += 1
        return maximum

    def findUpperLimitVolume(self, blood, end):
        maximum = len(blood)
        i = 0
        for key, value in blood.items():
            if value > int(end):
                maximum = i
                break
            i += 1
        return maximum

    def searchBloodType(self, bloodtype):
        result = []
        i = 0
        while i < len(self._factoryBlood):
            if self._factoryBlood[i].type == bloodtype:
                result.append(self._factoryBlood[i])
            i += 1
        return result
        

    def searchBloodExpiry(self, start, end):
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
        factoryBlood = self._factoryBlood
        self.sortBloodExpiry(factoryBlood)
        minimum = self.findLowerLimitExpiry(factoryBlood, newStart)
        maximum = self.findUpperLimitExpiry(factoryBlood, newEnd)
        return factoryBlood[minimum:maximum]

    def searchBloodVolume(self, start, end):
        try: 
            minimum = int(start)
            maximum = int(end)
        except ValueError:
            return {}
        A = self.searchBloodType("A")
        B = self.searchBloodType("B")
        AB = self.searchBloodType("AB")
        O = self.searchBloodType("O")
        sumA = self.sumBloodQuantity(A)
        sumB = self.sumBloodQuantity(B)
        sumAB = self.sumBloodQuantity(AB)
        sumO = self.sumBloodQuantity(O)
        bloodTypeQuantity = {}
        bloodTypeQuantity["A"] = sumA
        bloodTypeQuantity["B"] = sumB
        bloodTypeQuantity["AB"] = sumAB
        bloodTypeQuantity["O"] = sumO
        self.sortBloodVolume(bloodTypeQuantity)
        minimum = self.findLowerLimitVolume(bloodTypeQuantity, start)
        maximum = self.findUpperLimitVolume(bloodTypeQuantity, end)
        return self.sliceDict(bloodTypeQuantity, minimum, maximum)
        
    def sliceDict(seld, blood, minimum, maximum):
        i = 0
        result = {}
        for key, value in blood.items():
            if i >= minimum and i <maximum:
                result[key] = value
            i += 1
        return result

