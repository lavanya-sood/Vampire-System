class Blood():

        def __init__(self, donor_name, type, quantity,expiry_date,input_date,test_status,source):
            self._donor_name = donor_name
            self._type = type
            self._quantity = quantity
            self._expiry_date = expiry_date
            self._input_date = input_date
            self._test_status = test_status
            self._source = source

        @property
        def donor_name(self):
            return self._donor_name

        @property
        def type(self):
            return self._type

        @property
        def quantity(self):
            return self._quantity

        @property
        def expiry_date(self):
            return self._expiry_date

        @property
        def input_date(self):
            return self._input_date

        @property
        def test_status(self):
            return self._test_status
