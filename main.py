import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.config import settings
from forms import Resident, ElectricityReading
from repositories.resident_repos import ResidentRepository, ElectricityReadingRepository
from resource_access.db_session import session
from schemas import Electricity

form_router = Router()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer("Hi there! I have two command: \n/add_resident and /add_reading")


@form_router.message(Command('add_resident'))
async def add_resident(message: Message, state: FSMContext) -> None:
    await state.set_state(Resident.name)
    await message.answer("Ok, what's resident name")


@form_router.message(Resident.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Resident.home_number)
    await message.answer("What's resident home number?")


@form_router.message(Resident.home_number)
async def process_home_number(message: Message, state: FSMContext) -> None:
    await state.update_data(home_number=message.text)
    await message.answer("Wait a minute")

    async with session as db_session:
        repos = ResidentRepository(db_session)
        resident = await repos.create_resident(await state.get_data())
    await message.answer(f"Add resident with name: {resident.name}")

    await state.clear()


@form_router.message(Command("add_reading"))
async def add_readings(message: Message, state: FSMContext) -> None:
    await state.set_state(ElectricityReading.resident_id)
    await message.answer("What's resident home number?")


@form_router.message(ElectricityReading.resident_id)
async def process_resident_id(message: Message, state: FSMContext) -> None:
    async with session as db_session:
        repos = ResidentRepository(db_session)
        resident = await repos.get_resident_by_home_number(message.text)  # there may be an error due to the str

    if resident:
        await state.update_data(resident_id=resident.id)
        await state.set_state(ElectricityReading.current_kwh)
        await message.answer("Pleas write electricity kwh")
    else:
        await message.answer("Not found resident with this home number")

        await state.clear()


@form_router.message(ElectricityReading.current_kwh)
async def process_current_reading(message: Message, state: FSMContext) -> None:
    current_kwh = message.text
    electricity_data = await state.get_data()
    electricity = Electricity(resident_id=electricity_data.get('resident_id'))

    if current_kwh.isdigit():
        electricity.current_kwh = int(current_kwh)
    else:
        await message.answer("Pleas enter integer")
        await state.set_state(ElectricityReading.current_kwh)
        return None  # stop this function

    async with (session as db_session):
        repos = ElectricityReadingRepository(db_session)
        last_electricity = await repos.get_last_reading_by_resident_id(electricity.resident_id)

        if last_electricity:
            electricity.consumed_kwh = electricity.current_kwh - last_electricity.current_kwh

            if electricity.consumed_kwh <= settings.LIMIT:
                electricity.amount = electricity.consumed_kwh * settings.TARIFF
            else:
                electricity.not_increased_amount = settings.LIMIT * settings.TARIFF
                electricity.increased_kwh = electricity.consumed_kwh - settings.LIMIT
                electricity.increased_amount = electricity.increased_kwh * settings.INCREASED_TARIFF
                electricity.amount = electricity.not_increased_amount + electricity.increased_amount

        electricity = await repos.create_reading(electricity)

    await message.answer(f"Итоговая сумма: {electricity.amount}\n"
                         f"Изразходовано киловатт: {electricity.consumed_kwh}"
                         f"Превышено киловатт: {electricity.increased_kwh}\n"
                         f"Превышенная сумма: {electricity.increased_amount}")


async def main():
    bot = Bot(token=settings.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
