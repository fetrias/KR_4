from sqlalchemy import Column, Integer, Numeric, String, Text, text

from app.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    count = Column(Integer, nullable=False)
    description = Column(Text, nullable=False, server_default=text("''"))
