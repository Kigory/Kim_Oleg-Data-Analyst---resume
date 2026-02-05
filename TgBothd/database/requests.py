from database.models import async_session
from database.models import User, Transport_load, Transport_out, Transport
from sqlalchemy import select


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_ts(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def fill_load(user_id, direction, user_name, lots, transport, dt):
    async with async_session() as session:
        session.add(Transport_load(user_id=user_id, user_name=user_name, direction=direction,
                                   lots=lots, transport=transport, tr_date=dt))
        await session.commit()


async def fill_out(user_id, direction, user_name, transport, dt):
    async with async_session() as session:
        session.add(Transport_out(user_id=user_id, user_name=user_name, direction=direction,
                                  transport=transport, tr_date=dt))
        await session.commit()


async def fill_tr(tr, direction):
    async with async_session() as session:
        transport = await session.scalar(select(Transport).where(Transport.transport == tr))
        direct = await session.scalar(select(Transport).where(Transport.direction == direction))
        if not transport or not direct:
            session.add(Transport(direction=direction, transport=tr))
            await session.commit()


async def get_transport_dir(direct):
    async with async_session() as session:
        return await session.scalars(select(Transport).where(Transport.direction == direct))


async def transport_data():
    async with async_session() as session:
        res = await session.scalars(select(Transport))
        text_res = ""
        for i in res:
            text_res += f"{i.id}\nнаправление: {i.direction} | ТС: {i.transport}\n"
        return text_res


async def out_data():
    async with async_session() as session:
        res = await session.scalars(select(Transport_out))
        text_res = ""
        for i in res:
            text_res += (f"{i.id}\nнаправление: {i.direction} | ТС: {i.transport}\nСотрудник: {i.user_name}"
                         f" | Дата: {i.tr_date[:19]}\n")
        return text_res


async def load_data():
    async with async_session() as session:
        res = await session.scalars(select(Transport_load))
        text_res = ""
        for i in res:
            text_res += (f"{i.id}\nнаправление: {i.direction} | ТС: {i.transport}\nСотрудник: {i.user_name}"
                         f" | Лотков: {i.lots}\nДата: {i.tr_date[:19]}\n")
        return text_res


async def get_date_load():
    async with async_session() as session:
        return await session.scalars(select(Transport_load))


async def get_date_out():
    async with async_session() as session:
        return await session.scalars(select(Transport_out))


async def get_date_ss(dates):
    async with async_session() as session:
        return await session.scalars(select(Transport_out))