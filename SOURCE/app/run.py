#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from config import prod_config
from models import Base

# Deploy to production
manager = Manager(app)
app.config.from_object(prod_config)
db = SQLAlchemy(app)
Base.metadata.create_all(bind=db.engine)

if __name__ == '__main__':
    manager.run()
