# A spending target for one category in one month.
#
# Fields: user_id (FK), category_id (FK), month (first-of-month date, e.g.
# 2026-09-01), target_amount. Unique on (category_id, month).
#
# actual_spent is NOT a column -- compute it on read by summing Transaction.amount
# for that category within that month, so it never drifts from the ledger.
from app.config import settings
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base


class Budget(Base):
    user_id = Column(Integer, ForeignKey('user_id'))
    category_id = Column(Integer, ForeignKey('category_id'),primary_key=True,unique=True)
    month = Column(DateTime, unique=True)
    target_amount = Column(Integer)
    