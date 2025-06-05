from sqlalchemy import String, Integer, DateTime, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime

## タイムゾーン用
# import pytz
# from datetime import datetime
# jst = pytz.timezone('Asia/Tokyo')

class Base(DeclarativeBase):
    pass


class Item_master(Base):
    __tablename__ = 'item_master'
    PRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CODE: Mapped[str] = mapped_column(String(13))
    NAME: Mapped[str] = mapped_column(String(50))
    PRICE: Mapped[int] = mapped_column(Integer)

class Transaction(Base):
    __tablename__ = 'transaction'   
    TRD_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    DATETIME: Mapped[str] = mapped_column(DateTime)
    EMP_CD: Mapped[str] = mapped_column(String(10))
    STORE_CD: Mapped[str] = mapped_column(String(5))
    POS_NO: Mapped[str] = mapped_column(String(3))
    TOTAL_AMT: Mapped[int] = mapped_column(Integer)
    TTL_AMT_EX_TAX: Mapped[int] = mapped_column(Integer)


class Transaction_Details(Base):
    __tablename__ = 'transaction_details'
    DTL_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    TRD_ID: Mapped[int] = mapped_column(Integer)
    PRD_ID: Mapped[int] = mapped_column(Integer)
    PRD_CODE: Mapped[str] = mapped_column(String(13))
    PRD_NME: Mapped[str] = mapped_column(String(50))
    PRD_PRICE: Mapped[int] = mapped_column(Integer)
    TAX_CD: Mapped[str] = mapped_column(String(2))
    PRD_COUNT: Mapped[int] = mapped_column(Integer)



