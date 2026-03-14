from discord.ext import commands
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///database/users.db'  # データベースの種類と名前をここで指定できます
engine = create_engine(DATABASE_URL)  # データベースエンジンを作成
Base = declarative_base()            # データベースの親クラスを作成


class User(Base):
    __tablename__ = 'users'
    no = Column(Integer, primary_key=True)
    userid = Column(Integer)
    username = Column(String)
    displayname = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Sqltest1(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Sqltest1(bot))
