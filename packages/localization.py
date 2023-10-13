from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton


'''PHRASES'''
phrases = {
    "start": "<b>Привет!</b>\nМы ресторан с необычным образом бронирования столиков и заказа еды\nНажимай на кнопку 'Начать' и мы можем приступать 😋",
    "rest": "Ниже указанны номера залов и VIP\nНажмите на кнопку с номером",
    "day": "Ниже указанны числа на неделю вперед\nВыберите более подходящий для вас день",
    "time": "Выберите удобное вам время",
    "no_time": "К сожалению на этот день у нас нет свободных столиков",
    "has": "У вас уже есть зарезервированный столик",
    "successfully": "Бронирование прошло успешно!"
}

buttons = {
    "first": "1",
    "second": "2",
    "vip": "VIP",
    "exit": "В меню",
    "look": "Посмотреть мой заказ"
}

# Here are some buttons

# menu button
button_exit = InlineKeyboardButton(text=buttons["exit"], callback_data="exit")

# send a contact information
keyboard_number = ReplyKeyboardBuilder(markup=[[KeyboardButton(text="Начать", request_contact=True)]])

# Choose room
button_first_room = InlineKeyboardButton(text=buttons["first"], callback_data="1")
button_second_room = InlineKeyboardButton(text=buttons["second"], callback_data="2")
button_vip_room = InlineKeyboardButton(text=buttons["vip"], callback_data="3")
keyboard_choose_room = InlineKeyboardBuilder([[button_first_room, button_second_room], [button_vip_room]])

# Watch table
butoon_watch = InlineKeyboardButton(text=buttons["look"], callback_data="look")
keyboard_look = InlineKeyboardBuilder([[butoon_watch]])
