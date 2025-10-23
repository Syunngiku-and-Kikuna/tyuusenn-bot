from discord.ext import commands
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///cmdlab_users.db'  # データベースの種類と名前をここで指定できます
engine = create_engine(DATABASE_URL)  # データベースエンジンを作成
Base = declarative_base()            # データベースの親クラスを作成


class User(Base):
    __tablename__ = 'users'
    no = Column(Integer, primary_key=True)
    userid = Column(Integer)
    username = Column(String)
    oubo = Column(Boolean, default=False)
    rsl1 = Column(Boolean, default=False)
    rsl2 = Column(Boolean, default=False)
    rsc1 = Column(Boolean, default=False)
    rsc2 = Column(Boolean, default=False)
    rsc3 = Column(Boolean, default=False)
    rsc4 = Column(Boolean, default=False)
    rsc5 = Column(Boolean, default=False)
    rsc6 = Column(Boolean, default=False)
    rsc7 = Column(Boolean, default=False)
    rsc8 = Column(Boolean, default=False)
    rsc9 = Column(Boolean, default=False)
    rsc10 = Column(Boolean, default=False)
    pushbutton = Column(Integer, default=0)
    str1 = Column(String, default="")
    str2 = Column(String, default="")
    str3 = Column(String, default="")
    str4 = Column(String, default="")
    str5 = Column(String, default="")
    str6 = Column(String, default="")
    str7 = Column(String, default="")
    str8 = Column(String, default="")
    str9 = Column(String, default="")
    str10 = Column(String, default="")
    int1 = Column(Integer, default=0)
    int2 = Column(Integer, default=0)
    int3 = Column(Integer, default=0)
    int4 = Column(Integer, default=0)
    int5 = Column(Integer, default=0)
    int6 = Column(Integer, default=0)
    int7 = Column(Integer, default=0)
    int8 = Column(Integer, default=0)
    int9 = Column(Integer, default=0)
    int10 = Column(Integer, default=0)
    bool1 = Column(Boolean, default=False)
    bool2 = Column(Boolean, default=False)
    bool3 = Column(Boolean, default=False)
    bool4 = Column(Boolean, default=False)
    bool5 = Column(Boolean, default=False)
    bool6 = Column(Boolean, default=False)
    bool7 = Column(Boolean, default=False)
    bool8 = Column(Boolean, default=False)
    bool9 = Column(Boolean, default=False)
    bool10 = Column(Boolean, default=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# DATABASE_URL2 = 'sqlite:///ore_gacha.db'  # データベースの種類と名前をここで指定できます
# engine2 = create_engine(DATABASE_URL2)  # データベースエンジンを作成
# Base2 = declarative_base()            # データベースの親クラスを作成
# 
# 
# class Oregacha(Base2):
#     __tablename__ = 'usersgacha'
#     no = Column(Integer, primary_key=True)
#     userid = Column(Integer)
#     username = Column(String)
#     allcount = Column(Integer, default=0)
# 
#     netheritei = Column(Integer, default=0)
#     netherites = Column(Integer, default=0)
#     lapis = Column(Integer, default=0)
#     diamond = Column(Integer, default=0)
#     gold = Column(Integer, default=0)
#     redstone = Column(Integer, default=0)
#     emerald = Column(Integer, default=0)
#     iron = Column(Integer, default=0)
#     copper = Column(Integer, default=0)
#     quartz = Column(Integer, default=0)
#     coal = Column(Integer, default=0)
#     breaking_pickaxe = Column(Integer, default=0)
#     broken_pickaxe = Column(Integer, default=0)
#     death = Column(Integer, default=0)
# 
#     beacon = Column(Integer, default=0)
#     netheriteb = Column(Integer, default=0)
#     lapisb = Column(Integer, default=0)
#     diamondb = Column(Integer, default=0)
#     goldb = Column(Integer, default=0)
#     redstoneb = Column(Integer, default=0)
#     emeraldb = Column(Integer, default=0)
#     ironb = Column(Integer, default=0)
#     copperb = Column(Integer, default=0)
#     quartzb = Column(Integer, default=0)
#     coalb = Column(Integer, default=0)
#     broken_pickaxe9 = Column(Integer, default=0)
#     death9 = Column(Integer, default=0)
#     unkownworld = Column(Integer, default=0)
# 
#     dailygacha = Column(Integer, default=0)
# 
#     ogstr1 = Column(String, default="")  # ogstr1 : cog.core_gacha.py使用中(１日のガチャによる結果表示)
#     ogstr2 = Column(String, default="")
#     ogstr3 = Column(String, default="")
#     ogstr4 = Column(String, default="")
#     ogstr5 = Column(String, default="")
#     ogint1 = Column(Integer, default=0)  # cog.core_gacha.py使用中(１日のガチャによる経験値量の収支)#//userid:101のみ９倍デーのガチャ合計カウント
#     ogint2 = Column(Integer, default=0)
#     ogint3 = Column(Integer, default=0)
#     ogint4 = Column(Integer, default=0)
#     ogint5 = Column(Integer, default=0)
#     ogint6 = Column(Integer, default=0)
#     ogint7 = Column(Integer, default=0)
#     ogint8 = Column(Integer, default=0)
#     ogint9 = Column(Integer, default=0)
#     ogint10 = Column(Integer, default=0)
#     ogbool1 = Column(Boolean, default=False)
#     ogbool2 = Column(Boolean, default=False)
#     ogbool3 = Column(Boolean, default=False)
#     ogbool4 = Column(Boolean, default=False)
#     ogbool5 = Column(Boolean, default=False)
#     ogbool6 = Column(Boolean, default=False)
#     ogbool7 = Column(Boolean, default=False)
#     ogbool8 = Column(Boolean, default=False)
#     ogbool9 = Column(Boolean, default=False)
#     ogbool10 = Column(Boolean, default=False)
# 
# 
# Base2.metadata.create_all(engine2)
# Session2 = sessionmaker(bind=engine2)
# session2 = Session2()


class Sqltest1(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def setup(bot: commands.Bot):
    await bot.add_cog(Sqltest1(bot))
