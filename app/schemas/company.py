import uuid
from app.core.database import Base
from sqlalchemy import Column, String,Integer,CHAR, ForeignKey, JSON
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(String, ForeignKey(
        "company.id",
        ondelete="CASCADE"
    ))
    username = Column(String)
    reviewText = Column(String)
    reviewScore = Column(Integer)
    reviewedDate = Column(String)

    company = relationship("Company", back_populates='reviews')

class Company(Base):
    __tablename__ = 'company'

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    companyName = Column(String)
    address = Column(String)
    landmark = Column(String)
    employeesCount = Column(Integer)
    reviewsCount = Column(Integer)
    totalReviewRating = Column(Integer)
    openings = Column(JSON)
    reviews = relationship("Review", back_populates="company", cascade="all, delete")