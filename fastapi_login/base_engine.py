from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

FERNET_KEY_PASS = b'YDWyjuUJ2G-gLjK-VJ9fMh2A99WIZr-HZP1PiiYOGGc='
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ACCESS_TOKEN_EXPIRE_MINUTES = 180

engine = create_engine("postgresql://postgres:dD5Yz6xE5m@localhost:5435/logintestdb", pool_size=2000, max_overflow=0)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()