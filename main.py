import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.orm import Session

from core.config import settings
from depends import get_session
from forms import Resident
from repositories.resident_repos import ResidentRepository
from resource_access.db_session import session

form_router = Router()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Resident.name)
    await message.answer(
        "Hi there! What's resident name?",
    )


@form_router.message(Resident.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Resident.home_number)
    await message.answer("What's resident home number")


@form_router.message(Resident.home_number)
async def process_home_number(message: Message, state: FSMContext) -> None:
    await state.update_data(home_number=message.text)
    await message.answer("Wait a minute")

    async with session as db_session:
        repos = ResidentRepository(db_session)
        resident = await repos.create_resident(await state.get_data())
    await message.answer(f"Add resident with name: {resident.name}")

    await state.clear()


async def main():
    bot = Bot(token=settings.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
