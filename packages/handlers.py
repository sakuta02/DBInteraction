from aiogram import Router
from packages.localization import phrases, keyboard_number, keyboard_choose_room, button_exit, keyboard_look
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from packages.db_interaction import DBInteraction, users
from datetime import date, timedelta, datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

rt = Router()
DBInteraction.start_bot()


@rt.message(Command(commands=["start"]))
async def greetings(message: Message):
    if message.from_user.id not in users:
        await message.answer(text=phrases["start"],
                             reply_markup=keyboard_number.as_markup(resize_keyboard=True, one_time_keyboard=True))


@rt.message(lambda x: x.contact)
async def get_info(message: Message):
    cont = message.contact
    await message.answer(text="Отлично!", reply_markup=ReplyKeyboardRemove())
    users[int(message.from_user.id)] = DBInteraction(id_user=int(message.from_user.id),
                                                     phone_number=int(cont.phone_number.replace('+', '')),
                                                     name=str(cont.first_name))
    await message.answer(text=phrases["rest"], reply_markup=keyboard_choose_room.as_markup())


@rt.callback_query(lambda x: x.data == 'exit')
async def send_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=phrases["rest"], reply_markup=keyboard_choose_room.as_markup())


@rt.callback_query(lambda x: x.data == "look")
async def exit_menu(callback: CallbackQuery):
    value = users[callback.from_user.id].check_reservations()
    if not value:
        await callback.message.edit_text(text=phrases["no_info"],
                                         reply_markup=InlineKeyboardBuilder([[button_exit]]).as_markup())
    else:
        date_res, time_res = str(value[0]).split()
        room_number = value[1]
        if room_number == "3":
            room_number = "VIP"
        await callback.message.answer(text=phrases["info_res"].format(date_res, time_res[:-3], room_number))


@rt.callback_query(lambda x: x.data in "123")
async def show_dates(callback: CallbackQuery):
    date_now = date.today()
    week_to = [date_now + timedelta(days=i) for i in range(0, 8)]

    # Создание кнопок с днями недели
    day_buttons = [
        InlineKeyboardButton(
            text=str(day.day),
            callback_data=f"day_{day.strftime('%Y-%m-%d %H:%M:%S')}_{callback.data}"
        )
        for day in week_to
    ]
    await callback.message.edit_text(text=phrases["day"],
                                     reply_markup=InlineKeyboardBuilder(
                                         [day_buttons[:4], day_buttons[4:], [button_exit]]
                                     ).as_markup())


@rt.callback_query(lambda x: 'day_' in x.data)
async def show_free_time(callback: CallbackQuery):
    _, date_temp, index = callback.data.split('_')
    date_temp = datetime.fromisoformat(date_temp)
    values = DBInteraction.select_free_time(int(index), date_temp)
    if values:
        to_response = InlineKeyboardBuilder([list(map(lambda x: InlineKeyboardButton(text=x[-8:-3],
                                                                                     callback_data=f'call_{x}_{index}'),
                                                      values)), [button_exit]])
        await callback.message.edit_text(text=phrases["time"], reply_markup=to_response.as_markup())
    else:
        await callback.message.edit_text(text=phrases["no_time"],
                                         reply_markup=InlineKeyboardBuilder([[button_exit]]).as_markup())
    

@rt.callback_query(lambda x: 'call_' in x.data)
async def add_reservation(callback: CallbackQuery):
    _, date_data, index = callback.data.split('_')
    users[callback.from_user.id].insert_reservation(date_res=date_data,
                                                    index=int(index))
    await callback.message.edit_text(text=phrases["successfully"], reply_markup=keyboard_look.as_markup())


@rt.message(lambda x: x)
async def every_message(message: Message):
    await message.answer(text="comming soon...")
    
    
@rt.callback_query(lambda x: x)
async def every_callback(callback: CallbackQuery):
    await callback.answer(text=callback.data)
