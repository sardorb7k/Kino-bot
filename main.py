import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from config import token
from buttons import kodlarni_qidirish, kanalga_otish, admin_first, ye_or_no, finish_setup
from states2 import Kino, Admin
from fetch_db import fetch_data
from insert_db import insert_data

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command('start'))
async def StartCommand(message: types.Message, state: FSMContext):
    await state.set_state(Kino.code)
    await message.answer_photo(
        photo="https://thumbs.dreamstime.com/b/%D1%88%D0%B8%D1%84%D0%B5%D1%80-%D0%BA%D0%B8%D0%BD%D0%BE-%D0%B8-%D0%B2%D1%8C%D1%8E%D1%80%D0%BE%D0%BA-%D1%84%D0%B8-%D1%8C%D0%BC%D0%B0-%D0%BD%D0%B0-%D1%80%D0%B5%D0%B2%D0%B5%D1%81%D0%B8%D0%BD%D0%B5-36502412.jpg", 
        caption=f"Salom <b>{message.from_user.full_name}</b> 👋\n\n<i>Marhamat, kerakli kodni yuboring</i>",
        parse_mode="HTML",
        reply_markup=kodlarni_qidirish
    )

@dp.message(Command('search'))
async def StartCommand(message: types.Message, state: FSMContext):
    await state.set_state(Kino.code)
    await message.answer_photo(
        photo="https://thumbs.dreamstime.com/b/%D1%88%D0%B8%D1%84%D0%B5%D1%80-%D0%BA%D0%B8%D0%BD%D0%BE-%D0%B8-%D0%B2%D1%8C%D1%8E%D1%80%D0%BE%D0%BA-%D1%84%D0%B8-%D1%8C%D0%BC%D0%B0-%D0%BD%D0%B0-%D1%80%D0%B5%D0%B2%D0%B5%D1%81%D0%B8%D0%BD%D0%B5-36502412.jpg", 
        caption=f"Salom <b>{message.from_user.full_name}</b> 👋\n\n<i>Marhamat, kerakli kodni yuboring</i>",
        parse_mode="HTML",
        reply_markup=kodlarni_qidirish
    )

@dp.message(Command('admin'))
async def AdminCommand(message: types.Message, state: FSMContext):
    await message.answer("Hurmatli admin, 'database'ga yangi kino qo'shmoqchimisiz?", reply_markup=admin_first)

@dp.message(F.text == 'Ha')
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    await state.set_state(Admin.nomi)
    await message.answer('Kino nomini kiriting!')

@dp.message(F.text == "Yo'q, keyinroq")
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    await message.answer("Buyruq bekor qilindi.\nYangi kino yuklash uchun /admin buyrug'idan foydalaning\nKinolarni qidirish uchun esa /search")
    await state.clear()

@dp.message(Admin.nomi)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    kino_nomi = message.text
    await state.update_data(
        {'nomi': kino_nomi}
    )
    await message.answer("Kino sifatini kiriting!")
    await state.set_state(Admin.sifati)

@dp.message(Admin.sifati)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    kino_sifati = message.text
    await state.update_data(
        {'sifati': kino_sifati}
    )
    await message.answer("Kino janrini kiriting!")
    await state.set_state(Admin.janri)

@dp.message(Admin.janri)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    kino_janri = message.text
    await state.update_data(
        {'janri': kino_janri}
    )
    await message.answer("Kino yosh chegarasini kiriting!")
    await state.set_state(Admin.yosh_chegarasi)
    
@dp.message(Admin.yosh_chegarasi)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    kino_yosh_chegarasi = message.text
    await state.update_data(
        {'yosh_chegarasi': kino_yosh_chegarasi}
    )
    await message.answer("Kino urlini kiriting!")
    await state.set_state(Admin.video_url)

@dp.message(Admin.video_url)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    kino_video_url = message.text
    await state.update_data(
        {'video_url': kino_video_url}
    )
    data = await state.get_data()
    await message.answer_video(
                video=data['video_url'], 
                caption=f"\n🎦 Nomi: {data['nomi']}\n💻 Sifati: {data['sifati']}p\n🔋Janri: {data['janri']}\n❗️Yosh chegarasi: {data['yosh_chegarasi']}+\n🎥 Kanal: @t.me/kino_bot_uchun_kanal", 
            )
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=ye_or_no)
    await state.set_state(Admin.finish)

@dp.message(Admin.finish)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    finish_check = message.text
    data = await state.get_data()
    if finish_check == "Ha, to'gri!":
        insert_data(name=data['nomi'], quality=data['sifati'], genre=data['janri'], limitation=data['yosh_chegarasi'], video_url=data['video_url'])
        await message.answer("Yangi kino muvaffaqiyatli saqlandi!", reply_markup=finish_setup)
        await state.set_state(Admin.leave)
    elif finish_check == "Yo'q, xatolik bor!":
        await message.answer("Ma'lumot yuklanmadi.\nYangi kino yuklash uchun /admin buyrug'idan foydalaning\nKinolarni qidirish uchun esa /search")
        await state.clear()

@dp.message(Admin.leave)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    user_choice = message.text
    if user_choice == "Yana qo'shish":
        await message.answer('Kino nomini kiriting!')
        await state.set_state(Admin.nomi)
    elif user_choice == "Tugatish":
        await message.answer("Yangi kino yuklash uchun /admin buyrug'idan foydalaning\nKinolarni qidirish uchun esa /search")
        await state.clear()


@dp.message(Kino.code)
async def TranslateLangCommand(message: types.Message, state: FSMContext):
    code = message.text
    data = fetch_data()
    for i in data:
        if int(code) == int(i[0]):
            await message.answer_video(
                video=i[5], 
                caption=f"\n🎦 Nomi: {i[1]}\n💻 Sifati: {i[2]}p\n🔋 Janri: {i[3]}\n❗️Yosh chegarasi: {i[4]}+\n🎥 Kanal: {i[6]}", 
                reply_markup=kanalga_otish
            )
            break
    await state.set_state(Kino.code)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())