"""
SQLAlchemy ORM models for Mindflow database
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserProfile(Base):
    """User profile and initial questionnaire data"""

    __tablename__ = "user_profile"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)  # For multi-user support in future
    name = Column(String(255), nullable=True)
    goals = Column(JSON, nullable=True)  # List of long-term goals
    values = Column(JSON, nullable=True)  # User values and principles
    work_direction = Column(String(255), nullable=True)
    personality_traits = Column(JSON, nullable=True)  # User personality characteristics
    weak_points = Column(JSON, nullable=True)  # Areas for improvement
    preferred_reminder_style = Column(
        String(50), nullable=True
    )  # motivating, decompose, practical
    timezone = Column(String(50), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    behavior_features = relationship(
        "UserBehaviorFeatures", back_populates="user", cascade="all, delete-orphan"
    )
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    plans = relationship("Plan", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    conversation_history = relationship(
        "ConversationHistory", back_populates="user", cascade="all, delete-orphan"
    )


class UserBehaviorFeatures(Base):
    """User behavior features learned by the system"""

    __tablename__ = "user_behavior_features"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profile.id"), nullable=False)
    feature_key = Column(String(100), nullable=False)  # action_style, thinking_depth, etc.
    feature_value = Column(JSON, nullable=False)  # {value: "...", confidence: 0.85, evidence: [...]}
    confidence = Column(Float, default=0.0)  # Confidence score 0-1
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("UserProfile", back_populates="behavior_features")


class Event(Base):
    """Life events recorded by the user"""

    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profile.id"), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)  # work, learning, life, health, personal
    description = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False)  # When the event happened
    tags = Column(JSON, nullable=True)  # List of tags
    related_plans = Column(JSON, nullable=True)  # List of related plan IDs
    source = Column(String(50), nullable=True)  # conversation, manual_input, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("UserProfile", back_populates="events")


class Plan(Base):
    """User plans and goals"""

    __tablename__ = "plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profile.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active")  # active, completed, archived
    priority = Column(String(20), default="medium")  # high, medium, low
    progress = Column(Integer, default=0)  # 0-100
    start_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    milestones = Column(JSON, nullable=True)  # List of milestones
    related_events = Column(JSON, nullable=True)  # List of related event IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("UserProfile", back_populates="plans")
    updates = relationship("PlanUpdate", back_populates="plan", cascade="all, delete-orphan")


class PlanUpdate(Base):
    """Track plan progress changes"""

    __tablename__ = "plan_updates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), ForeignKey("plans.id"), nullable=False)
    progress_before = Column(Integer, nullable=True)
    progress_after = Column(Integer, nullable=True)
    update_note = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    plan = relationship("Plan", back_populates="updates")


class Review(Base):
    """Daily review records"""

    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profile.id"), nullable=False)
    review_date = Column(String(10), nullable=False)  # YYYY-MM-DD format
    layer1_response = Column(JSON, nullable=True)  # Basic framework answers
    layer2_response = Column(JSON, nullable=True)  # Event dimension answers
    layer3_response = Column(JSON, nullable=True)  # Plan dimension answers
    layer4_response = Column(JSON, nullable=True)  # Personalized dimension answers
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("UserProfile", back_populates="reviews")


class ConversationHistory(Base):
    """Store conversation history for context and learning"""

    __tablename__ = "conversation_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("user_profile.id"), nullable=False)
    session_id = Column(String(36), nullable=True)
    message_type = Column(String(20), nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    related_events = Column(JSON, nullable=True)  # Events extracted from this message
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("UserProfile", back_populates="conversation_history")
