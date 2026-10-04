# Merchant-keyword -> category auto-mapping rule, applied to new transactions
# on Plaid sync, manual entry, and CSV import.
# See services/categorization_service.py for how rules are applied.
from unicodedata import category

from app.config import settings
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base


class CategorizationRule(Base):
    user_id = Column(Integer, ForeignKey('user_id'))
    keyword = Column(String)
    category_id = Column(Integer, ForeignKey('category_id'),unique=True)
    priority = Column(Integer)