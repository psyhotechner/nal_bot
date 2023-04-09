import logging
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from config import token
from db.database import Database

class UserRegistration(StatesGroup):
    waiting_for_fullname = State()
    waiting_for_specialty = State()

class TelegramBot:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bot = Bot(token=token, parse_mode=ParseMode.HTML)
        self.dispatcher = Dispatcher(self.bot, storage=MemoryStorage())
        self.database = Database()

        self.dispatcher.register_message_handler(CommandStart(), self.start)
        self.dispatcher.register_message_handler(self.add_user_fullname, state=UserRegistration.waiting_for_fullname)
        self.dispatcher.register_message_handler(self.add_user_specialty, state=UserRegistration.waiting_for_specialty)

    async def start(self, message: types.Message):
        await message.answer("Привет! Введите свое ФИО в формате: <code>Иванов Иван Иванович</code>")

        await UserRegistration.waiting_for_fullname.set()

    async def add_user_fullname(self, message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        fullname = message.text

        await state.update_data(fullname=fullname)
        await message.answer("Введите вашу специальность:")

        await UserRegistration.waiting_for_specialty.set()

    async def add_user_specialty(self, message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        data = await state.get_data()
        fullname = data.get("fullname")
        specialty = message.text

        registration_date = datetime.datetime.now()

        last_name, first_name, second_name = fullname.split(' ')
        self.database.add_user(user_id, last_name, first_name, second_name, specialty, registration_date)

        await message.answer("Данные сохранены в базе данных")
        await state.finish()

    async def run(self):
        await self.dispatcher.start_polling()
        self.logger.info("Bot started polling...")