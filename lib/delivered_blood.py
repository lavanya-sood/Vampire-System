class delivered_blood(object):
	def __init__(type, expiryDate, quantity, testStatus, donorName, inputDate):
        self._type = type
        self._expiryDate = expiryDate
        self._quantity= quantity
        self._source= source
        self._testStatus = testStatus
        self._donorName = donorName
        self._inputDate = inputDate



	@property
	def tested_blood(self):
		return self._tested_blood

	@property
	def untested_blood(self):
		return self._untested_blood

	@property
	def yet_inputed(self):
		return self._yet_inputed



	def add_tested_blood(Blood blood):
		this._tested_blood.append(blood)

	def add_untested_blood(Blood blood):
		this._untested_blood.append(blood)

	def add_yet_inputed(Blood blood):
		this._yet_inputed.append(blood)

	def clear_tested_blood_list():
		this._tested_blood.clear()

	def clear_untested_blood_list():
		this._untested_blood.clear()

	def clear_yet_inputed_list():
		this._yet_inputed.clear()
