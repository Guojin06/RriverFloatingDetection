from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)
    videos = relationship('Video', back_populates='user')
    logs = relationship('Log', back_populates='user')

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    video_path = Column(String(255), nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='pending')
    user = relationship('User', back_populates='videos')
    detection_results = relationship('DetectionResult', back_populates='video')

class DetectionResult(Base):
    __tablename__ = 'detection_results'
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    result_json = Column(Text, nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow)
    video = relationship('Video', back_populates='detection_results')

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(255))
    action_time = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='logs') 