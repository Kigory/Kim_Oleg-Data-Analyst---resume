from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import requests as req


def choice_direction():
    inline_kb_list = [
        [InlineKeyboardButton(text="Смо - РЦ ВН", callback_data='dir_smo-VH')],
        [InlineKeyboardButton(text="Смо - РЦ Карелия", callback_data='dir_smo-Kar')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def result_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Готово", callback_data='res_done')],
        [InlineKeyboardButton(text="Начать сначала", callback_data='res_again')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]


    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def choice_input():
    inline_kb_list = [
        [InlineKeyboardButton(text="Отметить погрузку", callback_data='ch_load')],
        [InlineKeyboardButton(text="Отметить выезд с ворот", callback_data='ch_out')],
        [InlineKeyboardButton(text="Внести ТС", callback_data='ch_transport')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]


    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def main_kb():
    kb_list = [
        [KeyboardButton(text="Внести данные"), KeyboardButton(text="Получить данные")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list,
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder="выберите ы:")
    return keyboard


def sec_direction():
    inline_kb_list = [
        [InlineKeyboardButton(text="Смо - РЦ ВН", callback_data='outdir_smo-VH')],
        [InlineKeyboardButton(text="Смо - РЦ Карелия", callback_data='outdir_smo-Kar')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def result_kbsec():
    inline_kb_list = [
        [InlineKeyboardButton(text="Готово", callback_data='outres_done')],
        [InlineKeyboardButton(text="Начать сначала", callback_data='outres_again')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]


    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def tr_dir():
    inline_kb_list = [
        [InlineKeyboardButton(text="Смо - РЦ ВН", callback_data='trdir_smo-VH')],
        [InlineKeyboardButton(text="Смо - РЦ Карелия", callback_data='trdir_smo-Kar')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def result_tr():
    inline_kb_list = [
        [InlineKeyboardButton(text="Готово", callback_data='trres_done')],
        [InlineKeyboardButton(text="Начать сначала", callback_data='trres_again')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]


    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def transport_to(direct):
    all_tr = await req.get_transport_dir(direct)

    kb = InlineKeyboardBuilder()
    for tr in all_tr:
        kb.add(InlineKeyboardButton(text=tr.transport, callback_data=f'listtr_{tr.transport}'))
    return kb.adjust(1).as_markup()


async def transport_out(direct):
    all_tr = await req.get_transport_dir(direct)

    kb = InlineKeyboardBuilder()
    for tr in all_tr:
        kb.add(InlineKeyboardButton(text=tr.transport, callback_data=f'seclisttr_{tr.transport}'))
    return kb.adjust(1).as_markup()


async def get_data():
    inline_kb_list = [
        [InlineKeyboardButton(text="Данные по выезду", callback_data='data_out')],
        [InlineKeyboardButton(text="Данные по погрузке", callback_data='data_load')],
        [InlineKeyboardButton(text="Данные по тс", callback_data='data_tr')],
        [InlineKeyboardButton(text="на главную", callback_data='ch_back')]

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


async def transport_load_date():
    all_dates = await req.get_date_load()

    kb_list = []
    for dt in all_dates:
        s = [InlineKeyboardButton(text=dt.tr_date[:10], callback_data=f'loaddt{dt.tr_date[:10]}')]
        if s in kb_list:
            continue
        else:
            kb_list.append(s)
    return InlineKeyboardMarkup(inline_keyboard=kb_list)


async def transport_out_date():
    all_dates = await req.get_date_out()

    kb_list = []
    for dt in all_dates:
        s = [InlineKeyboardButton(text=dt.tr_date[:10], callback_data=f'loaddt{dt.tr_date[:10]}')]
        if s in kb_list:
            continue
        else:
            kb_list.append(s)
    return InlineKeyboardMarkup(inline_keyboard=kb_list)
