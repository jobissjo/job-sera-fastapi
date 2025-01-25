from typing import List, Optional
from pydantic import BaseModel
from app.schema.jobs import JobModel


class Review(BaseModel):
    username: str
    reviewText: str
    reviewScore: int
    reviewedDate: Optional[str]


class CompanyModel(BaseModel):
    companyName: str
    address: str
    landmark:str
    employeesCount: int
    reviewsCount: int
    totalReviewRating: int
    reviews: list[Review]
    openings: List[JobModel] = []