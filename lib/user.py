from flask_login import UserMixin
from abc import ABC, abstractmethod
import json

class User(UserMixin,ABC):

        def __init__(self, email, password, name, role):
            self._id = self._generate_id()
            self.username = username
            self._email = email
            self._password = password
            self._name = name
            self._role = role
            self._requests = []

        @property
        def email(self):
            return self._email

        @property
        def password(self):
            return self._password

        @property
        def name(self):
            return self._name

        @property
        def role(self):
            return self._role

        @property
        def is_authenticated(self):
            return True

        @property
        def is_active(self):
            return True

        @property
        def is_anonymous(self):
            return False

        def get_id(self):
            """Required by Flask-login"""
            return str(self._id)

        def _generate_id(self):
            User.__id += 1
            return User.__id

        def add_requests(self,request):
            self._request.append(request)

        @classmethod
        def set_id(cls, id):
            cls.__id = id

        def validate_password(self, password):
            return self._password == password

        def as_list():
            pass
