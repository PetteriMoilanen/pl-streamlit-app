from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Team(Base):
    __tablename__ = "teams"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(10)) 

class Venue(Base):
    __tablename__ = "venues"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    city: Mapped[Optional[str]] = mapped_column(String(100))

class Season(Base):
    __tablename__ = "seasons"
    
    id: Mapped[str] = mapped_column(String(50), primary_key=True) 
    name: Mapped[str] = mapped_column(String(100), nullable=False) 

class Match(Base):
    __tablename__ = "matches"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[str] = mapped_column(ForeignKey("seasons.id"), nullable=False)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)
    
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    
    match_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    home_score: Mapped[Optional[int]] = mapped_column(Integer)
    away_score: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Denormalized Weather Data
    weather_temp: Mapped[Optional[float]] = mapped_column(Float)
    weather_condition: Mapped[Optional[str]] = mapped_column(String(50))

class AggregateMatchState(Base):
    __tablename__ = "aggregate_match_states"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    
    # Snapshot performance metrics *before* this specific match kicked off
    home_points: Mapped[int] = mapped_column(Integer, default=0)
    away_points: Mapped[int] = mapped_column(Integer, default=0)
    home_goal_diff: Mapped[int] = mapped_column(Integer, default=0)
    away_goal_diff: Mapped[int] = mapped_column(Integer, default=0)

class Pundit(Base):
    __tablename__ = "pundits"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    organization: Mapped[Optional[str]] = mapped_column(String(100)) 

class MatchPrediction(Base):
    __tablename__ = "match_predictions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    pundit_id: Mapped[int] = mapped_column(ForeignKey("pundits.id"), nullable=False)
    
    prediction_summary: Mapped[str] = mapped_column(String(500), nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(500))