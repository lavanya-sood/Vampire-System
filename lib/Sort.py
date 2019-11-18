class Sort():

	def __init__(self, factoryBlood):
		self._factoryBlood = factoryBlood

	def sortBloodbyQuantity(self):
		blood = self._factoryBlood
		n = len(blood)
		for i in range(n) :
			for j in range(0, n-i-1):
				if blood[j].quantity > blood[j+1].quantity :
					blood[j], blood[j+1] = blood[j+1], blood[j]
		return blood


	def sortBloodbyExpiryDate(self):
		blood = self._factoryBlood
		n = len(blood)
		for i in range(n) :
			for j in range(0, n-i-1):
				if blood[j].expiryDate > blood[j+1].expiryDate :
					blood[j], blood[j+1] = blood[j+1], blood[j]
		return blood

	def sortBloodbyAddedDate(self):
		blood = self._factoryBlood
		n = len(blood)
		for i in range(n) :
			for j in range(0, n-i-1):
				if blood[j].inputDate > blood[j+1].inputDate :
					blood[j], blood[j+1] = blood[j+1], blood[j]
		return blood