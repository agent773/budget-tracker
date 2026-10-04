# Spending/income category, optionally nested (e.g. "Food" > "Groceries"/"Dining").
# Relationships: has many Transaction, Budget, CategorizationRule.

from app.config import settings
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, Nullable, String, Boolean, DateTime, ForeignKey
from app.database import Base


class Category(Base):
    user_id = Column(Integer, ForeignKey('user_id'), nullable=True)
    name = Column(String)
    parent_category_id = Column(Integer, nullable=True)
    is_income = Column(Boolean)