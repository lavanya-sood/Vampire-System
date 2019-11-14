class Search():
    
    def __init__(self, factoryBlood):
        self._factoryBlood = factoryBlood

    def searchBloodType(self, bloodtype):
	    return self.getBloodType(bloodtype)
	    
    def getBloodType(self, bloodtype):
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
        return self.getBloodExpiry(newStart, newEnd)
        
    def getBloodExpiry(self, minimum, maximum):
        result = []
        i = 0
        while i < len(self._factoryBlood):
            year = self._factoryBlood[i].expiryDate[:4]
            month = self._factoryBlood[i].expiryDate[5:7]
            day = self._factoryBlood[i].expiryDate[8:]
            date = year + month + day
            date = int(date)
            if date >= minimum and date <= maximum: 
                result.append(self._factoryBlood[i])
            i += 1
        return result

    def searchBloodVolume(self, minimum, maximum):
        try: 
            minimum = int(minimum)
            maximum = int(maximum)
        except ValueError:
            return {}
        A = self.getBloodType("A")
        B = self.getBloodType("B")
        AB = self.getBloodType("AB")
        O = self.getBloodType("O")
        sumA = self.sumBloodQuantity(A)
        sumB = self.sumBloodQuantity(B)
        sumAB = self.sumBloodQuantity(AB)
        sumO = self.sumBloodQuantity(O)
        bloodTypeQuantity = {}
        bloodTypeQuantity["A"] = sumA
        bloodTypeQuantity["B"] = sumB
        bloodTypeQuantity["AB"] = sumAB
        bloodTypeQuantity["O"] = sumO
        return self.getBloodVolume(bloodTypeQuantity, minimum, maximum)

    def sumBloodQuantity(self, bloodType):
	    amount = 0
	    i = 0
	    while i < len(bloodType):
	        amount += bloodType[i].quantity
	        i += 1
	    return amount
        
    def getBloodVolume(self, blood, minimum, maximum):
        result = {}
        for key, value in blood.items():
            if value >= minimum and value <= maximum:
                result[key] = value
        return result

