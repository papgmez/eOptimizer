#!/usr/bin/python3

from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Users(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128))
    home = relationship("Homes", uselist=False, backref="Users")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}, name= {self.name} {self.lastname}, email= {self.email}>'.format(self=self))

class Homes(Base):
    __tablename__ = "homes"
    id = Column(Integer, primary_key=True)
    city_code = Column(String(100), nullable=False)
    pv_modules = Column(Integer, nullable=False)
    amortization_years_pv = Column(Integer, nullable=False)
    amortization_years_bat = Column(Integer, nullable=False)
    UserId = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    user = relationship("Users", backref="Homes")

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}, city= {self.city_code}, pv_modules= {self.pv_modules}, ownerId= {self.UserId}>'.format(self=self))
