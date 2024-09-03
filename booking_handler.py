import sqlite3
import datetime
from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

user_state = {}


class BookingState(StatesGroup):
    waiting_for_name = State()
    waiting_for_time = State()
    waiting_for_cancel_info = State() 


def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            client_name TEXT NOT NULL,
            service TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cancellations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class BookingHandler:
    @staticmethod
    async def handle_cancel_booking(message: types.Message, state: FSMContext):
        await message.answer("Пожалуйста, введите дату и время бронирования, которое хотите отменить (формат: YYYY-MM-DD HH:MM), и ваше имя, разделенные пробелом:")
        await BookingState.waiting_for_cancel_info.set()

    @staticmethod
    async def handle_cancel_info_input(message: types.Message, state: FSMContext):
        cancel_info = message.text.strip()
        try:
            cancel_date, cancel_time, client_name = cancel_info.split(' ', 2)
        except ValueError:
            await message.answer("Пожалуйста, введите данные в формате: YYYY-MM-DD HH:MM Имя")
            return

       
        try:
            datetime.datetime.strptime(cancel_date, '%Y-%m-%d')
            datetime.datetime.strptime(cancel_time, '%H:%M')
        except ValueError:
            await message.answer("Неверный формат даты или времени.")
            return

     
        conn = sqlite3.connect('bookings.db')
        c = conn.cursor()
        c.execute('DELETE FROM bookings WHERE date = ? AND time = ? AND client_name = ?', (cancel_date, cancel_time, client_name))
        conn.commit()
        affected_rows = c.rowcount
        conn.close()

        if affected_rows > 0:
            await message.answer(f"Ваша запись на {cancel_date} в {cancel_time} была успешно отменена.")
        else:
            await message.answer(f"Запись на {cancel_date} в {cancel_time} для клиента {client_name} не найдена.")

        await state.finish()

    @staticmethod
    async def handle_booking(bot, callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        
        service = callback_query.data.split('_')[1]  # Пол услугу из callback_data
        user_id = callback_query.from_user.id
        user_state[user_id] = {"service": service}
        
        today = datetime.date.today()
        dates = [today + datetime.timedelta(days=i) for i in range(7)]
        
        date_keyboard = types.InlineKeyboardMarkup()
        for date in dates:
            date_keyboard.add(types.InlineKeyboardButton(
                text=date.strftime('%A, %d %B'), callback_data=f'date_{date}'))
        
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="Выберите дату:",
            reply_markup=date_keyboard
        )
        
    @staticmethod
    async def handle_date_selection(bot, callback_query: types.CallbackQuery, state: FSMContext):
        selected_date = callback_query.data.split('date_')[1]
        user_id = callback_query.from_user.id
        user_state[user_id]["date"] = selected_date
        
        await bot.answer_callback_query(callback_query.id)
        
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="Пожалуйста, введите ваше имя:"
        )
        
        await BookingState.waiting_for_name.set()

    @staticmethod
    async def handle_name_input(message: Message, state: FSMContext):
        user_id = message.from_user.id
        user_name = message.text.strip()
        
        if user_id in user_state:
            user_state[user_id]["name"] = user_name
        
        await message.answer(f"Спасибо, {user_name}. Теперь выберите время:")

        times = [f"{hour}:00" for hour in range(9, 18)]
        time_keyboard = types.InlineKeyboardMarkup()
        for time in times:
            time_keyboard.add(types.InlineKeyboardButton(
                text=time, callback_data=f'time_{user_state[user_id]["date"]}_{time}'))
        
        await message.answer("Выберите время:", reply_markup=time_keyboard)
        
        await BookingState.waiting_for_time.set()

    @staticmethod
    async def handle_time_selection(bot, callback_query: types.CallbackQuery, state: FSMContext):
        _, selected_date, selected_time = callback_query.data.split('_')
        user_id = callback_query.from_user.id
        user_info = user_state.get(user_id, {})
        
        service = user_info.get("service", "Неизвестно")
        client_name = user_info.get("name", "Неизвестно")
        
        await bot.answer_callback_query(callback_query.id)
        
        conn = sqlite3.connect('bookings.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO bookings (date, time, client_name, service)
            VALUES (?, ?, ?, ?)
        ''', (selected_date, selected_time, client_name, service))
        conn.commit()
        conn.close()
        # with open('image/eva_.png','rb') as photo:
        #     await bot.send_photo(
        #         chat_id=callback_query.chat.id,
        #         photo=photo,)
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"Вы забронировали {service} на {selected_date} в {selected_time}, {client_name}.",
        )
        
        await state.finish()
        user_state.pop(user_id, None)


dp.register_callback_query_handler(BookingHandler.handle_booking, lambda c: c.data in ["service1", "service2", "service3"])
dp.register_callback_query_handler(BookingHandler.handle_date_selection, lambda c: c.data.startswith('date_'), state='*')
dp.register_message_handler(BookingHandler.handle_name_input, state=BookingState.waiting_for_name)
dp.register_callback_query_handler(BookingHandler.handle_time_selection, lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
dp.register_message_handler(BookingHandler.handle_cancel_booking, commands=['cancel_booking'])
dp.register_message_handler(BookingHandler.handle_cancel_info_input, state=BookingState.waiting_for_cancel_info)
