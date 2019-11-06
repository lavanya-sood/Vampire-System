class Request():

    def __init__(self, medical_facility, blood_type, quantity,fulfillable):
        self._medical_facility = medical_facility
        self._blood_type = blood_type
        self._quantity = quantity
        self._fulfillable = fulfillable

    def setFulfilStatus(self, new):
        self._fulfillable = new

    @property
    def medical_facility(self):
        return self._medical_facility

    @property
    def blood_type(self):
        return self._blood_type

    @property
    def quantity(self):
        return self._quantity

    @property
    def fulfillable(self):
        return self._fulfillable
