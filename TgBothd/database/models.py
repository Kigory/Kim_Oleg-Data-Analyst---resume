from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Transport_load(Base):
    __tablename__ = 'transports_load'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(String(10))
    direction: Mapped[str] = mapped_column(String(25))
    lots = mapped_column(BigInteger)
    transport: Mapped[str] = mapped_column(String(25))
    tr_date: Mapped[str] = mapped_column(String(25))


class Transport_out(Base):
    __tablename__ = 'transports_out'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(String(10))
    direction: Mapped[str] = mapped_column(String(25))
    transport: Mapped[str] = mapped_column(String(25))
    tr_date: Mapped[str] = mapped_column(String(25))


class Transport(Base):
    __tablename__ = "Transports"

    id: Mapped[int] = mapped_column(primary_key=True)
    transport: Mapped[str] = mapped_column(String(15))
    direction: Mapped[str] = mapped_column(String(20))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
