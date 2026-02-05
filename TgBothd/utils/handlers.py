import asyncio
import database.requests as req

from datetime import timedelta, datetime
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils import keyboards as kb

start_router = Router()

dir_dict = {'dir_smo-mur': "Смо-Мур", "dir_mur-smo": "Мур-Смо",
            "dir_smo-VH": "Смо-ВН", "dir_smo-Kar": "Смо-Карелия",
            "dir_VH-Смо": "ВН-Смо",
            'outdir_smo-mur': "Смо-Мур", "outdir_mur-smo": "Мур-Смо",
            "outdir_smo-VH": "Смо-ВН", "outdir_smo-Kar": "Смо-Карелия",
            "outdir_VH-Смо": "ВН-Смо",
            'trdir_smo-mur': "Смо-Мур", "trdir_mur-smo": "Мур-Смо",
            "trdir_smo-VH": "Смо-ВН", "trdir_smo-Kar": "Смо-Карелия",
            "trdir_VH-Смо": "ВН-Смо"
            }


class TransportIn(StatesGroup):
    transport = State()
    direction = State()


class Whdata(StatesGroup):
    direction = State()
    lot = State()
    transport = State()
    create_dt = State()
    creator_name = State()


class Whout(StatesGroup):
    direction = State()
    transport = State()
    create_dt = State()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await req.set_user(message.from_user.id)
    await message.answer('выберите действие',
                         reply_markup=kb.main_kb())


@start_router.message(F.text.lower() == 'внести данные')
async def input_data(message: Message):
    await message.answer('выберите действие',
                         reply_markup=kb.choice_input())


# обработка внесения данных для погрузки
@start_router.callback_query(F.data == 'ch_load')
async def cmd_start_2(call: CallbackQuery):
    await call.message.edit_text('Выберите направление ',
                                 reply_markup=kb.choice_direction())


# выбираем сохраняем направление и просим ввести кол-во лотков
@start_router.callback_query(F.data.startswith("dir"))
async def capture_directtion(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(direction=call.data)
    data = await state.get_data()
    await call.message.edit_text(f'Выбрано направление: {dir_dict[data.get("direction")]}\n'
                                 f'Внесите кол-во лотков')
    await state.set_state(Whdata.lot)


# Сохраняем кол-во лотков и вводим номер тс
@start_router.message(F.text, Whdata.lot)
async def capture_lots(message: Message, state: FSMContext):
    await state.update_data(lot=message.text)
    data = await state.get_data()
    await state.update_data(create_dt=message.date + timedelta(hours=3))
    await asyncio.sleep(1)
    await message.answer(f'Выбрано направление: {dir_dict[data.get("direction")]}\n'
                         f'Лотков: {data.get("lot")}\n'
                         f'Укажите номер ТС',
                         reply_markup=await kb.transport_to(dir_dict[data.get("direction")]))
    await state.set_state(Whdata.transport)


# просим проверить данные по погрузке и вносим их
@start_router.callback_query(F.data.startswith("listtr"))
async def capture_tr(call: CallbackQuery, state: FSMContext):
    res = call.data.split("_")[1]
    await state.update_data(transport=res)
    data = await state.get_data()
    await call.message.edit_text(f'{call.from_user.full_name}, проверьте внесенные данные, '
                                 f'если все корректно нажмите готово\n'
                                 f'Выбрано направление: {dir_dict[data.get("direction")]}\n'
                                 f'Лотков: {data.get("lot")}\n'
                                 f'Номер ТС: {data.get("transport")}',
                                 reply_markup=kb.result_kb())


@start_router.callback_query(F.data.startswith("res"))
async def result(call: CallbackQuery, state: FSMContext):
    res = call.data.split("_")[1]
    data = await state.get_data()
    u_id = call.from_user.id
    u_name = call.from_user.full_name
    direct = dir_dict[data.get("direction")]
    lots_count = data.get("lot")
    ts = data.get("transport")
    dat = data.get("create_dt")
    if res == "done":
        await call.message.edit_text("Отлично, данные внесены",
                                     reply_markup=kb.choice_input())
        await req.fill_load(
            user_id=u_id,
            user_name=u_name,
            direction=direct,
            lots=lots_count,
            transport=ts,
            dt=dat
        )

    elif res == "again":
        await call.message.edit_text("Возвращаемся к вводу данных погрузки, выберите направление",
                                     reply_markup=kb.choice_direction())
    await state.clear()


@start_router.callback_query(F.data == 'ch_back')
async def ch_back(call: CallbackQuery):
    await call.message.answer("Внести/Получить данные",
                              reply_markup=kb.main_kb())


@start_router.callback_query(F.data == 'ch_out')
async def input_out(call: CallbackQuery):
    await call.message.edit_text('Выберите направление ',
                                 reply_markup=kb.sec_direction())


@start_router.callback_query(F.data.startswith("outdir"))
async def capture_out_dir(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(direction=call.data)
    data = await state.get_data()
    await call.message.edit_text(f'Выбрано направление: {dir_dict[data.get("direction")]}\n'
                                 f'Внесите ТС',
                                 reply_markup=await kb.transport_out(dir_dict[data.get("direction")]))
    await state.set_state(Whout.transport)


@start_router.callback_query(F.data.startswith("seclisttr"))
async def capture_tr(call: CallbackQuery, state: FSMContext):
    call_time = datetime.now()
    res = call.data.split("_")[1]
    await state.update_data(transport=res)
    await state.update_data(create_at=call_time)
    data = await state.get_data()
    await call.message.edit_text(f'{call.from_user.full_name}, проверьте внесенные данные, '
                                 f'если все корректно нажмите готово\n'
                                 f'Выбрано направление: {dir_dict[data.get("direction")]}\n'
                                 f'Номер ТС: {data.get("transport")}',
                                 reply_markup=kb.result_kbsec())


@start_router.callback_query(F.data.startswith("outres"))
async def out_result(call: CallbackQuery, state: FSMContext):
    res = call.data.split("_")[1]
    data = await state.get_data()
    u_id = call.from_user.id
    u_name = call.from_user.full_name
    direct = dir_dict[data.get("direction")]
    ts = data.get("transport")
    dat = data.get("create_at")
    if res == "done":
        await call.message.edit_text("Отлично, данные внесены",
                                     reply_markup=kb.choice_input())
        await req.fill_out(
            user_id=u_id,
            user_name=u_name,
            direction=direct,
            transport=ts,
            dt=dat
        )

    elif res == "again":
        await call.message.edit_text("Возвращаемся к вводу данных убытия, выберите направление",
                                     reply_markup=kb.sec_direction())
    await state.clear()


@start_router.callback_query(F.data == 'ch_transport')
async def input_tr(call: CallbackQuery):
    await call.message.edit_text('Выберите направление ',
                                 reply_markup=kb.tr_dir())


@start_router.callback_query(F.data.startswith("trdir"))
async def input_dir(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(direction=call.data)
    data = await state.get_data()
    await call.message.edit_text(f'выбрано направление {dir_dict[data.get("direction")]}\nвнесите номер ТС')
    await state.set_state(TransportIn.transport)


@start_router.message(F.text, TransportIn.transport)
async def capture_out_tr(message: Message, state: FSMContext):
    await state.update_data(transport=message.text)
    data = await state.get_data()
    await message.answer(f'{message.from_user.full_name},проверьте внесенные данные, '
                         f'если все корректно нажмите готово\n'
                         f'Выбрано направление: {dir_dict[data.get("direction")]}\n'
                         f'Номер ТС: {data.get("transport")}',
                         reply_markup=kb.result_tr())


@start_router.callback_query(F.data.startswith("trres"))
async def out_result(call: CallbackQuery, state: FSMContext):
    res = call.data.split("_")[1]
    data = await state.get_data()
    direct = dir_dict[data.get("direction")]
    ts = data.get("transport")
    if res == "done":
        await call.message.edit_text("Отлично, данные внесены",
                                     reply_markup=kb.choice_input())
        await req.fill_tr(
            direction=direct,
            tr=ts
        )

    elif res == "again":
        await call.message.edit_text("Возвращаемся к вводу данных ТС, выберите направление",
                                     reply_markup=kb.tr_dir())
    await state.clear()


@start_router.message(F.text == "Получить данные")
async def get_data(message: Message):
    await message.answer("Выберите, какие данные необходимо получить",
                         reply_markup=await kb.get_data())


@start_router.callback_query(F.data == "data_tr")
async def get_tr_data(call: CallbackQuery):
    tr = await req.transport_data()
    await call.message.edit_text(f"Вот список всех ТС\n{tr}", reply_markup=await kb.get_data())


@start_router.callback_query(F.data == "data_out")
async def get_out_data(call: CallbackQuery):
    out = await req.out_data()
    await call.message.edit_text(f"Вот список всех убытий\n{out}", reply_markup=await kb.get_data())


@start_router.callback_query(F.data == "data_load")
async def get_out_data(call: CallbackQuery):
    out = await req.load_data()
    await call.message.edit_text(f"Вот список всех погрузок\n{out}", reply_markup=await kb.get_data())


@start_router.message(Command('ss'))
async def cmd_start(message: Message):
    await req.set_user(message.from_user.id)
    await message.answer('выберите действие',
                         reply_markup=await kb.transport_load_date())
