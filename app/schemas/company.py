from app.utils.database import Base
from sqlalchemy import Column, String,Integer
from sqlalchemy.orm import relationship
from app.schemas.jobs import Job

class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    reviewText = Column(String)
    reviewScore = Column(Integer)
    reviewedDate = Column(String)


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, autoincrement=True)
    companyName = Column(String)
    address = Column(String)
    employeesCount = Column(Integer)
    reviewsCount = Column(Integer)
    totalReviewRating = Column(Integer)
    
    reviews = relationship("Review", backref="company")
    openings = relationship("Job", backref="company")