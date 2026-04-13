import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )
    
    filename: Mapped[str]= mapped_column(
        String(255),
        nullable=False
    )
    
    file_path: Mapped[str]= mapped_column(
        String(500),
        nullable=False
    )
    
    sha256_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending"
    )
    
    total_chunks : Mapped[int]= mapped_column(
        Integer,
        default=0
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.utcnow
    )
    
    updated_at: Mapped[datetime]= mapped_column(
        DateTime,
        default= datetime.utcnow,
        onupdate=datetime.utcnow,  
    )
    
    def __repr__(self):
        return f"<Document {self.id} {self.filename} {self.status}>"
    
    
     