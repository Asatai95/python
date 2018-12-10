from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

import os, sys
sys.path.append(os.getcwd())

from config.settings import Base, ENGINE

class UserAuth(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'auth_user'
    id = Column('id', Integer, primary_key = True)
    username = Column('username', String(150))
    email = Column('email', String(150))
    password = Column('password', String(150))
    first_name = Column('first_name', String(45))
    last_name = Column('last_name', String(45))
    is_staff = Column('is_staff', Integer)
    is_active = Column('is_active', Integer)
    date_joined = Column('date_joined', DATETIME, default=datetime.now())
    last_login = Column('last_login', DATETIME(6))
    is_superuser = Column('is_superuser', Integer)
    image = Column('image', String(45))

def main(args):
    """
    メイン関数
    """
    if args[1] == "create":
        Base.metadata.create_all(bind=ENGINE)

    elif args[1] == "delete":
        User.__table__.drop(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)
