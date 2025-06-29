# models.py
from sqlalchemy import Column, Integer, String, JSON, Text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# All models
class ServerProfile(Base):
    __tablename__ = "server_profiles"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, unique=True, index=True)
    data = Column(JSON)

class GuildProfile(Base):
    __tablename__ = "guild_profiles"
    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(String, unique=True, index=True)
    summary = Column(Text)

class GuildWord(Base):
    __tablename__ = "guild_words"
    id = Column(Integer, primary_key=True)
    guild_id = Column(String, index=True)
    word = Column(String, index=True)
    count = Column(Integer, default=0)

class GuildEmoji(Base):
    __tablename__ = "guild_emojis"
    id = Column(Integer, primary_key=True)
    guild_id = Column(String, index=True)
    emoji = Column(String, index=True)
    count = Column(Integer, default=0)

class UserWord(Base):
    __tablename__ = "user_words"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    guild_id = Column(String, index=True)
    word = Column(String, index=True)
    count = Column(Integer, default=0)

class UserEmoji(Base):
    __tablename__ = "user_emojis"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    guild_id = Column(String, index=True)
    emoji = Column(String, index=True)
    count = Column(Integer, default=0)
