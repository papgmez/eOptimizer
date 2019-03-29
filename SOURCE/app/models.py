#!/usr/bin/python3

from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from server import db

class Users(db.Model):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    home = relationship("Homes", uselist=False, backref="Users")

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}, name={self.name} {self.lastname}, email={self.email}, home_id={self.home.id}>'.format(self=self))

class Homes(db.Model):
    __tablename__ = "homes"
    id = Column(Integer, primary_key=True)
    city_code = Column(String(100), nullable=False)
    pv_modules = Column(Integer, nullable=False)
    amortization_years_pv = Column(Integer, nullable=False)
    amortization_years_bat = Column(Integer, nullable=False)
    UserId = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    user = relationship("Users", backref="Homes")

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}, city={self.city_code}, pv_modules={self.pv_modules}, user_id={self.UserId}>'.format(self=self))
