from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Ejemplo: "Miami-Quito"

    segments = relationship("Segment", back_populates="route", cascade="all, delete-orphan")

class Segment(Base):
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    distance_km = Column(Integer, nullable=False)  # ⚠️ Se mantiene en snake_case internamente

    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    route = relationship("Route", back_populates="segments")

    # ⬇️ Campo de actualización automática
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
