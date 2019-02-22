#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.types import DateTime, Integer, String

from boulet_bot.config.db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    boulet = Column(Integer, nullable=False)
    boulet_date = Column(DateTime, nullable=False)
    old_name = Column(String, nullable=True)

    UniqueConstraint('name', name='name_uc')

    def __init__(self, name):
        self.name = name
        self.boulet = 1
        self.boulet_date = datetime.datetime.now()
