from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from datetime import datetime

import os, sys
sys.path.append(os.getcwd()) # コマンド実行ディレクトリを設定
from config.settings import ENGINE, Base

from mysite.models.user_auth import UserAuth

class Social(Base):

    __tablename__ = 'social'
    id = Column('id', Integer, primary_key = True)
    user_id = Column('user_id', ForeignKey('auth_user.id',onupdate='CASCADE', ondelete='CASCADE'))
    provider = Column('provider', String(200))
    provider_id = Column('provider_id', String(200))
    created_at = Column('created_at', DateTime, default=datetime.now())

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
