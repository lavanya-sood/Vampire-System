class Blood():

        def __init__(self, donor_name, type, quantity,expiry_date,input_date,test_status,source, id,delivered_status):
            self._donorName = donor_name
            self._type = type
            self._quantity = quantity
            self._expiryDate = expiry_date
            self._inputDate = input_date
            self._testStatus = test_status
            self._source = source
            self._id = id
            self._delivered_status = delivered_status

        @property
        def donorName(self):
            return self._donorName

        def setInputDate(self, time):
            self._inputDate = time

        @property
        def id(self):
            return self._id

        @property
        def source(self):
            return self._source
        @property
        def type(self):
            return self._type

        @property
        def quantity(self):
            return self._quantity

        @property
        def expiryDate(self):
            return self._expiryDate

        @property
        def inputDate(self):
            return self._inputDate

        @property
        def testStatus(self):
            return self._testStatus

        def setTestStatus(self, str):
            self._test_status = str

        @property
        def deliveredStatus(self):
            return self._delivered_status

        def setDeliveredStatus(self, str):
            self._delivered_status = str
