# Relationships: has many Transaction, ManualEntry, Holding.
# official_balance is a cache, only ever updated by sync_service (Plaid) or the
# manual_router (manual entries/holdings) -- never recomputed ad hoc elsewhere.
from app.config import settings
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base


class Account(Base):
    user_id = Column(Integer, ForeignKey('users.id'))
    plaid_item_id = Column(Integer, ForeignKey('plaid_items.id'), nullable=True)
    plaid_account_id = Column(Integer, nullable=True, unique=True)
    name = Column(String)
    type = Column(String)
    offical_balance = Column(String)
    currency = Column(String)
    is_manual = Column(Boolean)
    is_active = Column(Boolean)
    