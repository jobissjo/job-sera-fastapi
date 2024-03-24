from typing import List, Optional
from pydantic import BaseModel
from app.models.jobs import JobModel


class Review(BaseModel):
    username: str
    reviewText: str
    reviewScore: int
    reviewedDate: Optional[str]


class CompanyModel(BaseModel):
    companyName: str
    address: str
    employeesCount: int
    reviewsCount: int
    totalReviewRating: int
    reviews: List[Review] = []
    openings: List[JobModel] = []