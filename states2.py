from aiogram.fsm.state import State, StatesGroup

class Kino(StatesGroup):
    code = State()

class Admin(StatesGroup):
    nomi = State() 
    sifati = State() 
    janri = State() 
    yosh_chegarasi = State() 
    video_url = State()
    finish = State()
    leave = State()