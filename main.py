from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from  aiogram.types import BotCommand
from config import token
from booking_handler import BookingHandler
from booking_handler import BookingState
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging 
# import random_tip
# import random

storage = MemoryStorage()
bot=Bot(token=token)
dp=Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
user_state = {}



button1= types.KeyboardButton('Парикмахерские услуги 💇')
button2=types.KeyboardButton('Маникюр 💅')
button3=types.KeyboardButton('Массаж 💆‍♀️')
button4=types.KeyboardButton('Ресницы 🫶')
button5=types.KeyboardButton('Акции')
keyboard2=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)

keyboard2.add(button1,button2)
keyboard2.add(button3,button4)
keyboard2.add(button5)


@dp.message_handler(commands='start')
async def services(message: types.Message):
    with open ('image/image.png','rb') as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption= "Меня зовут Нуриза  \nЯ помогу вам выбрать услугу и записаться на нее.👇👇👇👇👇",reply_markup=keyboard2
        )
async def on_startup(dp):
    await bot.set_my_commands([
        BotCommand(command='/start', description='Запустит бот'),
        BotCommand(command='/adress', description='Наш адрес и контакты'),
        BotCommand(command='/manue', description='Главный меню')
    ])


# tips = [
#             "Совет 1: Регулярно увлажняйте кожу для поддержания её эластичности.",
#             "Совет 2: Используйте солнцезащитный крем, чтобы защитить кожу от ультрафиолетового излучения.",
#             "Совет 3: Пейте достаточно воды для поддержания гидратации кожи.",
#             "Совет 4: Избегайте частого касания лица руками, чтобы предотвратить появление прыщей.",
#             "Совет 5: Используйте очищающие средства, подходящие для вашего типа кожи."
#         ]

class PromoState(StatesGroup):
    waiting_for_number = State()

user_attempts={}

@dp.message_handler(text = 'Акции')
# @dp.message_handler(lambda message: message.text == "Акции")
# async def promo_message(message: types.Message):
#     await message.answer("У нас 20% скидка на все услуги каждому клиенту. Если хотите получить скидку, ответьте любой цифрой 1-2-3-4.")
#     await PromoState.waiting_for_number.set()

# @dp.message_handler(state=PromoState.waiting_for_number)
# async def check_number(message: types.Message, state: FSMContext):
#     correct_number = '2'  # Предположим, что правильный номер  2
#     if message.text == correct_number:
#         await message.answer("Поздравляю, вы правильно угадали. У вас 20% скидка на все услуги. Свяжитесь с нами. Мы ждём вас в нашем салоне.")
#         await message.answer_contact(phone_number='+996777797921', first_name='Eliza', last_name='Erkinbek kyzy')
#         await message.answer_contact(phone_number='+996990130081', first_name='Nuriza', last_name='Xamytbekova')
#     else:
#         await message.answer("Неправильный ответ. Попробуйте ещё раз или нажмите 'Акции' снова, чтобы начать заново.")
#     await state.finish()
async def promo_message(message: types.Message):
    user_id = message.from_user.id

    if user_attempts.get(user_id, 0) >= 2:
        await message.answer("Вы уже получили скидку. Скидку можно получить только один раз.")
    else:
        await message.answer("У нас 20% скидка на все услуги каждому клиенту. Если хотите получить скидку, ответьте любой цифрой 1-2-3-4.")
        await PromoState.waiting_for_number.set()

@dp.message_handler(state=PromoState.waiting_for_number)
async def check_number(message: types.Message, state: FSMContext):
    correct_number = '2'  
    user_id = message.from_user.id
    user_attempts[user_id] = user_attempts.get(user_id, 0) + 1

    if message.text == correct_number:
        await message.answer("Поздравляю, вы правильно угадали. У вас 20% скидка на все услуги. Свяжитесь с нами. Мы ждём вас в нашем салоне.")
        await message.answer_contact(phone_number='+996777797921', first_name='Eliza', last_name='Erkinbek kyzy')
        await message.answer_contact(phone_number='+996990130081', first_name='Nuriza', last_name='Xamytbekova')
    else:
        await message.answer("Неправильный ответ. Попробуйте ещё раз или нажмите 'Акции' снова, чтобы начать заново.")

    
    if user_attempts[user_id] >= 2:
        await message.answer("Скидку можно получить только один раз.")
    
    await state.finish()




@dp.message_handler(commands='adress')
async def adress(message: types.Message):
    await message.answer('Вот наши контакты: ☎️')
    await message.answer_contact(phone_number='+996777797921', first_name='Eliza', last_name='Erkinbek kyzy')
    await message.answer_contact(phone_number='+996990130081', first_name='Nuriza', last_name='Xamytbekova')
    await message.answer('Мы рады будем Вам ответить!')
    await message.reply(' 📍 Наш адрес: Город Ош, район Кара-Суу, трц Айбийке 1-этаж ')
    await message.reply_location(latitude=40.708585, longitude=72.891825)

@dp.message_handler(commands='manue')
async def back_to_main_manue(message:types.Message):
    await services(message)


class Hairdressing_services:
    @dp.message_handler(text='Парикмахерские услуги 💇')
    async def parix(message:types.Message):
        hair_keyboard= types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        hair_button1= types.KeyboardButton('➖ Cтрижка ➖')
        hair_button2=types.KeyboardButton('➖ окрашивание волос ➖')
        hair_button3=types.KeyboardButton('👈 Назад')
        hair_button4 = types.KeyboardButton('➖ Мастер парикмахерских услуг ➖')

        hair_keyboard.add(hair_button1)
        hair_keyboard.add(hair_button2)
        hair_keyboard.add(hair_button3, hair_button4)

        with open ('image/image4.png', 'rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption="""В нашем салоне вам доступно 2 вида парихмахерских услуг:
                \n- Cтрижка
                \n- окрашивание волос""",
                reply_markup=hair_keyboard 
            ) 

    @dp.message_handler(lambda message: message.text == '👈 Назад')
    async def handle_back2(message: types.Message):
        await services(message)

    @dp.message_handler(text='Мастер парикмахерских услуг')
    async def show_master_info(message: types.Message):
        master_name = "Анна Иванова"
        master_description = (
            "Опыт работы: 10 лет\n"
            "Специализация: Парикмахер-стилист\n"
            "Дополнительные навыки: Окрашивание волос, "
            "уход за волосами, создание свадебных причесок\n"
            "Образование: Московская школа парикмахерского искусства\n"
            "Отзывы клиентов: ⭐⭐⭐⭐⭐\n"
            "Контакт: +7 (123) 456-78-90"
        )

        with open('image/master_hair.png', 'rb') as photo:  
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"Мастер: {master_name}\n\n{master_description}"
            )

    class Haircut:
        @dp.message_handler(text='➖ Cтрижка ➖')
        async def hair_cut(message: types.Message):
            hair_keyboard = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_hairdressing_services')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Cтрижка')
            
            hair_keyboard.add(button2)
            hair_keyboard.add(button1)

            with open('image/image7.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Женские стрижки представляют собой разнообразие стилей, которые могут подчеркнуть индивидуальность и обновить образ. Вот некоторые популярные виды:\n
        Лесенка: Переходы длины волос создают эффект лестницы, что придает объем.
                Длительность:от 30 минут и выше
                Цена: 450 сом\n
        Каскад: Слои волос создают каскадный эффект, придают динамичность и объем.
                Длительность:зависит от густоты волос, от 30 минут и выше
                Цена: 500 сом\n
        Каре: Стрижка с четкими линиями, часто доходит до подбородка или плеч.
                Длительность:  от 60 до 120 минут
                Цена: 800 сом""",
                    reply_markup=hair_keyboard
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_hairdressing_services')
        async def handle_back_to_hairdressing_services(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Hairdressing_services.parix(callback_query.message)

        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)



    class Haircoloring:
        @dp.message_handler(text='➖ окрашивание волос ➖')
        async def hair_cut(message: types.Message):
            hair_keyboard = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_hairdressing_services')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_окрашивание волос')
            
            hair_keyboard.add(button2)
            hair_keyboard.add(button1)

            with open('image/image8.png', 'rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Окрашивание волос — самый простой способ быстро сменить образ и подчеркнуть индивидуальность. Вот некоторые популярные виды:\n
        Мелирование.
        Колорирование
        Брондирование
        Мажимеш
        Тонирование\n 
        ❗️Стоимость и время, затрачиваемое на окрашивание волос, зависит от густоты и длины волос.""",
                    reply_markup=hair_keyboard
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_hairdressing_services')
        async def handle_back_to_hairdressing_services(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Hairdressing_services.parix(callback_query.message)


        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)


class Eyelashes:  
    @dp.message_handler(text='Ресницы 🫶')
    async def massaj(message: types.Message):
    
        keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        button1 = types.KeyboardButton('➖ Наращивание ➖')
        button2 = types.KeyboardButton('➖ Ламинирование ➖')
        button3 = types.KeyboardButton('👈 Назад')
        button4 = types.KeyboardButton('➖ Мастер ресниц ➖')

        keyboard3.add(button1)
        keyboard3.add(button2)
        keyboard3.add(button3,button4)
        
        with open('image/image6.png','rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption="""В нашем салоне вам доступно 2 вида услуга реснице:
                \n- Наращивание
                \n- Ламинирование
                """,
                reply_markup=keyboard3
            )

    @dp.message_handler(text='➖ Мастер ресниц ➖')
    async def show_lash_master_info(message: types.Message):
        master_name = "Екатерина Петрова"
        master_description = (
            "Опыт работы: 5 лет\n"
            "Специализация: Лэшмейкер\n"
            "Дополнительные навыки: Наращивание ресниц, ламинирование ресниц, коррекция бровей\n"
            "Образование: Академия красоты и эстетики\n"
            "Отзывы клиентов: ⭐⭐⭐⭐⭐\n"
            "Контакт: +7 (987) 654-32-10"
        )

        with open('image/master_eyes.png', 'rb') as photo:  # Укажите путь к PNG файлу мастера ресниц
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"Мастер по ресницам: {master_name}\n\n{master_description}"
            )


    class Eyelashextensions:
        @dp.message_handler(text='➖ Наращивание ➖')
        async def eyelashextensions(message:types.Message):
            keyboard_eyes = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_eyelash')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Наращивание')
            
            keyboard_eyes.add(button2)
            keyboard_eyes.add(button1)

            with open('image/image9.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Наращивание ресниц в салоне, центре красоты – популярная и безопасная процедура увеличения длины и объема ресниц, помогает придать глазам выразительность и привлекательность .\n
        
                Длительность:  от 30 минут до 2 часа
                Цена: от 700 до 1500 сом""",
                    reply_markup=keyboard_eyes
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_eyelash')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Eyelashes.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)

    class Eyelashlamination:
        @dp.message_handler(text='➖ Ламинирование ➖')
        async def eyelashlamination(message:types.Message):
            keyboard_eyes = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_lamination')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Ламинирование')
            
            keyboard_eyes.add(button2)
            keyboard_eyes.add(button1)

            with open('image/image10.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Ламинирование ресниц — косметическая процедура, которая придает ресницам густоту и красивый изгиб на несколько недель. После обработки специальным составом они выглядят сильными, объемными и блестящими. Взгляд становится открытым и выразительным.\n
        
                Длительность: 1 час
                Цена: 700 сом""",
                    reply_markup=keyboard_eyes
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_lamination')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Eyelashes.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)


class Manicure:  
    @dp.message_handler(text='Маникюр 💅')
    async def massaj(message: types.Message):
    
        keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        button1 = types.KeyboardButton('➖ Наращивание ногтей ➖')
        button2 = types.KeyboardButton('➖ SPA маникюр ➖')
        button3 = types.KeyboardButton('➖ Европейский маникюр ➖')
        button4 = types.KeyboardButton('👈 Назад')
        button5 = types.KeyboardButton('➖ Мастер маникюра ➖')

        keyboard3.add(button1)
        keyboard3.add(button2)
        keyboard3.add(button3)
        keyboard3.add(button4, button5)

        with open ('image/image5.png' , 'rb') as photo:
        
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption="""В нашем салоне вам доступно 3 вида услуга маникюра:
                \n- Наращивание ногтей
                \n- SPA маникюр
                \n- Европейский маникюр""",
                reply_markup=keyboard3
            )

    @dp.message_handler(text='➖ Мастер маникюра ➖')
    async def show_manicure_master_info(message: types.Message):
        master_name = "Анна Иванова"
        master_description = (
            "Опыт работы: 7 лет\n"
            "Специализация: Мастер маникюра и педикюра\n"
            "Дополнительные навыки: Дизайн ногтей, наращивание ногтей\n"
            "Образование: Школа ногтевого искусства\n"
            "Отзывы клиентов: ⭐⭐⭐⭐⭐\n"
            "Контакт: +7 (912) 345-67-89"
        )

        with open('image/master_manekur.png', 'rb') as photo:  # Укажите путь к PNG файлу мастера маникюра
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"Мастер по маникюру: {master_name}\n\n{master_description}"
            )


    class Nailextensions:
        @dp.message_handler(text='➖ Наращивание ногтей ➖')
        async def eyelashextensions(message:types.Message):
            keyboard_eyes = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_naillash')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Наращивание ногтей')
            
            keyboard_eyes.add(button2)
            keyboard_eyes.add(button1)

            with open('image/image11.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Наращивание ногтей — это процесс, когда искусственные ногти клеятся поверх натуральной пластины с помощью различных техник и базовых материалов.Длинные ухоженные ногти — прекрасный атрибут красивого и женственного образа. \n
        
                Длительность: больше 60 минут;
                Цена: от 500 до 1000 сом""",
                    reply_markup=keyboard_eyes
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_naillash')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Manicure.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)

    class SPAmanicure:
        @dp.message_handler(text='➖ SPA маникюр ➖')
        async def spa(message:types.Message):
            keyboard_eyes = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_spamanik')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_SPA маникюр')
            
            keyboard_eyes.add(button2)
            keyboard_eyes.add(button1)

            with open('image/image12.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Спа-маникюр - это комплекс процедур, целью которых является улучшение состояния кожи рук, укрепление ногтевой пластины и стимуляция кровообращения. Эта уникальная процедура объединяет разнообразные методики ухода за ногтями, начиная от обычного маникюра и заканчивая ароматерапией и парафинотерапией. \n
        
                Длительность: от 1 до 1,5 часа;
                Цена: 1320 сом""",
                    reply_markup=keyboard_eyes
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_spamanik')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Manicure.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)  
    
    class Europeanmanicure:
        @dp.message_handler(text='➖ Европейский маникюр ➖')
        async def euro(message:types.Message):
            keyboard_eyes = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_europeanmanicure')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Европейский маникюр')
            
            keyboard_eyes.add(button2)
            keyboard_eyes.add(button1)

            with open ('image/image13.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Европейский маникюр – это вид маникюра, который не предусматривает удаления кутикулы. Мастер не использует фрезы, ножницы или кусачки. Размягченная кутикула аккуратно отодвигается при помощи пушера или апельсиновой палочки. \n
        
                Длительность: 1 час;
                Цена: 600 сом""",
                    reply_markup=keyboard_eyes
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_europeanmanicure')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Manicure.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)  

class Massage:
    @dp.message_handler(text='Массаж 💆‍♀️')
    async def massaj(message: types.Message):
    
        keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('➖ Расслабляющий массаж ➖')
        button2 = types.KeyboardButton('➖ Массаж лица ➖')
        button3 = types.KeyboardButton('➖ Массаж стоп ➖')
        button4 = types.KeyboardButton('👈 Назад')
        button5 = types.KeyboardButton('➖ Мастер массажных услуг ➖')

        keyboard3.add(button1)
        keyboard3.add(button2)
        keyboard3.add(button3)
        keyboard3.add(button4, button5)

        with open ('image/image5.png','rb') as photo:
        
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption="""В нашем салоне вам доступно 3 вида массажа:
                \n- Расслабляющий массаж
                \n- Массаж лица
                \n- Массаж стоп""",
                reply_markup=keyboard3
            )

    @dp.message_handler(text='➖ Мастер массажных услуг ➖')
    async def show_massage_master_info(message: types.Message):
        master_name = "Ольга Смирнова"
        master_description = (
            "Опыт работы: 10 лет\n"
            "Специализация: Массажист\n"
            "Дополнительные навыки: Лечебный массаж, антицеллюлитный массаж\n"
            "Образование: Медицинский колледж\n"
            "Отзывы клиентов: ⭐⭐⭐⭐⭐\n"
            "Контакт: +7 (923) 456-78-90"
        )

        with open('image/master_massage.png', 'rb') as photo:  # Укажите путь к PNG файлу мастера массажа
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"Массажист: {master_name}\n\n{master_description}"
        )

    
    class Relaxingmassage:
        @dp.message_handler(text='➖ Расслабляющий массаж ➖')
        async def eyelashextensions(message:types.Message):
            keyboard_massaj = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_relaxmassaj')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Расслабляющий массаж')
            
            keyboard_massaj.add(button2)
            keyboard_massaj.add(button1)

            with open ('image/9007.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Расслабляющий массаж — процедура, позволяющая снять физическое и нервное напряжение, расслабить мышцы, улучшить настроение, повысить иммунитет. Главная цель воздействия — восстановить гармоничное взаимодействие между головным мозгом и мышцами, так как эмоциональные переживания влекут за собой напряжение мышц.\n
        
                Длительность: 1 час;
                Цена: 1500 сом""",
                    reply_markup=keyboard_massaj
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_relaxmassaj')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Massage.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)

    class Facialmassage:
        @dp.message_handler(text='➖ Массаж лица ➖')
        async def facialmassage(message:types.Message):
            keyboard_massaj_facial = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_facimassaj')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Массаж лица')
            
            keyboard_massaj_facial.add(button2)
            keyboard_massaj_facial.add(button1)

            with open ('image/image14.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Массаж лица – это процедура, направленная на восстановление тонуса кожи, улучшение кровообращения и обменных процессов в коже, усиление ее защитных функций, разглаживание мимических морщин.\n
        
                Длительность: 1 час;
                Цена: 1500 сом""",
                    reply_markup=keyboard_massaj_facial
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_footmassaj')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Massage.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)

            
    class Footmassage:
        @dp.message_handler(text='➖ Массаж стоп ➖')
        async def footmassage(message:types.Message):
            keyboard_massaj_foot = types.InlineKeyboardMarkup()
            
            button1 = types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_to_footmassaj')
            button2 = types.InlineKeyboardButton(text='Записаться ✍️', callback_data='book_Массаж стоп')
            
            keyboard_massaj_foot.add(button2)
            keyboard_massaj_foot.add(button1)

            with open('image/image15.png','rb') as photo:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo,
                    caption="""Массаж стоп – это древняя восточная процедура, которая предназначается для общего расслабления, лечения различных заболеваний и поддержания здоровья. На стопах человека расположено около 70 тысяч нервных окончаний! Которые отвечают за работу внутренних органов.\n
        
                Длительность: 1 час;
                Цена: 1500 сом""",
                    reply_markup=keyboard_massaj_foot
        )
            
        @dp.callback_query_handler(lambda c: c.data == 'back_to_footmassaj')
        async def handle_back_to_eyelash(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await Massage.massaj(callback_query.message)
        
        @dp.callback_query_handler(lambda c: c.data.startswith('book_'))
        async def handle_book_to_hair(callback_query: types.CallbackQuery):
            await BookingHandler.handle_booking(bot, callback_query)

        @dp.message_handler(state=BookingState.waiting_for_name)
        async def handle_name_input(message: types.Message, state: FSMContext):
            await BookingHandler.handle_name_input(message, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('date_'), state='*')
        async def handle_date_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_date_selection(bot, callback_query, state)

        @dp.callback_query_handler(lambda c: c.data.startswith('time_'), state=BookingState.waiting_for_time)
        async def handle_time_selection(callback_query: types.CallbackQuery, state: FSMContext):
            await BookingHandler.handle_time_selection(bot, callback_query, state)



if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup) 